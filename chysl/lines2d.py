"2D lines chart."

import constants
import schema
import utils
from chart import Chart, Element
from datapoints import DatapointsReader
from dimension import Dimension
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
        xdimension = Dimension(width=self.width)
        ydimension = Dimension(width=self.width, reversed=True)
        for line in self.lines:
            xdimension.update_span(line["line"].minmax("x"))
            ydimension.update_span(line["line"].minmax("y"))
        xdimension.expand_span(0.05)
        ydimension.expand_span(0.05)
        ydimension.update_end(self.height)
        # XXX This is a kludge, assuming legend label is two characters wide.
        xdimension.update_start(
            utils.get_text_length(
                "99", constants.DEFAULT_FONT_FAMILY, constants.DEFAULT_FONT_SIZE
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
            self.height += constants.DEFAULT_FONT_SIZE
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
            self.height += constants.DEFAULT_FONT_SIZE * constants.FONT_DESCEND

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
                        y=N(tick.pixel + constants.DEFAULT_FONT_SIZE / 3),
                    )
                )
                if tick is ticks[0]:
                    label["y"] = N(tick.pixel)
                elif tick is ticks[-1]:
                    label["y"] = N(tick.pixel + constants.DEFAULT_FONT_SIZE)

        # Graphics for lines.
        self.svg += (graphics := Element("g"))
        for line in self.lines:
            points = []
            for dp in line["line"]:
                xvalue = dp["x"]
                yvalue = dp["y"]
                points.append(
                    f"{N(xdimension.get_pixel(xvalue))} {N(ydimension.get_pixel(yvalue))}"
                )
            graphics += (
                elem := Element(
                    "polyline",
                    points=",".join(points),
                    fill="none",
                    stroke=line.get("color") or "black",
                )
            )
            if (opacity := line.get("opacity")) is not None:
                elem["opacity"] = opacity
            elem["stroke-width"] = line.get("linewidth") or constants.DEFAULT_LINEWIDTH
            elem["stroke-linejoin"] = "round"
            elem["stroke-linecap"] = "round"
            if href := line.get("href"):
                elem["href"] = href
