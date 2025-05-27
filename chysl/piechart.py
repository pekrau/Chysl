"Pie chart with slices."

import itertools

import constants
import schema
import utils
from color import Color
from degrees import Degrees
from chart import Chart, Entry, Element
from path import Path
from vector2 import Vector2


class Piechart(Chart):
    "Pie chart containing slices."

    DEFAULT_DIAMETER = 200
    DEFAULT_START = Degrees(-90)

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "entries"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "piechart"},
            "title": {
                "title": "Title of the pie chart.",
                "$ref": "#text",
            },
            "diameter": {
                "title": "Diameter of the pie chart.",
                "type": "number",
                "default": DEFAULT_DIAMETER,
                "exclusiveMinimum": 0,
            },
            "total": {
                "title": "Total value to relate slice values to.",
                "type": "number",
                "exclusiveMinimum": 0,
            },
            "start": {
                "title": "Starting point for first slice; in degrees from the top.",
                "type": "number",
            },
            "palette": {
                "title": "Palette for slice colors.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "title": "Color in palette.",
                    "type": "string",
                    "format": "color",
                },
                "default": constants.DEFAULT_PALETTE,
            },
            "entries": {
                "title": "Entries in the pie chart.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "oneOf": [
                        {
                            "title": "Slice in the pie chart.",
                            "type": "object",
                            "required": ["entry", "value"],
                            "additionalProperties": False,
                            "properties": {
                                "entry": {"const": "slice"},
                                "value": {
                                    "title": "The value visualized by the slice.",
                                    "type": "number",
                                    "exclusiveMinimum": 0,
                                },
                                "label": {
                                    "title": "Description of the value.",
                                    "type": "string",
                                },
                                "color": {
                                    "title": "Color of the slice. Palette used if not defined.",
                                    "type": "string",
                                    "format": "color",
                                },
                            },
                        },
                        # Sector
                    ],
                },
            },
        },
    }

    schema.add_defs(SCHEMA)

    def __init__(
        self,
        title=None,
        entries=None,
        diameter=None,
        total=None,
        start=None,
        palette=None,
    ):
        super().__init__(title=title, entries=entries)
        assert diameter is None or (isinstance(diameter, (int, float)) and diameter > 0)
        assert total is None or isinstance(total, (int, float))
        assert start is None or isinstance(start, (int, float))
        assert palette is None or isinstance(palette, (tuple, list))

        self.diameter = diameter or self.DEFAULT_DIAMETER
        self.total = total
        self.start = start
        # Create a copy of the palette, for safety and for YAML output.
        self.palette = list(palette or constants.DEFAULT_PALETTE)

    def convert_entry(self, entry):
        entry = super().convert_entry(entry)
        if not isinstance(entry, Slice):
            raise ValueError(f"invalid entry for piechart: {entry}; not a Slice")
        return entry

    def as_dict(self):
        result = super().as_dict()
        if self.diameter != self.DEFAULT_DIAMETER:
            result["diameter"] = self.diameter
        if self.total is not None:
            result["total"] = self.total
        if self.start is not None:
            result["start"] = self.start
        if self.palette != constants.DEFAULT_PALETTE:
            result["palette"] = self.palette
        return result

    def build(self):
        """Create the SVG elements in the 'svg' attribute. Adds the title, if given.
        Set the 'svg' and 'height' attributes.
        Sets the 'width' attribute from 'diameter' and padding.
        """
        # XXX add line width if and when implemented
        self.width = self.diameter + 2 * constants.DEFAULT_PADDING

        super().build()

        if self.total is None:
            total = sum([e.value for e in self.entries])
        else:
            total = self.total
        palette = itertools.cycle(self.palette)
        radius = self.diameter / 2
        x = radius + constants.DEFAULT_PADDING
        y = self.height + radius + constants.DEFAULT_PADDING
        self.height += self.diameter + 2 * constants.DEFAULT_PADDING

        self.svg += (
            pie := Element("g", transform=f"translate({utils.N(x)}, {utils.N(y)})")
        )
        pie += Element("circle", r=radius)

        # Prepare and create slices.
        if self.start is None:
            stop = self.DEFAULT_START
        else:
            stop = Degrees(self.start) + self.DEFAULT_START
        for entry in self.entries:
            entry.start = stop
            entry.fraction = entry.value / total
            entry.stop = entry.start + entry.fraction * Degrees(360)
            stop = entry.stop
        pie += (slices := Element("g", stroke="black"))
        slices["stroke-width"] = 1
        for entry in self.entries:
            slices += entry.render_graphic(radius, palette)

        # Labels on top of slices.
        pie += (labels := Element("g", stroke="none", fill="black"))
        labels["text-anchor"] = "middle"
        for entry in self.entries:
            if (label := entry.render_label(radius)):
                labels += label


class Slice(Entry):
    "A slice in a pie chart."

    def __init__(self, value, label=None, color=None):
        assert isinstance(value, (int, float))
        assert label is None or isinstance(label, str)
        assert color is None or isinstance(color, str)

        self.value = value
        self.label = label
        self.color = color

    def as_dict(self):
        result = super().as_dict()
        result["value"] = self.value
        if self.label:
            result["label"] = self.label
        if self.color:
            result["color"] = self.color
        return result

    def render_graphic(self, radius, palette):
        p0 = Vector2.from_polar(radius, float(self.start))
        p1 = Vector2.from_polar(radius, float(self.stop))
        lof = 1 if self.stop - self.start > Degrees(180) else 0
        result = Element(
            "path",
            d=Path(0, 0).L(p0.x, p0.y).A(radius, radius, 0, lof, 1, p1.x, p1.y).Z(),
        )
        if self.color:
            result["fill"] = self.background = self.color
        else:
            result["fill"] = self.background = next(palette)
        return result

    def render_label(self, radius):
        if not self.label:
            return
        middle = self.start + 0.5 * self.fraction * Degrees(360)
        pos = Vector2.from_polar(0.7 * radius, float(middle))
        result = Element("text", self.label, x=utils.N(pos.x), y=utils.N(pos.y))
        result["fill"] = Color(self.background).best_contrast
        return result
