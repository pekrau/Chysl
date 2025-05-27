"Chart to place charts at specified positions."

import constants
import schema
from chart import Chart, Element, parse


class Board(Chart):
    "Chart to place charts at specified positions."

    DEFAULT_TITLE_FONT_SIZE = 36

    SCHEMA = {
        "title": __doc__,
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
                "title": "Charts at specified positions.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["x", "y", "item"],
                    "additionalProperties": False,
                    "properties": {
                        "item": {"$ref": "#chart_or_include"},
                        "x": {
                            "title": "Absolute position of item. Left is 0.",
                            "type": "number",
                            "minimum": 0,
                        },
                        "y": {
                            "title": "Absolute position of item. Top is 0.",
                            "type": "number",
                            "minimum": 0,
                        },
                        "scale": {
                            "title": "Scaling of the item chart.",
                            "type": "number",
                            "exclusiveMinimum": 0,
                            "default": 1,
                        },
                        "opacity": {"$ref": "#opacity"},
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
        item = entry["item"]
        if isinstance(item, dict):
            item = parse(item)
        if not isinstance(item, Chart):
            raise ValueError(f"invalid entry '{entry}' for {self.name}")
        return {"x": x, "y": y, "scale": scale, "item": item}

    def entries_as_dict(self):
        result = []
        for entry in self.entries:
            e = {"x": entry["x"], "y": entry["y"]}
            if scale := entry.get("scale"):
                e["scale"] = scale
            item = entry["item"]
            try:
                e["item"] = {"include": item.location}
            except AttributeError:
                e["item"] = item.as_dict()
            result.append(e)
        return {"entries": result}

    def build(self):
        """Create the SVG elements in the 'svg' attribute.
        Set the 'svg' and 'height' attributes.
        Sets the 'width' attribute.
        """
        for entry in self.entries:
            entry["item"].build()

        self.width = 0
        for entry in self.entries:
            scale = entry.get("scale") or 1
            self.width = max(self.width, entry["x"] + scale * entry["item"].width)

        super().build()

        offset = self.height
        for entry in self.entries:
            scale = entry.get("scale") or 1
            transforms = []
            try:
                transforms.append(f"scale({entry['scale']})")
            except KeyError:
                pass
            transforms.append(f"translate({entry['x']}, {entry['y'] + offset})")
            g = Element("g", transform=" ".join(transforms))
            try:
                g["opacity"] = entry["opacity"]
            except KeyError:
                pass
            g.append(entry["item"].svg)
            self.svg += g
            self.height = max(
                self.height, entry["y"] + offset + scale * entry["item"].height
            )
