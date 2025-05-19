"Chart to place charts at specified positions."

import constants
import schema
from chart import Chart, Element, parse


class Board(Chart):
    "Chart to place charts at specified positions."

    DEFAULT_TITLE_FONT_SIZE = 36

    SCHEMA = {
        "title": __doc__,
        "$anchor": "board",
        "type": "object",
        "required": ["chart", "entries"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "board"},
            "title": {
                "title": "Title of the board.",
                "$ref": "#text",
            },
            "entries": {
                "title": "Component charts at specified positions.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["x", "y", "component"],
                    "additionalProperties": False,
                    "properties": {
                        "x": {
                            "title": "Absolute position of component. Left is 0.",
                            "type": "number",
                            "minimum": 0,
                        },
                        "y": {
                            "title": "Absolute position of component. Top is 0.",
                            "type": "number",
                            "minimum": 0,
                        },
                        "scale": {
                            "title": "Scaling of the component chart.",
                            "type": "number",
                            "exclusiveMinimum": 0,
                            "default": 1,
                        },
                        "component": {"$ref": "#chart_or_include"},
                    },
                },
            },
        },
    }

    schema.add_defs(SCHEMA)

    def append(self, *entry, **fields):
        "Append the entry to the board."
        assert not entry or (len(entry) == 1 and isinstance(entry[0], dict))
        assert bool(fields) ^ bool(entry)
        if entry:
            entry = entry[0]
        else:
            entry = fields
        self.entries.append(self.convert_entry(entry))

    def convert_entry(self, entry):
        if not isinstance(entry, dict):
            raise ValueError(f"invalid entry for board: {entry}; not a dict")
        if not isinstance(x := entry.get("x"), (int, float)) or x < 0:
            raise ValueError(
                f"invalid entry for board: {entry}; 'x' is not a non-negative number"
            )
        if not isinstance(y := entry.get("y"), (int, float)) or y < 0:
            raise ValueError(
                f"invalid entry for board: {entry}; 'y' is not a non-negative number"
            )
        try:
            scale = entry["scale"]
            if not isinstance(scale, (int, float)) or scale <= 0:
                raise ValueError(
                    f"invalid entry for board: {entry}; 'scale' is not a positive number"
                )
        except KeyError:
            scale = 1
        component = entry["component"]
        if isinstance(component, dict):
            component = parse(component)
        if not isinstance(component, Chart):
            raise ValueError(f"invalid entry '{entry}' for {self.name}")
        return {"x": x, "y": y, "scale": scale, "component": component}

    def entries_as_dict(self):
        result = []
        for entry in self.entries:
            entry2 = {"x": entry["x"], "y": entry["y"]}
            if scale := entry.get("scale"):
                entry2["scale"] = scale
            component = entry["component"]
            try:
                entry2["component"] = {"include": component.location}
            except AttributeError:
                entry2["component"] = component.as_dict()
            result.append(entry2)
        return {"entries": result}

    def build(self):
        """Create the SVG elements in the 'svg' attribute.
        Set the 'svg' and 'height' attributes.
        Sets the 'width' attribute.
        """
        for entry in self.entries:
            entry["component"].build()

        self.width = 0
        for entry in self.entries:
            component = entry["component"]
            scale = entry.get("scale") or 1
            self.width = max(self.width, entry["x"] + scale * component.width)

        super().build()

        offset = self.height
        for entry in self.entries:
            component = entry["component"]
            scale = entry.get("scale") or 1
            transform = []
            try:
                transform.append(f"scale({entry['scale']})")
            except KeyError:
                pass
            transform.append(f"translate({entry['x']}, {entry['y'] + offset})")
            g = Element("g", transform=" ".join(transform))
            g.append(component.svg)
            self.svg += g
            self.height = max(
                self.height, entry["y"] + offset + scale * component.height
            )
