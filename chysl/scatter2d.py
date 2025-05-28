"2D scatter chart."

import constants
import schema
import utils
from chart import Chart, Entry, DatapointsReader, Element
from dimension import Dimension
from marker import Marker
from path import Path
from utils import N


class Scatter2d(Chart):
    "2D scatter chart."

    DEFAULT_WIDTH = 600
    DEFAULT_MARKER = constants.DISC
    DEFAULT_SIZE = constants.DEFAULT_MARKER_SIZE
    DEFAULT_COLOR = "black"

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "points"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "scatter2d"},
            "title": {
                "title": "Title of the plot.",
                "$ref": "#text",
            },
            "width": {
                "title": "Width of the chart, including legends etc.",
                "type": "number",
                "default": DEFAULT_WIDTH,
                "exclusiveMinimum": 0,
            },
            "xaxis": {
                "title": "X axis specification.",
                "$ref": "#axis",
            },
            "yaxis": {
                "title": "Y axis specification.",
                "$ref": "#axis",
            },
            "marker": {
                "title": "Default marker.",
                "$ref": "#marker",
                "default": DEFAULT_MARKER,
            },
            "size": {
                "title": "Default size.",
                "$ref": "#size",
                "default": DEFAULT_SIZE,
            },
            "color": {
                "title": "Default color",
                "$ref": "#color",
                "default": DEFAULT_COLOR,
            },
            "opacity": {
                "title": "Default opacity.",
                "$ref": "#opacity",
            },
            "points": {
                "title": "A container of 2D points to display as markers.",
                "$ref": "#datapoints",
            },
        },
    }

    schema.add_defs(SCHEMA)

    def __init__(
        self,
        title=None,
        points=None,
        width=None,
        xaxis=None,
        yaxis=None,
        marker=None,
        size=None,
        color=None,
        opacity=None,
    ):
        super().__init__(title=title)
        assert width is None or (isinstance(width, (int, float)) and width > 0)
        assert xaxis is None or isinstance(xaxis, (bool, dict))
        assert yaxis is None or isinstance(yaxis, (bool, dict))
        assert marker is None or marker in constants.MARKERS
        assert size is None or (isinstance(size, (int, float)) and size > 0)
        assert color is None or utils.is_color(color)
        assert opacity is None or (
            isinstance(opacity, (int, float)) and (0 <= opacity <= 1)
        )

        self.points = DatapointsReader(points, required=["x", "y"])
        self.width = width or self.DEFAULT_WIDTH
        self.xaxis = True if xaxis is None else xaxis
        self.yaxis = True if yaxis is None else yaxis
        self.marker = marker or self.DEFAULT_MARKER
        self.size = size or self.DEFAULT_SIZE
        self.color = color or self.DEFAULT_COLOR
        self.opacity = opacity

    def append(self, point):
        self.points.append(point)

    def as_dict(self):
        result = super().as_dict()
        if self.width != self.DEFAULT_WIDTH:
            result["width"] = self.width
        if self.xaxis is False or isinstance(self.xaxis, dict):
            result["xaxis"] = self.xaxis
        if self.yaxis is False or isinstance(self.yaxis, dict):
            result["yaxis"] = self.yaxis
        if self.marker != self.DEFAULT_MARKER:
            result["marker"] = self.marker
        if self.size != self.DEFAULT_SIZE:
            result["size"] = self.size
        if self.color != self.DEFAULT_COLOR:
            result["color"] = self.color
        if self.opacity is not None and self.opacity != 1:
            result["opacity"] = self.opacity
        result["points"] = self.points.as_dict()
        return result

    def build(self):
        """Create the SVG elements in the 'svg' attribute. Adds the title, if given.
        Set the 'svg' and 'height' attributes.
        Requires the 'width' attribute.
        """
        super().build()

        # Determine dimensions for the axes.
        xdimension = Dimension(width=self.width)
        ydimension = Dimension(width=self.width, reversed=True)
        xdimension.update_span(self.points.minmax("x"))
        ydimension.update_span(self.points.minmax("y"))
        xdimension.expand_span(0.05)
        ydimension.expand_span(0.05)
        ydimension.update_end(self.height)
        # XXX This is a kludge, assuming legend label is two characters wide.
        xdimension.update_start(
            utils.get_text_length(
                "99", constants.DEFAULT_FONT_FAMILY, self.DEFAULT_FONT_SIZE
            )
            + constants.DEFAULT_PADDING
        )
        xdimension.update_end(constants.DEFAULT_PADDING)
        if isinstance(self.xaxis, dict):
            absolute = bool(self.xaxis.get("absolute"))
        else:
            absolute = False
        xdimension.build(absolute=absolute)
        if isinstance(self.yaxis, dict):
            absolute = bool(self.yaxis.get("absolute"))
        else:
            absolute = False
        ydimension.build(absolute=absolute)

        self.height += self.width - self.height

        # X axis grid and its labels.
        if self.xaxis:
            if isinstance(self.xaxis, dict):
                color = self.xaxis.get("color") or "gray"
                caption = self.xaxis.get("caption")
            else:
                color = "gray"
                caption = None
            self.svg += (xaxis := Element("g"))
            ticks = xdimension.ticks
            top = ydimension.get_pixel(ydimension.first)
            bottom = ydimension.get_pixel(ydimension.last)
            path = Path(ticks[0].pixel, top).V(bottom)
            for tick in ticks[1:]:
                path.M(tick.pixel, top).V(bottom)
            xaxis += Element("path", d=path, stroke=color)

            xaxis += (labels := Element("g"))
            labels["text-anchor"] = "middle"
            labels["stroke"] = "none"
            labels["fill"] = "black"
            self.height += self.DEFAULT_FONT_SIZE
            for tick in ticks:
                labels += (
                    label := Element(
                        "text",
                        tick.label,
                        x=N(tick.pixel),
                        y=N(self.height),
                    )
                )
                if tick is ticks[0]:
                    label["text-anchor"] = "start"
                elif tick is ticks[-1]:
                    label["text-anchor"] = "end"
            self.height += self.DEFAULT_FONT_SIZE * constants.FONT_DESCEND

        # Y axis grid and its labels.
        if self.yaxis:
            if isinstance(self.yaxis, dict):
                color = self.yaxis.get("color") or "gray"
                caption = self.yaxis.get("caption")
            else:
                color = "gray"
                caption = None
            self.svg += (yaxis := Element("g"))
            ticks = ydimension.ticks
            start = xdimension.get_pixel(xdimension.first)
            end = xdimension.get_pixel(xdimension.last)
            path = Path(start, ticks[0].pixel)
            path.H(end)
            for tick in ticks[1:]:
                path.M(start, tick.pixel).H(end)
            yaxis += Element("path", d=path, stroke=color)

            yaxis += (labels := Element("g"))
            labels["text-anchor"] = "end"
            labels["stroke"] = "none"
            labels["fill"] = "black"
            for tick in ticks:
                labels += (
                    label := Element(
                        "text",
                        tick.label,
                        x=N(xdimension.start - constants.DEFAULT_PADDING),
                        y=N(tick.pixel + self.DEFAULT_FONT_SIZE / 3),
                    )
                )
                if tick is ticks[0]:
                    label["y"] = N(tick.pixel)
                elif tick is ticks[-1]:
                    label["y"] = N(tick.pixel + self.DEFAULT_FONT_SIZE)

        # Graphics for points.
        self.svg += (points := Element("g"))
        for dp in self.points:
            if (opacity := dp.get("opacity")) is None:
                opacity = self.opacity
            if opacity != 1:
                kwargs = dict(opacity=opacity)
            else:
                kwargs = {}
            marker = Marker(
                dp.get("marker") or self.marker,
                size=dp.get("size") or self.size,
                color=dp.get("color") or self.color,
                **kwargs,
            )
            points += marker.get_graphic(
                xdimension.get_pixel(dp["x"]), ydimension.get_pixel(dp["y"])
            )
