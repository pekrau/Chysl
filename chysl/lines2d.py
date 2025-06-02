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
            "title": {"$ref": "#title"},
            "description": {"$ref": "#description"},
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
            "xgrid": {
                "title": "X grid specification.",
                "$ref": "#grid",
            },
            "ygrid": {
                "title": "Y grid specification.",
                "$ref": "#grid",
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
        description=None,
        lines=None,
        width=None,
        xaxis=None,
        yaxis=None,
        xgrid=None,
        ygrid=None,
    ):
        super().__init__(title=title, description=description)
        assert lines is None or isinstance(lines, list)
        assert width is None or (isinstance(width, (int, float)) and width > 0)
        assert xaxis is None or isinstance(xaxis, (bool, dict))
        assert yaxis is None or isinstance(yaxis, (bool, dict))
        assert xgrid is None or isinstance(xgrid, (bool, dict))
        assert ygrid is None or isinstance(ygrid, (bool, dict))

        self.lines = []
        if lines:
            for line in lines:
                self.add(line)
        self.width = width or constants.DEFAULT_WIDTH
        self.xaxis = True if xaxis is None else xaxis
        self.yaxis = True if yaxis is None else yaxis
        self.xgrid = True if xgrid is None else xgrid
        self.ygrid = True if ygrid is None else ygrid

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
        for line in self.lines:
            line["line"].check_required("x", "y")

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
        ypxlow = self.height
        self.height += self.width - self.height
        ypxhigh = self.height

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

        # Chart frame; overwrite grid.
        self.svg += xdimension.get_frame(
            ypxlow,
            ypxhigh,
            color=constants.DEFAULT_COLOR,
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
                self.height += constants.DEFAULT_FONT_SIZE * (
                    1 + constants.FONT_DESCEND
                )

            # X axis caption.
            if isinstance(self.xaxis, dict) and (caption := self.xaxis.get("caption")):
                self.height += constants.DEFAULT_FONT_SIZE
                labels += Element(
                    "text",
                    caption,
                    x=utils.N(
                        xdimension.get_pixel((xdimension.first + xdimension.last) / 2)
                    ),
                    y=utils.N(self.height),
                )
            self.height += constants.DEFAULT_FONT_SIZE * constants.FONT_DESCEND

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

        # Graphics for lines.
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
