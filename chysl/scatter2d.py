"2D scatter chart."

import constants
import schema
import utils
from chart import Chart, Entry, Element
from datapoints import DatapointsReader
from dimension import Xdimension, Ydimension
from marker import Marker
from path import Path
from utils import N


class Scatter2d(Chart):
    "2D scatter chart."

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
                "default": constants.DEFAULT_WIDTH,
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
                "default": constants.DEFAULT_MARKER,
            },
            "size": {
                "title": "Default size.",
                "$ref": "#size",
                "default": constants.DEFAULT_MARKER_SIZE,
            },
            "color": {
                "title": "Default color.",
                "$ref": "#color",
                "default": constants.DEFAULT_COLOR,
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
        self.width = width or constants.DEFAULT_WIDTH
        self.xaxis = True if xaxis is None else xaxis
        self.yaxis = True if yaxis is None else yaxis
        self.marker = marker or constants.DEFAULT_MARKER
        self.size = size or constants.DEFAULT_MARKER_SIZE
        self.color = color or constants.DEFAULT_COLOR
        self.opacity = opacity

    def __iadd__(self, point):
        self.add(point)
        return self

    def add(self, point):
        self.points.add(point)

    def as_dict(self):
        result = super().as_dict()
        if self.width != constants.DEFAULT_WIDTH:
            result["width"] = self.width
        if self.xaxis is False or isinstance(self.xaxis, dict):
            result["xaxis"] = self.xaxis
        if self.yaxis is False or isinstance(self.yaxis, dict):
            result["yaxis"] = self.yaxis
        if self.marker != constants.DEFAULT_MARKER:
            result["marker"] = self.marker
        if self.size != constants.DEFAULT_MARKER_SIZE:
            result["size"] = self.size
        if self.color != constants.DEFAULT_COLOR:
            result["color"] = self.color
        if self.opacity is not None and self.opacity != 1:
            result["opacity"] = self.opacity
        result["points"] = self.points.as_dict()
        return result

    def build(self):
        """Create the SVG elements in the 'svg' attribute.
        Adds the title, if defined.
        Set the 'svg' and 'height' attributes.
        Requires the 'width' attribute.
        """
        super().build()

        # Determine dimensions for the axes.
        xdimension = Xdimension(width=self.width)
        ydimension = Ydimension(width=self.width, reversed=True)
        xdimension.update_span(self.points.minmax("x"))
        ydimension.update_span(self.points.minmax("y"))
        xdimension.expand_span(0.05)
        ydimension.expand_span(0.05)
        ydimension.update_end(self.height)

        # Y dimension has to be built first; label lengths needed for adjusting x.
        if isinstance(self.yaxis, dict):
            absolute = bool(self.yaxis.get("absolute"))
        else:
            absolute = False
        ydimension.build(absolute=absolute)

        xdimension.update_start(
            ydimension.get_label_length(constants.DEFAULT_FONT_SIZE)
            + constants.DEFAULT_PADDING
        )

        xdimension.update_end(constants.DEFAULT_PADDING)
        if isinstance(self.xaxis, dict):
            absolute = bool(self.xaxis.get("absolute"))
        else:
            absolute = False
        xdimension.build(absolute=absolute)

        ypxlow = self.height
        self.height += self.width - self.height
        ypxhigh = self.height

        # Chart frame.
        self.svg += xdimension.get_frame(
            ypxlow,
            ypxhigh,
            color=constants.DEFAULT_COLOR,
            linewidth=constants.DEFAULT_FRAME_WIDTH,
        )

        # X axis: grid and labels.
        if self.xaxis:
            if isinstance(self.xaxis, dict):
                color = self.xaxis.get("color") or "gray"
                caption = self.xaxis.get("caption")
            else:
                color = "gray"
                caption = None
            self.svg += (xaxis := Element("g"))
            xaxis += xdimension.get_grid(ypxlow, ypxhigh, color)
            xaxis += (
                labels := xdimension.get_labels(ypxhigh, constants.DEFAULT_FONT_SIZE)
            )
            self.height += constants.DEFAULT_FONT_SIZE * (1 + constants.FONT_DESCEND)

        # Y axis grid and its labels.
        if self.yaxis:
            if isinstance(self.yaxis, dict):
                color = self.yaxis.get("color") or "gray"
                caption = self.yaxis.get("caption")
            else:
                color = "gray"
                caption = None
            self.svg += (yaxis := Element("g"))
            start = xdimension.get_pixel(xdimension.first)
            end = xdimension.get_pixel(xdimension.last)
            yaxis += ydimension.get_grid(start, end, color)
            yaxis += (
                labels := ydimension.get_labels(start, constants.DEFAULT_FONT_SIZE)
            )

        # Graphics for points.
        clippath_id, clippath_def = xdimension.get_clippath(ypxlow, ypxhigh)
        self.svg += clippath_def
        self.svg += (graphics := Element("g"))
        graphics["clip-path"] = f"url(#{clippath_id})"
        for dp in self.points:
            kwargs = {}
            if (opacity := dp.get("opacity")) is None:
                opacity = self.opacity
            if opacity != 1:
                kwargs["opacity"] = opacity
            if href := dp.get("href"):
                kwargs["href"] = href
            marker = Marker(
                dp.get("marker") or self.marker,
                size=dp.get("size") or self.size,
                color=dp.get("color") or self.color,
                **kwargs,
            )
            graphics += marker.get_graphic(
                xdimension.get_pixel(dp["x"]), ydimension.get_pixel(dp["y"])
            )
