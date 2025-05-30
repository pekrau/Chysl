"2D lines chart."

import constants
import schema
import utils
from chart import Chart, Element
from datapoints import DatapointsReader
from dimension import Xdimension, Ydimension
from path import Path
from utils import N


class Lines2d(Chart):
    "2D lines chart."

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "lines"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "lines2d"},
            "title": {
                "title": "Title of the 2D lines chart.",
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
            "lines": {
                "title": "An array of containers of 2D points to display as lines.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "title": "A contaimer of 2D points to display as a line.",
                    "type": "object",
                    "required": ["line"],
                    "additionalProperties": False,
                    "properties": {
                        "line": {"$ref": "#datapoints"},
                        "linewidth": {
                            "title": "Width of the line.",
                            "type": "number",
                            "minimumExclusive": 0,
                            "default": constants.DEFAULT_LINEWIDTH,
                        },
                        "color": {
                            "title": "Color of the line.",
                            "$ref": "#color",
                            "default": "black",
                        },
                        "opacity": {
                            "title": "Opacity of the line.",
                            "$ref": "#opacity",
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
        lines=None,
        width=None,
        xaxis=None,
        yaxis=None,
    ):
        super().__init__(title=title)
        assert lines is None or isinstance(lines, list)
        assert width is None or (isinstance(width, (int, float)) and width > 0)
        assert xaxis is None or isinstance(xaxis, (bool, dict))
        assert yaxis is None or isinstance(yaxis, (bool, dict))

        self.lines = []
        if lines:
            for line in lines:
                self.add(line)
        self.width = width or constants.DEFAULT_WIDTH
        self.xaxis = True if xaxis is None else xaxis
        self.yaxis = True if yaxis is None else yaxis

    def __iadd__(self, line):
        self.add(line)
        return self

    def add(self, line):
        assert isinstance(line, dict)
        line["line"] = DatapointsReader(line["line"], required=["x", "y"])
        self.lines.append(line)

    def as_dict(self):
        result = super().as_dict()
        result["lines"] = lines = []
        if self.width != constants.DEFAULT_WIDTH:
            result["width"] = self.width
        if self.xaxis is False or isinstance(self.xaxis, dict):
            result["xaxis"] = self.xaxis
        if self.yaxis is False or isinstance(self.yaxis, dict):
            result["yaxis"] = self.yaxis
        for line in self.lines:
            i = {}
            for key in ["linewidth", "color", "opacity"]:
                if (value := line.get(key)) is not None:
                    i[key] = value
            if href := line.get("href"):
                i["href"] = href
            i["line"] = line["line"].as_dict()
            lines.append(i)
        return result

    def build(self):
        """Create the SVG elements in the 'svg' attribute.
        Adds the title, if defined.
        Sets the 'svg' and 'height' attributes.
        Requires the 'width' attribute.
        """
        super().build()

        # Determine dimensions for the axes.
        xdimension = Xdimension(width=self.width)
        ydimension = Ydimension(width=self.width, reversed=True)
        for line in self.lines:
            xdimension.update_span(line["line"].minmax("x"))
            ydimension.update_span(line["line"].minmax("y"))
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

        # Y axis: grid and labels.
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

        # Graphics for lines.
        clippath_id, clippath_def = xdimension.get_clippath(ypxlow, ypxhigh)
        self.svg += clippath_def
        self.svg += (graphics := Element("g"))
        graphics["clip-path"] = f"url(#{clippath_id})"
        for line in self.lines:
            points = []
            for dp in line["line"]:
                xvalue = dp["x"]
                yvalue = dp["y"]
                points.append(
                    f"{N(xdimension.get_pixel(xvalue))} {N(ydimension.get_pixel(yvalue))}"
                )
            elem = Element(
                "polyline",
                points=",".join(points),
                fill="none",
                stroke=line.get("color") or "black",
            )
            if (opacity := line.get("opacity")) is not None:
                elem["opacity"] = opacity
            elem["stroke-width"] = line.get("linewidth") or constants.DEFAULT_LINEWIDTH
            elem["stroke-linejoin"] = "round"
            elem["stroke-linecap"] = "round"
            if href := line.get("href"):
                elem = Element("a", elem, href=href)
            graphics += elem
