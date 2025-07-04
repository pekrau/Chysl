"Charts arranged in a row."

import components
import constants
import schema
from chart import Chart, Layout, register, parse
from minixml import Element
from utils import N


class Row(Chart):
    "Charts arranged in a row."

    TITLE_CLASS = components.CompoundTitle

    DEFAULT_ALIGN = constants.MIDDLE

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "subcharts"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "row"},
            "title": {
                "title": "Title of the chart.",
                "$ref": "#text",
            },
            "description": {
                "title": "Description of the chart. Rendered as <desc> in SVG.",
                "type": "string",
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
                "default": 0,
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

    def __init__(
        self, title=None, description=None, subcharts=None, align=None, padding=None
    ):
        super().__init__(title=title, description=description)
        assert subcharts is None or isinstance(subcharts, list)
        assert align is None or align in constants.VERTICAL
        assert padding is None or (isinstance(padding, (int, float)) and padding >= 0)

        self.align = align or self.DEFAULT_ALIGN
        self.padding = padding
        self.subcharts = []
        if subcharts:
            for subchart in subcharts:
                self.add(subchart)

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
        if self.padding is not None:
            result["padding"] = self.padding
        return result

    def build(self):
        "Create the SVG elements in the 'svg' attribute."
        super().build()
        layout = Layout(
            rows=1,
            columns=len(self.subcharts),
            title=self.title,
            hpadding=self.padding,
            vpadding=self.padding,
        )

        for pos, subchart in enumerate(self.subcharts):
            subchart.build()
            for element in subchart.svg:
                layout.add(0, pos, element)

        self.svg.load_layout(layout)


register(Row)
