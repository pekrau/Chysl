"2D scatter chart."

import constants
import schema
import utils
from chart import Chart, register
from datapoints import DatapointsReader
from dimension import Xdimension, Ydimension
from marker import Marker
from minixml import Element
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
            "title": {"$ref": "#title"},
            "description": {"$ref": "#description"},
            "width": {
                "title": "Width of the chart, including legends etc.",
                "type": "number",
                "default": constants.DEFAULT_WIDTH,
                "exclusiveMinimum": 0,
            },
            "height": {
                "title": "Height of the chart, including legends etc.",
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
            "xgrid": {
                "title": "X grid specification.",
                "$ref": "#grid",
            },
            "ygrid": {
                "title": "Y grid specification.",
                "$ref": "#grid",
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
                "default": "black",
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
        description=None,
        points=None,
        width=None,
        height=None,
        xaxis=None,
        yaxis=None,
        xgrid=None,
        ygrid=None,
        marker=None,
        size=None,
        color=None,
        opacity=None,
    ):
        super().__init__(title=title, description=description)
        assert width is None or (isinstance(width, (int, float)) and width > 0)
        assert height is None or (isinstance(height, (int, float)) and height > 0)
        assert xaxis is None or isinstance(xaxis, (bool, dict))
        assert yaxis is None or isinstance(yaxis, (bool, dict))
        assert xgrid is None or isinstance(xgrid, (bool, dict))
        assert ygrid is None or isinstance(ygrid, (bool, dict))
        assert marker is None or marker in constants.MARKERS
        assert size is None or (isinstance(size, (int, float)) and size > 0)
        assert color is None or utils.is_color(color)
        assert opacity is None or (
            isinstance(opacity, (int, float)) and (0 <= opacity <= 1)
        )

        self.points = DatapointsReader(points)
        self.width = width or constants.DEFAULT_WIDTH
        self.total_height = height or constants.DEFAULT_WIDTH
        self.xaxis = True if xaxis is None else xaxis
        self.yaxis = True if yaxis is None else yaxis
        self.xgrid = True if xgrid is None else xgrid
        self.ygrid = True if ygrid is None else ygrid
        self.marker = marker or constants.DEFAULT_MARKER
        self.size = size or constants.DEFAULT_MARKER_SIZE
        self.color = color or "black"
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
        if self.xgrid is False or isinstance(self.xgrid, dict):
            result["xgrid"] = self.xgrid
        if self.ygrid is False or isinstance(self.ygrid, dict):
            result["ygrid"] = self.ygrid
        if self.marker != constants.DEFAULT_MARKER:
            result["marker"] = self.marker
        if self.size != constants.DEFAULT_MARKER_SIZE:
            result["size"] = self.size
        if self.color != "black":
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
        self.points.check_required("x", "y")

        super().build()

        # Determine dimensions for the axes.
        xdimension = Xdimension(width=self.width)
        xdimension.update_span(self.points.minmax("x"))
        xdimension.expand_span(0.05)

        ydimension = Ydimension(width=self.width, reversed=True)
        ydimension.update_span(self.points.minmax("y"))
        ydimension.expand_span(0.05)
        ydimension.update_end(self.total_height)

        # Y dimension has to be built first; label lengths needed for adjusting x.
        if isinstance(self.yaxis, dict):
            ydimension.build(
                ticks=self.yaxis.get("ticks") or constants.DEFAULT_TICKS_TARGET,
                min=self.yaxis.get("min"),
                max=self.yaxis.get("max"),
                labels=self.yaxis.get("labels", True),
                factor=self.yaxis.get("factor"),
                absolute=bool(self.yaxis.get("absolute")),
            )
            ywidth = self.yaxis.get("width")
        else:
            ydimension.build()
            ywidth = None

        if (isinstance(self.yaxis, bool) and self.yaxis) or self.yaxis.get(
            "labels", True
        ):
            if ywidth is not None:
                xdimension.update_start(ywidth)
            else:
                xdimension.update_start(
                    ydimension.get_label_length(constants.DEFAULT_FONT_SIZE)
                    + constants.DEFAULT_PADDING
                )

        xdimension.update_end(constants.DEFAULT_PADDING)
        if isinstance(self.xaxis, dict):
            xdimension.build(
                ticks=self.xaxis.get("ticks") or constants.DEFAULT_TICKS_TARGET,
                min=self.xaxis.get("min"),
                max=self.xaxis.get("max"),
                labels=self.xaxis.get("labels", True),
                factor=self.xaxis.get("factor"),
                absolute=bool(self.xaxis.get("absolute")),
            )
        else:
            xdimension.build()

        # Chart area.
        xpxlow = xdimension.get_pixel(xdimension.first)
        xpxhigh = xdimension.get_pixel(xdimension.last)
        ypxlow = self.total_height
        self.total_height += self.width - self.total_height
        ypxhigh = self.total_height

        # X coordinate grid.
        if self.xgrid:
            if isinstance(self.xgrid, dict):
                color = self.xgrid.get("color") or constants.DEFAULT_GRID_COLOR
            else:
                color = constants.DEFAULT_GRID_COLOR
            self.svg += xdimension.get_grid(ypxlow, ypxhigh, color)

        # Y coordinate grid.
        if self.ygrid:
            if isinstance(self.ygrid, dict):
                color = self.ygrid.get("color") or constants.DEFAULT_GRID_COLOR
            else:
                color = constants.DEFAULT_GRID_COLOR
            self.svg += ydimension.get_grid(xpxlow, xpxhigh, color)

        # Chart frame; overwrite the grid.
        self.svg += xdimension.get_frame(
            ypxlow,
            ypxhigh,
            color="black",
            linewidth=constants.DEFAULT_FRAME_WIDTH,
        )

        # X axis labels.
        if self.xaxis:
            if isinstance(self.xaxis, dict):
                caption = self.xaxis.get("caption")
            else:
                caption = None
            self.svg += (xaxis := Element("g"))
            xaxis += (
                labels := xdimension.get_labels(ypxhigh, constants.DEFAULT_FONT_SIZE)
            )
            if len(labels) > 0:
                self.total_height += constants.DEFAULT_FONT_SIZE * (
                    1 + constants.FONT_DESCEND
                )

            # X axis caption.
            if isinstance(self.xaxis, dict) and (caption := self.xaxis.get("caption")):
                self.total_height += constants.DEFAULT_FONT_SIZE
                labels += Element(
                    "text",
                    caption,
                    x=utils.N(
                        xdimension.get_pixel((xdimension.first + xdimension.last) / 2)
                    ),
                    y=utils.N(self.total_height),
                )
            self.total_height += constants.DEFAULT_FONT_SIZE * constants.FONT_DESCEND

        # Y axis labels.
        if self.yaxis:
            if isinstance(self.yaxis, dict):
                caption = self.yaxis.get("caption")
            else:
                caption = None
            self.svg += (yaxis := Element("g"))
            yaxis += (
                labels := ydimension.get_labels(xpxlow, constants.DEFAULT_FONT_SIZE)
            )

        # Graphics area clipping.
        clippath_id, clippath_def = xdimension.get_clippath(ypxlow, ypxhigh)
        self.svg += clippath_def
        self.svg += (graphics := Element("g"))
        graphics["clip-path"] = f"url(#{clippath_id})"

        # Graphics for points.
        for datapoint in self.points:
            kwargs = {}
            if (opacity := datapoint.get("opacity")) is None:
                opacity = self.opacity
            if opacity != 1:
                kwargs["opacity"] = opacity
            if href := datapoint.get("href"):
                kwargs["href"] = href
            marker = Marker(
                datapoint.get("marker") or self.marker,
                size=datapoint.get("size") or self.size,
                color=datapoint.get("color") or self.color,
                **kwargs,
            )
            graphics += marker.get_graphic(
                xdimension.get_pixel(datapoint["x"]),
                ydimension.get_pixel(datapoint["y"]),
            )
            datapoint["label_x_offset"] = marker.label_x_offset

        # Labels for points.
        labels = Element("g")
        labels["stroke"] = "none"
        labels["fill"] = "black"
        labels["text-anchor"] = "start"
        labels["font-size"] = constants.DEFAULT_FONT_SIZE
        for datapoint in self.points:
            if label := datapoint.get("label"):
                labels += Element(
                    "text",
                    label,
                    x=xdimension.get_pixel(datapoint["x"])
                    + datapoint["label_x_offset"]
                    + constants.DEFAULT_PADDING,
                    y=ydimension.get_pixel(datapoint["y"])
                    + constants.DEFAULT_FONT_SIZE / 2,
                )
        if len(labels) > 0:
            self.svg += labels


register(Scatter2d)
