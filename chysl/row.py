"Charts arranged in a row."

import constants
import schema
from chart import Chart, Element, parse
from utils import N


class Row(Chart):

    ALIGN_VALUES = constants.VERTICAL

    DEFAULT_TITLE_FONT_SIZE = 22
    DEFAULT_ALIGN = constants.MIDDLE
    DEFAULT_PADDING = 10

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "entries"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "row"},
            "title": {
                "title": "Title of the column chart.",
                "$ref": "#text",
            },
            "align": {
                "title": "Align charts vertically within the row.",
                "enum": ALIGN_VALUES,
                "default": DEFAULT_ALIGN,
            },
            "entries": {
                "title": "Charts in the row.",
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

        self.width = sum([e.width for e in self.entries])
        self.width += (len(self.entries) - 1) * self.DEFAULT_PADDING

        super().build()
        self.height += self.DEFAULT_PADDING

        x = 0
        max_height = max([e.height for e in self.entries])

        for entry in self.entries:
            match self.align:
                case constants.BOTTOM:
                    y = self.height + max_height - entry.height
                case constants.MIDDLE:
                    y = self.height + (max_height - entry.height) / 2
                case constants.TOP:
                    y = self.height
            self.svg += Element(
                "g", entry.svg, transform=f"translate({N(x)}, {N(y)})"
            )
            x += entry.width + self.DEFAULT_PADDING

        self.height += max_height
