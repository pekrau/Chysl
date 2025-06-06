"Charts stacked in a column."

import constants
import schema
from chart import Chart, Layout, parse, register
from minixml import Element
from utils import N


class Column(Chart):
    "Charts stacked in a column."

    DEFAULT_TITLE_FONT_SIZE = 22
    DEFAULT_ALIGN = constants.CENTER
    DEFAULT_PADDING = 0

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "subcharts"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "column"},
            "title": {"$ref": "#title"},
            "description": {"$ref": "#description"},
            "align": {
                "title": "Align charts horizontally within the column.",
                "enum": constants.HORIZONTAL,
                "default": DEFAULT_ALIGN,
            },
            "padding": {
                "title": "Padding between the subcharts.",
                "type": "number",
                "minimum": 0,
                "default": constants.DEFAULT_PADDING,
            },
            "subcharts": {
                "title": "Charts in the column.",
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
        assert align is None or align in constants.HORIZONTAL
        assert padding is None or (isinstance(padding, (int, float)) and padding >= 0)

        self.align = align or self.DEFAULT_ALIGN
        self.padding = padding if padding is not None else constants.DEFAULT_PADDING
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
        if self.padding is not None and self.padding != constants.DEFAULT_PADDING:
            result["padding"] = self.padding
        return result

    def build(self):
        "Create the SVG elements in the 'svg' attribute."
        super().build()

        for subchart in self.subcharts:
            subchart.build()

        # Create the layout, add the different parts to it and load it.
        layout = Layout(rows=len(self.subcharts), columns=1, title=self.get_title())
        for pos, subchart in enumerate(self.subcharts):
            subchart.build()
            # XXX how deal with alignment?
            for element in subchart.svg:
                layout.add(pos, 0, element)
        self.svg.load_layout(layout)


register(Column)
