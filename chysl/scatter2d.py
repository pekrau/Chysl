"2D scatter chart."

import components
import constants
import schema
import utils
from chart import Chart, Layout, register
from datasource import Datasource
from dimension import Xdimension, Ydimension, Axis, Grid
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
                "oneOf": [
                    {
                        "title": "Inline list of 2D points.",
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "properties": {
                                "x": {"type": "number"},
                                "y": {"type": "number"},
                                "marker": {"$ref": "#marker"},
                                "size": {
                                    "title": "Size of the marker (pixels).",
                                    "type": "number",
                                    "minimumExclusive": 0,
                                },
                                "color": {
                                    "title": "Color specified by hex code '#rrggbb' or CSS3 color name.",
                                    "type": "string",
                                    "format": "color",
                                },
                                "opacity": {
                                    "title": "Opacity of the marker.",
                                    "type": "number",
                                    "minimum": 0,
                                    "maximum": 1,
                                    "default": 1,
                                },
                                "label": {
                                    "title": "Description of the point.",
                                    "type": "string",
                                },
                                "href": {
                                    "title": "A link URL, absolute or relative.",
                                    "type": "string",
                                    "format": "uri-reference",
                                },
                            },
                        },
                    },
                    {
                        "title": "External source of 2D points data.",
                        "$ref": "#datasource",
                    },
                ],
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

        self.width = width or self.DEFAULT_WIDTH
        self.height = height or self.DEFAULT_HEIGHT
        self.frame = components.Frame(frame)
        self.xaxis = Axis(xaxis)
        self.yaxis = Axis(yaxis)
        self.xgrid = Grid(xgrid)
        self.ygrid = Grid(ygrid)
        self.marker = marker or self.DEFAULT_MARKER
        self.size = size or self.DEFAULT_SIZE
        self.color = color or self.DEFAULT_COLOR
        self.opacity = 1 if opacity is None else opacity

        if isinstance(points, dict):
            self.datasource = Datasource(points, Point2d)
            self.points = self.datasource.data
        else:
            self.datasource = None
            self.points = []
            if points:
                for point in points:
                    self.add(point)

    def __iadd__(self, point):
        self.add(point)
        return self

    def add(self, point):
        assert isinstance(point, (dict, Point2d))
        if isinstance(point, dict):
            point = Point2d(**point)
        self.points.append(point)

    def as_dict(self):
        result = super().as_dict()
        if self.width != self.DEFAULT_WIDTH:
            result["width"] = self.width
        if self.height != self.DEFAULT_HEIGHT:
            result["height"] = self.height
        result.update(self.frame.as_dict())
        result.update(self.xaxis.as_dict("xaxis"))
        result.update(self.yaxis.as_dict("yaxis"))
        result.update(self.xgrid.as_dict("xgrid"))
        result.update(self.ygrid.as_dict("ygrid"))
        if self.marker != self.DEFAULT_MARKER:
            result["marker"] = self.marker
        if self.size != self.DEFAULT_SIZE:
            result["size"] = self.size
        if self.color != self.DEFAULT_COLOR:
            result["color"] = self.color
        if self.opacity != 1:
            result["opacity"] = self.opacity
        if self.datasource:
            result["points"] = self.datasource.as_dict()
        else:
            result["points"] = points = []
            for point in self.points:
                points.append(point.as_dict())
        return result

    def build(self):
        "Create the SVG elements in the 'svg' attribute."
        super().build()

        xdimension = Xdimension(self.width, self.xaxis)
        xdimension.update_span([p.x for p in self.points])
        xdimension.expand_span(0.05)
        xdimension.build()

        ydimension = Ydimension(self.height, self.yaxis, reversed=True)
        ydimension.update_span([p.y for p in self.points])
        ydimension.expand_span(0.05)
        ydimension.build()

        layout = Layout(rows=2, columns=2, title=self.title)
        layout.add(0, 0, ydimension.get_labels(self.height))
        layout.add(0, 1, self.frame.get_element(self.width, self.height))
        layout.add(0, 1, self.get_plot(xdimension, ydimension))
        layout.add(1, 1, xdimension.get_labels(self.width))
        self.svg.load_layout(layout)

    def get_plot(self, xdimension, ydimension):
        "Get the element for the chart plot area, grid and points."
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

        # Add the x coordinate grid.
        if self.xgrid:
            result += xdimension.get_grid(self.height, self.xgrid)

        # Add the y coordinate grid.
        if self.ygrid:
            result += ydimension.get_grid(self.width, self.ygrid)

        # Graphics for points.
        result += (graphics := Element("g"))
        graphics["class"] = "graphics"
        if self.opacity != 1:
            graphics["opacity"] = self.opacity
        for point in self.points:
            kwargs = {}
            if point.opacity is not None:
                kwargs["opacity"] = point.opacity
            if point.href:
                kwargs["href"] = point.href
            marker = Marker(
                point.marker or self.marker,
                size=point.size or self.size,
                color=point.color or self.color,
                **kwargs,
            )
            graphics += marker.get_graphic(
                xdimension.get_pixel(point.x),
                ydimension.get_pixel(point.y),
            )
            point.label_x_offset = marker.label_x_offset

        # Labels for points. After graphics, to render on top.
        result += (labels := Element("g"))
        labels["class"] = "labels"
        labels["font-family"] = constants.DEFAULT_FONT_FAMILY
        labels["font-size"] = constants.DEFAULT_FONT_SIZE
        labels["text-anchor"] = "start"

        for point in self.points:
            if point.label:
                labels += Element(
                    "text",
                    point.label,
                    x=N(
                        xdimension.get_pixel(point.x)
                        + point.label_x_offset
                        + self.PADDING
                    ),
                    y=N(
                        ydimension.get_pixel(point.y)
                        + constants.DEFAULT_FONT_SIZE / 4
                    ),
                )

        return result


register(Scatter2d)


class Point2d:
    "A point in a 2D scatter chart."

    # Fields, with converter and checker functions.
    fields = dict(
        x=dict(convert=float, required=True),
        y=dict(convert=float, required=True),
        marker=dict(check=lambda m: m in constants.MARKERS),
        size=dict(convert=float, check=lambda s: s > 0),
        color=dict(check=lambda c: utils.is_color(c)),
        opacity=dict(convert=float, check=lambda o: 0 <= o <= 1),
        label=None,
        href=None,
    )

    def __init__(
            self, x, y, marker=None, size=None, color=None, opacity=None, label=None, href=None,
    ):
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert marker is None or marker in constants.MARKERS
        assert size is None or (isinstance(size, (int, float)) and size > 0)
        assert color is None or utils.is_color(color)
        assert opacity is None or (
            isinstance(opacity, (int, float)) and (0 <= opacity <= 1)
        )
        assert label is None or isinstance(label, str)
        assert href is None or isinstance(href, str)

        self.x = x
        self.y = y
        self.marker = marker
        self.size = size
        self.color = color
        self.opacity = opacity
        self.label = label
        self.href = href

    def as_dict(self):
        result = dict(x=self.x, y=self.y)
        if self.marker is not None:
            result["marker"] = self.marker
        if self.size is not None:
            result["size"] = self.size
        if self.color is not None:
            result["color"] = self.color
        if self.opacity is not None:
            result["opacity"] = self.opacity
        if self.label is not None:
            result["label"] = self.label
        if self.href is not None:
            result["href"] = self.href
        return result
