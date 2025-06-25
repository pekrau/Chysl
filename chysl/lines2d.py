"2D lines chart."

import components
import constants
import schema
import utils
from chart import Chart, Layout, register
from datasource import Datasource
from dimension import Xdimension, Ydimension, Axis, Grid
from minixml import Element
from path import Path
from utils import N


class Lines2d(Chart):
    "2D lines chart."

    DEFAULT_WIDTH = 600
    DEFAULT_HEIGHT = 600
    DEFAULT_THICKNESS = 1
    DEFAULT_COLOR = "black"

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "lines"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "lines2d"},
            "title": {
                "title": "Title of the chart.",
                "$ref": "#text",
            },
            "description": {
                "title": "Description of the chart. Rendered as <desc> in SVG.",
                "type": "string",
            },
            "lines": {
                "title": "Array of lines.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "title": "Line consisting of 2D points with optional styling.",
                    "type": "object",
                    "required": ["line"],
                    "additionalProperties": False,
                    "properties": {
                        "line": {
                            "oneOf": [
                                {
                                    "title": "Inline list of 2D points.",
                                    "type": "array",
                                    "minItems": 2,
                                    "items": {
                                        "type": "object",
                                        "additionalProperties": False,
                                        "properties": {
                                            "x": {"type": "number"},
                                            "y": {"type": "number"},
                                        },
                                    },
                                },
                                {
                                    "title": "External source of 2D points data.",
                                    "$ref": "#datasource",
                                },
                            ],
                        },
                        "thickness": {
                            "title": "Thickness of the line (pixels).",
                            "type": "number",
                            "minimumExclusive": 0,
                            "default": DEFAULT_THICKNESS,
                        },
                        "color": {
                            "title": "Color of the line.",
                            "type": "string",
                            "format": "color",
                            "default": DEFAULT_COLOR,
                        },
                        "opacity": {
                            "title": "Opacity of the line.",
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                            "default": 1,
                        },
                        "href": {
                            "title": "A link URL, absolute or relative.",
                            "type": "string",
                            "format": "uri-reference",
                        },
                    },
                },
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
            "thickness": {
                "title": "Default thickness of the lines (pixels).",
                "type": "number",
                "minimumExclusive": 0,
                "default": DEFAULT_THICKNESS,
            },
            "color": {
                "title": "Default line color.",
                "type": "string",
                "format": "color",
                "default": DEFAULT_COLOR,
            },
            "opacity": {
                "title": "Default line opacity.",
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
        lines=None,
        width=None,
        height=None,
        frame=True,
        xaxis=True,
        yaxis=True,
        xgrid=True,
        ygrid=True,
        thickness=None,
        color=None,
        opacity=None,
    ):
        super().__init__(title=title, description=description)
        assert lines is None or isinstance(lines, list)
        assert width is None or (isinstance(width, (int, float)) and width > 0)
        assert height is None or (isinstance(height, (int, float)) and height > 0)
        assert isinstance(frame, (bool, dict))
        assert isinstance(xaxis, (bool, dict))
        assert isinstance(yaxis, (bool, dict))
        assert isinstance(xgrid, (bool, dict))
        assert isinstance(ygrid, (bool, dict))
        assert thickness is None or (
            isinstance(thickness, (int, float)) and thickness > 0
        )
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
        self.thickness = thickness or self.DEFAULT_THICKNESS
        self.color = color or self.DEFAULT_COLOR
        self.opacity = 1 if opacity is None else opacity

        self.lines = []
        if lines:
            for line in lines:
                self.add(line)

    def __iadd__(self, line):
        self.add(line)
        return self

    def add(self, line):
        assert isinstance(line, dict)
        if isinstance(line["line"], dict):
            line["datasource"] = Datasource(line["line"], Point2d)
            line["line"] = line["datasource"].data
        else:
            for pos, data in enumerate(line["line"]):
                line["line"][pos] = Point2d(**data)
        self.lines.append(line)

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
        if self.thickness != self.DEFAULT_THICKNESS:
            result["thickness"] = self.thickness
        if self.color != self.DEFAULT_COLOR:
            result["color"] = self.color
        if self.opacity != 1:
            result["opacity"] = self.opacity

        result["lines"] = lines = []
        for line in self.lines:
            item = {}
            if (thickness := line.get("thickness")) is not None:
                item["thickness"] = thickness
            if (color := line.get("color")) is not None:
                item["color"] = color
            if (opacity := line.get("opacity")) is not None:
                item["opacity"] = opacity
            if href := line.get("href"):
                item["href"] = href
            try:
                datasource = line["datasource"]
            except KeyError:
                item["line"] = [p.as_dict() for p in line["line"]]
            else:
                item["line"] = datasource.as_dict()
            lines.append(item)
        return result

    def build(self):
        "Create the SVG elements in the 'svg' attribute."
        super().build()

        xdimension = Xdimension(self.width, self.xaxis)
        for line in self.lines:
            xdimension.update_span([p.x for p in line["line"]])
        xdimension.expand_span(0.05)
        xdimension.build()

        ydimension = Ydimension(self.height, self.yaxis, reversed=True)
        for line in self.lines:
            ydimension.update_span([p.y for p in line["line"]])
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

        # Graphics for lines.
        result += (graphics := Element("g", fill="none", stroke=self.color))
        graphics["class"] = "graphics"
        graphics["stroke-width"] = self.thickness
        if self.opacity != 1:
            graphics["opacity"] = self.opacity
        graphics["stroke-linejoin"] = "round"
        graphics["stroke-linecap"] = "round"

        for line in self.lines:
            points = []
            for p in line["line"]:
                points.append(
                    f"{N(xdimension.get_pixel(p.x))} {N(ydimension.get_pixel(p.y))}"
                )
            elem = Element("polyline", points=",".join(points))
            if (thickness := line.get("thickness")) is not None:
                elem["stroke-width"] = thickness
            if (color := line.get("color")) is not None:
                elem["stroke"] = color
            if (opacity := line.get("opacity")) is not None:
                elem["opacity"] = opacity
            if href := line.get("href"):
                elem = Element("a", elem, href=href)
            graphics += elem

        return result


register(Lines2d)


class Point2d:
    "2d point in a line."

    # Fields, with converter and checker functions.
    fields = dict(
        x=dict(convert=float, required=True),
        y=dict(convert=float, required=True),
    )

    def __init__(self, x, y):
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))

        self.x = x
        self.y = y

    def as_dict(self):
        return dict(x=self.x, y=self.y)
