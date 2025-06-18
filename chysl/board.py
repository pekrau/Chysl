"Chart to place charts at specified positions."

import components
import constants
import schema
from chart import Chart, Layout, register, parse
from minixml import Element


class Board(Chart):
    "Chart to place charts at specified positions, with optional opacity."

    TITLE_CLASS = components.CompoundTitle

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "items"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "board"},
            "title": {
                "title": "Title of the chart.",
                "$ref": "#text",
            },
            "description": {
                "title": "Description of the chart. Rendered as <desc> in SVG.",
                "type": "string",
            },
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
                        "opacity": {
                            "title": "Opacity of the subchart.",
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                            "default": 1,
                        },
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
        "Create the SVG elements in the 'svg' attribute."
        super().build()
        board = Element("g")
        board.total_width = 0
        board.total_height = 0

        for item in self.items:
            item["subchart"].build()
            svg = item["subchart"].svg
            xhigh = item["x"] + (item.get("scale") or 1) * svg.total_width
            yhigh = item["y"] + (item.get("scale") or 1) * svg.total_height
            board.total_width = max(board.total_width, xhigh)
            board.total_height = max(board.total_height, yhigh)

            board += (elem := Element("g", *list(svg)))
            elem["class"] = "subchart"
            transforms = [f"translate({item['x']},{item['y']})"]
            if (scale := item.get("scale")) and scale != 1:
                transforms.append(f"scale({scale})")
            elem["transform"] = " ".join(transforms)
            if (opacity := item.get("opacity")) is not None and opacity != 1:
                elem["opacity"] = opacity

        layout = Layout(rows=1, columns=1, title=self.title)
        layout.add(0, 0, board)
        self.svg.load_layout(layout)


register(Board)
