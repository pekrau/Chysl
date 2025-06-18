"2D lines chart."

import components
import constants
import schema
import utils
from chart import Chart, Layout, register
from datapoints import DatapointsReader
from dimension import Xdimension, Ydimension
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
                "title": "An array of lists of 2D points to display as lines.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "title": "A list of 2D points to display as a line.",
                    "type": "object",
                    "required": ["line"],
                    "additionalProperties": False,
                    "properties": {
                        "line": {"$ref": "#datapoints"},
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
                            "title": "A link URI from the line, absolute or relative.",
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

        self.lines = []
        if lines:
            for line in lines:
                self.add(line)
        self.width = width or self.DEFAULT_WIDTH
        self.height = height or self.DEFAULT_HEIGHT
        self.frame = components.Frame(frame)
        self.xaxis = True if xaxis is None else xaxis
        self.yaxis = True if yaxis is None else yaxis
        self.xgrid = True if xgrid is None else xgrid
        self.ygrid = True if ygrid is None else ygrid
        self.thickness = thickness or self.DEFAULT_THICKNESS
        self.color = color or self.DEFAULT_COLOR
        self.opacity = 1 if opacity is None else opacity

    def __iadd__(self, line):
        self.add(line)
        return self

    def add(self, line):
        assert isinstance(line, dict)
        line["line"] = DatapointsReader(line["line"])
        self.lines.append(line)

    def as_dict(self):
        result = super().as_dict()
        result["lines"] = lines = []
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
        if self.thickness != self.DEFAULT_THICKNESS:
            result["thickness"] = self.thickness
        if self.color != self.DEFAULT_COLOR:
            result["color"] = self.color
        if self.opacity != 1:
            result["opacity"] = self.opacity

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
            item["line"] = line["line"].as_dict()
            lines.append(item)
        return result

    def build(self):
        "Create the SVG elements in the 'svg' attribute."
        super().build()

        for line in self.lines:
            line["line"].check_required("x", "y")

        xdimension = Xdimension(self.width, self.xaxis)
        for line in self.lines:
            xdimension.update_span(line["line"].minmax("x"))
        xdimension.expand_span(0.05)
        xdimension.build()

        ydimension = Ydimension(self.height, self.yaxis, reversed=True)
        for line in self.lines:
            ydimension.update_span(line["line"].minmax("y"))
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
            for dp in line["line"]:
                x = dp["x"]
                y = dp["y"]
                points.append(
                    f"{N(xdimension.get_pixel(x))} {N(ydimension.get_pixel(y))}"
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
