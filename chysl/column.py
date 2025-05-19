"Charts stacked in a column."

import constants
import schema
from chart import Chart, Element, parse


class Column(Chart):

    ALIGN_VALUES = constants.HORIZONTAL

    DEFAULT_TITLE_FONT_SIZE = 22
    DEFAULT_ALIGN = constants.CENTER
    DEFAULT_PADDING = 10

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "entries"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "column"},
            "title": {
                "title": "Title of the column chart.",
                "$ref": "#text",
            },
            "align": {
                "title": "Align charts horizontally within the column.",
                "enum": ALIGN_VALUES,
                "default": DEFAULT_ALIGN,
            },
            "entries": {
                "title": "Component charts in the column.",
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#chart_or_include"},
            },
        },
    }

    schema.add_defs(SCHEMA)

    def __init__(
        self,
        title=None,
        entries=None,
        align=None,
    ):
        super().__init__(title=title, entries=entries)
        assert align is None or align in self.ALIGN_VALUES

        self.align = align or self.DEFAULT_ALIGN

    def convert_entry(self, entry):
        if isinstance(entry, dict):
            entry = parse(entry)
        if not isinstance(entry, Chart):
            raise ValueError(f"invalid entry '{entry}' for {self.name}")
        return entry

    def as_dict(self):
        result = super().as_dict()
        if self.align != self.DEFAULT_ALIGN:
            result["align"] = self.align
        return result

    def build(self):
        """Create the SVG elements in the 'svg' attribute. Adds the title, if given.
        Set the 'svg' and 'height' attributes.
        Sets the 'width' attribute.
        """
        for entry in self.entries:
            entry.build()

        self.width = max([e.width for e in self.entries])

        super().build()

        height = self.height
        self.height += sum([e.height for e in self.entries])
        self.height += (len(self.entries) - 1) * self.DEFAULT_PADDING

        for entry in self.entries:
            match self.align:
                case constants.LEFT:
                    x = 0
                case constants.CENTER:
                    x = (self.width - entry.width) / 2
                case constants.RIGHT:
                    x = self.width - entry.width
            self.svg += Element("g", entry.svg, transform=f"translate({x}, {height})")
            height += entry.height + self.DEFAULT_PADDING
