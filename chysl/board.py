"Chart to place charts at specified positions."

import copy

import constants
import schema
from chart import Chart, Element, parse


class Board(Chart):
    "Chart to place charts at specified positions."

    DEFAULT_TITLE_FONT_SIZE = 36

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "items"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "board"},
            "title": {"$ref": "#title"},
            "description": {"$ref": "#description"},
            "items": {
                "title": "Subcharts at specified positions.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["subchart", "x", "y"],
                    "additionalProperties": False,
                    "properties": {
                        "subchart": {"$ref": "#chart_or_include"},
                        "x": {
                            "title": "Absolute position of subchart. Left is 0.",
                            "type": "number",
                            "minimum": 0,
                        },
                        "y": {
                            "title": "Absolute position of subchart. Top is 0.",
                            "type": "number",
                            "minimum": 0,
                        },
                        "scale": {
                            "title": "Scaling of the subchart.",
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

    def __init__(self, title=None, description=None, items=None):
        super().__init__(title=title, description=description)
        assert items is None or isinstance(items, list)

        self.items = []
        if items:
            for item in items:
                self.add(item)

    def __iadd__(self, item):
        self.add(item)
        return self

    def add(self, item):
        "Add the item (subchart with position etc) to the board."
        assert isinstance(item, dict)
        self.add_item(**item)

    def add_item(self, subchart, x, y, scale=None, opacity=None):
        assert isinstance(subchart, (dict, Chart))
        assert isinstance(x, (int, float)) and x >= 0
        assert isinstance(y, (int, float)) and y >= 0
        assert scale is None or isinstance(scale, (int, float)) and scale > 0
        assert (
            opacity is None or isinstance(opacity, (int, float)) and 0 <= opacity <= 1
        )
        if isinstance(subchart, dict):
            subchart = parse(subchart)
        self.items.append(
            dict(subchart=subchart, x=x, y=y, scale=scale, opacity=opacity)
        )

    def as_dict(self):
        result = super().as_dict()
        result["items"] = []
        for item in self.items:
            i = dict(x=item["x"], y=item["y"])
            subchart = item["subchart"]
            try:  # If this subchart was included from another source.
                i["subchart"] = dict(include=subchart.location)
            except AttributeError:
                i["subchart"] = subchart.as_dict()
            if (scale := item.get("scale")) and scale != 1:
                i["scale"] = scale
            if (opacity := item.get("opacity")) is not None and opacity != 1:
                i["opacity"] = opacity
            result["items"].append(i)
        return result

    def build(self):
        """Create the SVG elements in the 'svg' attribute.
        Adds the title, if defined.
        Sets the 'svg', 'height' and 'width' attributes.
        """
        for item in self.items:
            item["subchart"].build()

        self.width = 0
        for item in self.items:
            self.width = max(
                self.width,
                item["x"] + (item.get("scale") or 1) * item["subchart"].width,
            )

        super().build()

        offset = self.height
        for item in self.items:
            transforms = []
            if (scale := item.get("scale")) and scale != 1:
                transforms.append(f"scale({scale})")
            transforms.append(f"translate({item['x']}, {item['y'] + offset})")
            g = Element("g", transform=" ".join(transforms))
            if (opacity := item.get("opacity")) is not None and opacity != 1:
                g["opacity"] = opacity
            g.append(item["subchart"].svg)
            self.svg += g
            self.height = max(
                self.height,
                item["y"] + offset + (item.get("scale") or 1) * item["subchart"].height,
            )
