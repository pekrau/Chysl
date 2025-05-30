"Pie chart displaying slices."

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
    "Pie chart displaying slices."

    DEFAULT_DIAMETER = 200
    DEFAULT_START = Degrees(-90)

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "slices"],
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
                "title": "Palette for slice colors; used for slices lacking color specification.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "title": "Color in palette.",
                    "type": "string",
                    "format": "color",
                },
                "default": constants.DEFAULT_PALETTE,
            },
            "slices": {
                "title": "Slices in the pie chart.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "title": "Slice in the pie chart.",
                    "type": "object",
                    "required": ["value"],
                    "additionalProperties": False,
                    "properties": {
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
                            "title": "Color of the slice.",
                            "$ref": "#color",
                        },
                        "href": {"$ref": "#uri"},
                    },
                },
            },
        },
    }

    schema.add_defs(SCHEMA)

    def __init__(
        self,
        title=None,
        slices=None,
        diameter=None,
        total=None,
        start=None,
        palette=None,
    ):
        super().__init__(title=title)
        assert slices is None or isinstance(slices, list)
        assert diameter is None or (isinstance(diameter, (int, float)) and diameter > 0)
        assert total is None or isinstance(total, (int, float))
        assert start is None or isinstance(start, (int, float))
        assert palette is None or isinstance(palette, (tuple, list))

        self.slices = []
        if slices:
            for slice in slices:
                self.add(slice)
        self.diameter = diameter or self.DEFAULT_DIAMETER
        self.total = total
        self.start = start
        # Create a copy of the palette, for safety and for YAML output.
        self.palette = list(palette or constants.DEFAULT_PALETTE)

    def __iadd__(self, slice):
        self.add(slice)
        return self

    def add(self, slice):
        assert isinstance(slice, dict)

        self.add_slice(*[slice.get(key) for key in ["value", "label", "color", "href"]])

    def add_slice(self, value, label=None, color=None, href=None):
        assert isinstance(value, (int, float)) and value > 0
        assert label is None or isinstance(label, str)
        assert color is None or utils.is_color(color)
        assert href is None or isinstance(href, str)

        self.slices.append(dict(value=value, color=color, label=label, href=href))

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
        result["slices"] = slices = []
        for slice in self.slices:
            slices.append(s := dict(value=slice["value"]))
            if label := slice.get("label"):
                s["label"] = label
            if color := slice.get("color"):
                s["color"] = color
            if href := slice.get("href"):
                s["href"] = href
        return result

    def build(self):
        """Create the SVG elements in the 'svg' attribute.
        Adds the title, if defined.
        Sets the 'svg' and 'height' attributes.
        Sets the 'width' attribute from 'diameter' and padding.
        """
        # XXX add line width if and when implemented
        self.width = self.diameter + 2 * constants.DEFAULT_PADDING

        super().build()

        if self.total is None:
            total = sum([s["value"] for s in self.slices])
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
        # XXX linewidth
        pie += Element("circle", r=radius)

        # Prepare and create slices.
        if self.start is None:
            stop = self.DEFAULT_START
        else:
            stop = Degrees(self.start) + self.DEFAULT_START
        for slice in self.slices:
            slice["start"] = stop
            slice["fraction"] = slice["value"] / total
            slice["stop"] = slice["start"] + slice["fraction"] * Degrees(360)
            stop = slice["stop"]
        pie += (slices := Element("g", stroke="black"))
        # XXX linewidth
        slices["stroke-width"] = 1

        for slice in self.slices:
            p0 = Vector2.from_polar(radius, float(slice["start"]))
            p1 = Vector2.from_polar(radius, float(slice["stop"]))
            lof = 1 if slice["stop"] - slice["start"] > Degrees(180) else 0
            elem = Element(
                "path",
                d=Path(0, 0).L(p0.x, p0.y).A(radius, radius, 0, lof, 1, p1.x, p1.y).Z(),
            )
            if color := slice.get("color"):
                elem["fill"] = slice["background"] = color
            else:
                elem["fill"] = slice["background"] = next(palette)
            if href := slice.get("href"):
                elem = Element("a", elem, href=href)
            slices += elem

        # Labels on top of slices.
        pie += (labels := Element("g", stroke="none", fill="black"))
        labels["text-anchor"] = "middle"

        for slice in self.slices:
            if label := slice.get("label"):
                middle = slice["start"] + 0.5 * slice["fraction"] * Degrees(360)
                pos = Vector2.from_polar(0.7 * radius, float(middle))
                labels += Element(
                    "text",
                    label,
                    x=utils.N(pos.x),
                    y=utils.N(pos.y),
                    fill=Color(slice["background"]).best_contrast,
                )
