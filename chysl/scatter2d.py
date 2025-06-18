"2D scatter chart."

import components
import constants
import schema
import utils
from chart import Chart, Layout, register
from datapoints import DatapointsReader
from dimension import Xdimension, Ydimension
from marker import Marker
from minixml import Element
from path import Path
from utils import N


class Scatter2d(Chart):
    "2D scatter chart."

    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600
    DEFAULT_MARKER = "disc"
    DEFAULT_SIZE = 10
    DEFAULT_COLOR = "black"
    PADDING = 2

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "points"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "scatter2d"},
            "title": {
                "title": "Title of the chart.",
                "$ref": "#text",
            },
            "description": {
                "title": "Description of the chart. Rendered as <desc> in SVG.",
                "type": "string",
            },
            "points": {
                "title": "The list of 2D points to display by markers.",
                "$ref": "#datapoints",
            },
            "width": {
                "title": "Width of the chart.",
                "type": "number",
                "default": DEFAULT_WIDTH,
                "exclusiveMinimum": 0,
            },
            "height": {
                "title": "Height of the chart.",
                "type": "number",
                "default": DEFAULT_HEIGHT,
                "exclusiveMinimum": 0,
            },
            "frame": {
                "title": "Chart area frame specification.",
                "$ref": "#frame",
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
                "default": DEFAULT_MARKER,
            },
            "size": {
                "title": "Default size of the markers (pixels).",
                "type": "number",
                "minimumExclusive": 0,
                "default": DEFAULT_SIZE,
            },
            "color": {
                "title": "Default marker color.",
                "type": "string",
                "format": "color",
                "default": DEFAULT_COLOR,
            },
            "opacity": {
                "title": "Default marker opacity.",
                "type": "number",
                "minimum": 0,
                "maximum": 1,
                "default": 1,
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
        frame=True,
        xaxis=True,
        yaxis=True,
        xgrid=True,
        ygrid=True,
        marker=None,
        size=None,
        color=None,
        opacity=None,
    ):
        super().__init__(title=title, description=description)
        assert width is None or (isinstance(width, (int, float)) and width > 0)
        assert height is None or (isinstance(height, (int, float)) and height > 0)
        assert isinstance(frame, (bool, dict))
        assert isinstance(xaxis, (bool, dict))
        assert isinstance(yaxis, (bool, dict))
        assert isinstance(xgrid, (bool, dict))
        assert isinstance(ygrid, (bool, dict))
        assert marker is None or marker in constants.MARKERS
        assert size is None or (isinstance(size, (int, float)) and size > 0)
        assert color is None or utils.is_color(color)
        assert opacity is None or (
            isinstance(opacity, (int, float)) and (0 <= opacity <= 1)
        )

        self.points = DatapointsReader(points)
        self.width = width or self.DEFAULT_WIDTH
        self.height = height or self.DEFAULT_HEIGHT
        self.frame = components.Frame(frame)
        self.xaxis = xaxis
        self.yaxis = yaxis
        self.xgrid = xgrid
        self.ygrid = ygrid
        self.marker = marker or self.DEFAULT_MARKER
        self.size = size or self.DEFAULT_SIZE
        self.color = color or self.DEFAULT_COLOR
        self.opacity = 1 if opacity is None else opacity

    def __iadd__(self, point):
        self.add(point)
        return self

    def add(self, point):
        self.points.add(point)

    def as_dict(self):
        result = super().as_dict()
        if self.width != self.DEFAULT_WIDTH:
            result["width"] = self.width
        if self.height != self.DEFAULT_HEIGHT:
            result["height"] = self.height
        result.update(self.frame.as_dict())
        if self.xaxis is False or isinstance(self.xaxis, dict):
            result["xaxis"] = self.xaxis
        if self.yaxis is False or isinstance(self.yaxis, dict):
            result["yaxis"] = self.yaxis
        if self.xgrid is False or isinstance(self.xgrid, dict):
            result["xgrid"] = self.xgrid
        if self.ygrid is False or isinstance(self.ygrid, dict):
            result["ygrid"] = self.ygrid
        if self.marker != self.DEFAULT_MARKER:
            result["marker"] = self.marker
        if self.size != self.DEFAULT_SIZE:
            result["size"] = self.size
        if self.color != self.DEFAULT_COLOR:
            result["color"] = self.color
        if self.opacity != 1:
            result["opacity"] = self.opacity
        result["points"] = self.points.as_dict()
        return result

    def build(self):
        "Create the SVG elements in the 'svg' attribute."
        super().build()

        self.points.check_required("x", "y")

        xdimension = Xdimension(self.width, self.xaxis)
        xdimension.update_span(self.points.minmax("x"))
        xdimension.expand_span(0.05)
        xdimension.build()

        ydimension = Ydimension(self.height, self.yaxis, reversed=True)
        ydimension.update_span(self.points.minmax("y"))
        ydimension.expand_span(0.05)
        ydimension.build()

        layout = Layout(rows=2, columns=2, title=self.title)
        layout.add(0, 0, ydimension.get_labels(self.height))
        layout.add(0, 1, self.frame.get_element(self.width, self.height))
        layout.add(0, 1, self.get_plot(xdimension, ydimension))
        layout.add(1, 1, xdimension.get_labels(self.width))
        self.svg.load_layout(layout)

    def get_plot(self, xdimension, ydimension):
        "Get the element for the chart plot area, grid and datapoints."
        result = Element("g")
        result["class"] = "plot"
        clippath_id = next(utils.unique_id)
        result["clip-path"] = f"url(#{clippath_id})"
        result.total_width = self.width
        result.total_height = self.height

        # Clip path definition. Yes, can be added as part of the result.
        result += Element(
            "defs",
            Element(
                "clipPath",
                Element("rect", width=N(self.width), height=N(self.height)),
                id=clippath_id,
            ),
        )

        # Add the x axis grid.
        if self.xgrid:
            if isinstance(self.xgrid, dict):
                color = self.xgrid.get("color") or constants.DEFAULT_GRID_COLOR
            else:
                color = constants.DEFAULT_GRID_COLOR
            result += xdimension.get_grid(self.height, color)

        # Add the y axis grid.
        if self.ygrid:
            if isinstance(self.ygrid, dict):
                color = self.ygrid.get("color") or constants.DEFAULT_GRID_COLOR
            else:
                color = constants.DEFAULT_GRID_COLOR
            result += ydimension.get_grid(self.width, color)

        # Graphics for points.
        result += (graphics := Element("g"))
        graphics["class"] = "graphics"
        if self.opacity != 1:
            graphics["opacity"] = self.opacity
        for datapoint in self.points:
            kwargs = {}
            if (opacity := datapoint.get("opacity")) is not None:
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

        # Labels for points. After graphics, to render on top.
        result += (labels := Element("g"))
        labels["class"] = "labels"
        labels["font-family"] = constants.DEFAULT_FONT_FAMILY
        labels["font-size"] = constants.DEFAULT_FONT_SIZE
        labels["text-anchor"] = "start"

        for datapoint in self.points:
            if label := datapoint.get("label"):
                labels += Element(
                    "text",
                    label,
                    x=N(
                        xdimension.get_pixel(datapoint["x"])
                        + datapoint["label_x_offset"]
                        + self.PADDING
                    ),
                    y=N(
                        ydimension.get_pixel(datapoint["y"])
                        + constants.DEFAULT_FONT_SIZE / 4
                    ),
                )

        return result


register(Scatter2d)
