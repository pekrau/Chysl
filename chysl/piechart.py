"Pie chart displaying slices."

__all__ = ["Piechart", "Slice"]

import itertools

import components
import constants
import schema
import utils
from color import Color
from degrees import Degrees
from chart import Chart, Layout, register
from minixml import Element
from path import Path
from utils import N
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
                "title": "Title of the chart.",
                "$ref": "#text",
            },
            "description": {
                "title": "Description of the chart. Rendered as <desc> in SVG.",
                "type": "string",
            },
            "diameter": {
                "title": "Diameter of the pie chart.",
                "type": "number",
                "default": DEFAULT_DIAMETER,
                "exclusiveMinimum": 0,
            },
            "frame": {
                "title": "Specification of the piechart perimeter.",
                "$ref": "#frame",
            },
            "total": {
                "title": "Sum total x value to relate slice x values to.",
                "type": "number",
                "exclusiveMinimum": 0,
            },
            "start": {
                "title": "Starting point for first slice; in degrees from the top.",
                "type": "number",
            },
            "palette": {
                "title": "Palette used for slices lacking explicit color specification.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "title": "Color entry in the palette.",
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
                    "required": ["x"],
                    "additionalProperties": False,
                    "properties": {
                        "x": {
                            "title": "The value visualized by the slice.",
                            "type": "number",
                            "exclusiveMinimum": 0,
                        },
                        "label": {
                            "title": "Description of the x value.",
                            "type": "string",
                        },
                        "color": {
                            "title": "Color of the slice. Overrides the palette.",
                            "type": "string",
                            "format": "color",
                        },
                        "href": {
                            "title": "A link URL, absolute or relative.",
                            "type": "string",
                            "format": "uri-reference",
                        },
                    },
                },
            },
        },
    }

    schema.add_defs(SCHEMA)

    def __init__(
        self,
        title=None,
        description=None,
        diameter=None,
        frame=True,
        total=None,
        start=None,
        palette=None,
        slices=None,
    ):
        super().__init__(title=title, description=description)
        assert diameter is None or (isinstance(diameter, (int, float)) and diameter > 0)
        assert isinstance(frame, (bool, dict))
        assert total is None or isinstance(total, (int, float))
        assert start is None or isinstance(start, (int, float))
        assert palette is None or isinstance(palette, (tuple, list))
        assert slices is None or isinstance(slices, list)

        self.diameter = diameter or self.DEFAULT_DIAMETER
        self.frame = components.CircularFrame(frame)
        self.total = total
        self.start = start
        # Create a copy of the palette, just in case.
        self.palette = list(palette or constants.DEFAULT_PALETTE)
        self.slices = []
        if slices:
            for slice in slices:
                self.add(slice)

    def __iadd__(self, slice):
        self.add(slice)
        return self

    def add(self, slice):
        assert isinstance(slice, (dict, Slice))
        if isinstance(slice, dict):
            slice = Slice(**slice)
        assert isinstance(slice, Slice)
        self.slices.append(slice)

    def as_dict(self):
        result = super().as_dict()
        if self.diameter != self.DEFAULT_DIAMETER:
            result["diameter"] = self.diameter
        result.update(self.frame.as_dict())
        if self.total is not None:
            result["total"] = self.total
        if self.start is not None:
            result["start"] = self.start
        if self.palette != constants.DEFAULT_PALETTE:
            result["palette"] = self.palette
        result["slices"] = slices = []
        for slice in self.slices:
            slices.append(slice.as_dict())
        return result

    def build(self):
        "Create the SVG elements in the 'svg' attribute."
        super().build()
        layout = Layout(rows=1, columns=1, title=self.title)
        layout.add(0, 0, self.get_plot())
        self.svg.load_layout(layout)

    def get_plot(self):
        "Get the element for the chart circle (frame) and slices."
        if self.total is None:
            total = sum([s.x for s in self.slices])
        else:
            total = self.total
        palette = itertools.cycle(self.palette)
        radius = self.diameter / 2

        result = Element("g")
        result["class"] = "plot"
        clippath_id = next(utils.unique_id)
        result["clip-path"] = f"url(#{clippath_id})"
        result.total_width = self.diameter
        result.total_height = self.diameter

        if self.frame:
            result += self.frame.get_element(self.diameter)
            result.total_width += 2 * self.frame.thickness
            result.total_height += 2 * self.frame.thickness

        # Clip path definition. Yes, can be added as part of the result.
        result += Element(
            "defs",
            Element(
                "clipPath",
                Element(
                    "rect",
                    x=N(-result.total_width / 2),
                    y=N(-result.total_height / 2),
                    width=N(result.total_width),
                    height=N(result.total_height),
                    id=clippath_id,
                ),
            ),
        )

        # Prepare and create slices.
        if self.start is None:
            stop = self.DEFAULT_START
        else:
            stop = Degrees(self.start) + self.DEFAULT_START
        for slice in self.slices:
            slice.start = stop
            slice.fraction = slice.x / total
            slice.stop = slice.start + slice.fraction * Degrees(360)
            stop = slice.stop

        result += (graphics := Element("g"))
        graphics["class"] = "graphics"
        graphics += Element("circle", r=radius, fill="white")
        for slice in self.slices:
            graphics += slice.render_graphic(radius, palette)

        # Labels on top of slices.
        result += (labels := Element("g"))
        labels["class"] = "labels"
        labels["font-family"] = constants.DEFAULT_FONT_FAMILY
        labels["font-size"] = constants.DEFAULT_FONT_SIZE
        labels["text-anchor"] = "middle"
        for slice in self.slices:
            if label := slice.render_label(radius):
                labels += label

        # Move pie to (0, 0, total_width, total_height).
        result["transform"] = (
            f"translate({N(result.total_width/2)},{N(result.total_height/2)})"
        )
        return result


register(Piechart)


class Slice:
    "Slice in a pie chart."

    def __init__(self, x, label=None, color=None, href=None):
        assert isinstance(x, (int, float)) and x > 0
        assert label is None or isinstance(label, str)
        assert color is None or (isinstance(color, str) and utils.is_color(color))
        assert href is None or isinstance(href, str)

        self.x = x
        self.label = label
        self.color = color
        self.href = href

    def as_dict(self):
        result = {"x": self.x}
        if self.label:
            result["label"] = self.label
        if self.color:
            result["color"] = self.color
        if self.href:
            result["href"] = self.href
        return result

    def render_graphic(self, radius, palette):
        p0 = Vector2.from_polar(radius, float(self.start))
        p1 = Vector2.from_polar(radius, float(self.stop))
        lof = 1 if self.stop - self.start > Degrees(180) else 0
        result = Element(
            "path",
            d=Path(0, 0).L(p0.x, p0.y).A(radius, radius, 0, lof, 1, p1.x, p1.y).Z(),
        )
        result["class"] = "slice"
        if self.color:
            result["fill"] = self.background = self.color
        else:
            result["fill"] = self.background = next(palette)
        if self.href:
            result = Element("a", result, href=self.href)
        return result

    def render_label(self, radius):
        if not self.label:
            return None
        middle = self.start + 0.5 * self.fraction * Degrees(360)
        # Empirical factor 0.7
        pos = Vector2.from_polar(0.7 * radius, float(middle))
        return Element(
            "text",
            self.label,
            x=N(pos.x),
            y=N(pos.y),
            fill=Color(self.background).best_contrast,
        )
