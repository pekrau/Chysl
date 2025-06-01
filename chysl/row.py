"Charts arranged in a row."

import constants
import schema
from chart import Chart, Element, parse
from utils import N


class Row(Chart):
    "Charts arranged in a row."

    DEFAULT_TITLE_FONT_SIZE = 22
    DEFAULT_ALIGN = constants.MIDDLE

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "subcharts"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "row"},
            "title": {
                "title": "Title of the column chart.",
                "$ref": "#text",
            },
            "align": {
                "title": "Align charts vertically within the row.",
                "enum": constants.VERTICAL,
                "default": DEFAULT_ALIGN,
            },
            "padding": {
                "title": "Padding between the subcharts.",
                "type": "number",
                "minimum": 0,
                "default": constants.DEFAULT_PADDING,
            },
            "subcharts": {
                "title": "Charts in the row.",
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#chart_or_include"},
            },
        },
    }

    schema.add_defs(SCHEMA)

    def __init__(self, title=None, subcharts=None, align=None, padding=None):
        super().__init__(title=title)
        assert subcharts is None or isinstance(subcharts, list)
        assert align is None or align in constants.VERTICAL
        assert padding is None or (isinstance(padding, (int, float)) and padding >= 0)

        self.subcharts = []
        if subcharts:
            for subchart in subcharts:
                self.add(subchart)
        self.align = align or self.DEFAULT_ALIGN
        self.padding = padding if padding is not None else constants.DEFAULT_PADDING

    def __iadd__(self, subchart):
        self.add(subchart)
        return self

    def add(self, subchart):
        assert isinstance(subchart, (dict, Chart))
        if isinstance(subchart, dict):
            subchart = parse(subchart)
        self.subcharts.append(subchart)

    def as_dict(self):
        result = super().as_dict()
        result["subcharts"] = []
        for subchart in self.subcharts:
            try:  # If this subchart was included from another source.
                result["subcharts"].append(dict(include=subchart.location))
            except AttributeError:
                result["subcharts"].append(subchart.as_dict())
        if self.align != self.DEFAULT_ALIGN:
            result["align"] = self.align
        if self.padding is not None and self.padding != constants.DEFAULT_PADDING:
            result["padding"] = self.padding
        return result

    def build(self):
        """Create the SVG elements in the 'svg' attribute.
        Adds the title, if defined.
        Sets the 'svg', 'height' and 'width' attributes.
        """
        for subchart in self.subcharts:
            subchart.build()

        self.width = sum([s.width for s in self.subcharts])
        self.width += (len(self.subcharts) - 1) * self.padding

        super().build()

        x = 0
        max_height = max([s.height for s in self.subcharts])

        for subchart in self.subcharts:
            match self.align:
                case constants.BOTTOM:
                    y = self.height + max_height - subchart.height
                case constants.MIDDLE:
                    y = self.height + (max_height - subchart.height) / 2
                case constants.TOP:
                    y = self.height
            self.svg += Element(
                "g", subchart.svg, transform=f"translate({N(x)}, {N(y)})"
            )
            x += subchart.width + self.padding

        self.height += max_height
