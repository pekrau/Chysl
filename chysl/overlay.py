"Charts overlayed over one another, with optional opacity."

import constants
import schema
from chart import Chart, Element, parse
from utils import N


class Overlay(Chart):

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "entries"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "overlay"},
            "title": {
                "title": "Title of the overlay chart.",
                "$ref": "#text",
            },
            "entries": {
                "title": "Charts to overlay, with optional opacity.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "title": "Chart with opacity.",
                    "type": "object",
                    "required": ["item"],
                    "additionalProperties": False,
                    "properties": {
                        "item": {"$ref": "#chart_or_include"},
                        "opacity": {"$ref": "#opacity"},
                    },
                },
            },
        },
    }

    schema.add_defs(SCHEMA)

    def convert_entry(self, entry):
        if isinstance(entry, Chart):  # Python syntactic sugar; not allowed in YAML.
            return dict(item=entry, opacity=1)
        try:
            item = entry["item"]
        except KeyError:
            raise ValueError(f"invalid entry '{entry}' for {self.name}")
        if isinstance(item, dict):
            entry["item"] = parse(item)
        if not isinstance(entry["item"], Chart):
            raise ValueError(f"invalid entry '{entry}' for {self.name}")
        if "opacity" not in entry:
            entry["opacity"] = 1
        return entry

    def entries_as_dict(self):
        result = []
        for entry in self.entries:
            if entry["opacity"] == 1:
                e = dict()
            else:
                e = dict(opacity=entry["opacity"])
            try:
                e["item"] = entry["item"].location
            except AttributeError:
                e["item"] = entry["item"].as_dict()
            result.append(e)
        return {"entries": result}

    def build(self):
        """Create the SVG elements in the 'svg' attribute. Adds the title, if given.
        Set the 'svg' and 'height' attributes.
        Sets the 'width' attribute.
        """
        for entry in self.entries:
            entry["item"].build()

        self.width = max([e["item"].width for e in self.entries])

        super().build()

        for entry in self.entries:
            self.svg += Element(
                "g",
                entry["item"].svg,
                transform=f"translate(0,{N(self.height)})",
                opacity=entry["opacity"],
            )

        self.height += max([e["item"].height for e in self.entries])
