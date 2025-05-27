"2D chart plotting x/y data; scatter, line, etc."

import copy
import pathlib

import constants
import schema
import utils
from chart import Chart, Entry, DataReader, Element
from dimension import Dimension
from marker import Marker
from path import Path
from utils import N


class Plot2d(Chart):
    "2D chart plotting x/y data; scatter, etc."

    DEFAULT_WIDTH = 600

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "entries"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "plot2d"},
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
            "entries": {
                "title": "Sets of data with specified visualization.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "oneOf": [
                        {
                            "title": "2D scatter plot.",
                            "type": "object",
                            "required": ["entry", "data"],
                            "additionalProperties": False,
                            "properties": {
                                "entry": {"const": "scatter2d"},
                                "data": {"$ref": "#items_or_source"},
                                "size": {
                                    "title": "Default value when not given by data.",
                                    "$ref": "#size",
                                    "default": constants.DEFAULT_MARKER_SIZE,
                                },
                                "color": {
                                    "title": "Default value when not given by data.",
                                    "$ref": "#color",
                                },
                                "opacity": {
                                    "title": "Default value when not given by data.",
                                    "$ref": "#opacity",
                                },
                                "marker": {
                                    "title": "Default value when not given by data.",
                                    "$ref": "#marker",
                                },
                            },
                        },
                        {
                            "title": "2D line plot.",
                            "type": "object",
                            "required": ["entry", "data"],
                            "additionalProperties": False,
                            "properties": {
                                "entry": {"const": "line2d"},
                                "data": {"$ref": "#items_or_source"},
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
                            },
                        },
                    ],
                },
            },
        },
    }

    schema.add_defs(SCHEMA)

    def __init__(
        self,
        title=None,
        entries=None,
        width=None,
        xaxis=None,
        yaxis=None,
    ):
        super().__init__(title=title, entries=entries)
        assert width is None or (isinstance(width, (int, float)) and width > 0)
        assert xaxis is None or isinstance(xaxis, (bool, dict))
        assert yaxis is None or isinstance(yaxis, (bool, dict))

        self.width = width or self.DEFAULT_WIDTH
        self.xaxis = True if xaxis is None else xaxis
        self.yaxis = True if yaxis is None else yaxis

    def convert_entry(self, entry):
        entry = super().convert_entry(entry)
        if not isinstance(entry, _Plot2dEntry):
            raise ValueError(f"invalid entry for plot: {entry}; not a subclass of Plot2dEntry")
        return entry

    def as_dict(self):
        result = super().as_dict()
        if self.width != self.DEFAULT_WIDTH:
            result["width"] = self.width
        if self.xaxis is False or isinstance(self.xaxis, dict):
            result["xaxis"] = self.xaxis
        if self.yaxis is False or isinstance(self.yaxis, dict):
            result["yaxis"] = self.yaxis
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
        for entry in self.entries:
            xdimension.update_span(entry.xminmax())
            ydimension.update_span(entry.yminmax())
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

        # Graphics for entries.
        self.svg += (graphics := Element("g"))
        for entry in self.entries:
            graphics += entry.render_graphic(xdimension, ydimension)


class _Plot2dEntry(Entry):
    "Generic Entry class for Plot2d."

    def __init__(self, data, size=None, color=None, opacity=None, marker=None):
        assert isinstance(data, (list, dict))
        assert color is None or utils.is_color(color)
        assert opacity is None or (
            isinstance(opacity, (int, float)) and opacity >= 0 and opacity <= 1
        )

        self.color = color or constants.DEFAULT_COLOR
        self.opacity = opacity or 1

        # Explicit data points.
        if isinstance(data, list):
            if len(data) == 0:
                raise ValueError("No data in the list.")
            if not isinstance(data[0], dict):
                raise ValueError("First item in the list is not a dict.")
            if "x" not in data[0]:
                raise ValueError("First dict in the list does not contain 'x'.")
            if "y" not in data[0]:
                raise ValueError("First dict in the list does not contain 'y'.")
            self.data = copy.deepcopy(data)  # For safety.

        # Data from file, web resource or database.
        else:
            try:
                self.source = data["source"]
            except KeyError:
                raise ValueError("No 'source' given in data.")
            reader = DataReader(self.source)
            reader.read()
            self.parameters = data.get("parameters")
            if self.parameters:
                reader.map_parameters_fields(self.parameters)
            self.data = reader.data

    def as_dict(self):
        result = super().as_dict()
        if self.color != constants.DEFAULT_COLOR:
            result["color"] = self.color
        if self.opacity != 1:
            result["opacity"] = self.opacity
        try:
            # Data from file or web source.
            result["data"] = dict(source=self.source)
            if self.parameters:
                result["data"]["parameters"] = self.parameters
        except AttributeError:
            # Explicit data points.
            result["data"] = data = []
            for point in self.data:
                item = {"x": point["x"], "y": point["y"]}
                if (size := point.get("size")) is not None:
                    item["size"] = size
                if (color := point.get("color")) is not None:
                    item["color"] = color
                if (opacity := point.get("opacity")) is not None and opacity != 1:
                    item["opacity"] = opacity
                if (marker := point.get("marker")) is not None:
                    item["marker"] = marker
                data.append(item)
        return result

    def xminmax(self):
        return self.minmax("x")

    def yminmax(self):
        return self.minmax("y")

    def minmax(self, key):
        point = self.data[0]
        value = point[key]
        if isinstance(value, dict):
            try:
                low = value["low"]
            except KeyError:
                low = value["value"] - value["error"]
            try:
                high = value["high"]
            except KeyError:
                high = value["value"] + value["error"]
        else:
            low = value
            high = value
        for point in self.data[1:]:
            value = point[key]
            if isinstance(value, dict):
                try:
                    low = min(low, value["low"])
                except KeyError:
                    low = min(low, value["value"] - value["error"])
                try:
                    high = max(high, value["high"])
                except KeyError:
                    high = max(high, value["value"] + value["error"])
            else:
                low = min(low, value)
                high = max(high, value)
        return (low, high)


class Scatter2d(_Plot2dEntry):
    "2D scatter plot."

    def __init__(self, data, size=None, color=None, opacity=None, marker=None):
        super().__init__(data, color=color, opacity=opacity)
        assert size is None or (isinstance(size, (int, float)) and size > 0)
        assert marker is None or utils.is_marker(marker)

        self.size = size or constants.DEFAULT_MARKER_SIZE
        self.marker = marker or constants.DEFAULT_MARKER

    def as_dict(self):
        result = super().as_dict()
        if self.size != constants.DEFAULT_MARKER_SIZE:
            result["size"] = self.size
        if self.marker != constants.DEFAULT_MARKER:
            result["marker"] = self.marker
        return result

    def render_graphic(self, xdimension, ydimension):
        g = Element("g")
        for point in self.data:
            xvalue = point["x"]
            if isinstance(xvalue, dict):
                xvalue = xvalue["value"]
            yvalue = point["y"]
            if isinstance(yvalue, dict):
                yvalue = yvalue["value"]
            if (opacity := point.get("opacity")) is None:
                opacity = self.opacity
            marker = Marker(
                point.get("marker") or self.marker,
                size=point.get("size") or self.size,
                color=point.get("color") or self.color,
                opacity=opacity,
            )
            g += marker.get_graphic(
                xdimension.get_pixel(xvalue), ydimension.get_pixel(yvalue)
            )
        return g


class Line2d(_Plot2dEntry):
    "2D line plot."

    def __init__(self, data, linewidth=None, color=None, opacity=None):
        super().__init__(data, color=color, opacity=opacity)

        assert linewidth is None or (isinstance(linewidth (int, float)) and linewidth > 0)

        self.linewidth = linewidth or constants.DEFAULT_LINEWIDTH

    def render_graphic(self, xdimension, ydimension):
        points = []
        for point in self.data:
            xvalue = point["x"]
            if isinstance(xvalue, dict):
                xvalue = xvalue["value"]
            yvalue = point["y"]
            if isinstance(yvalue, dict):
                yvalue = yvalue["value"]
            points.append(f"{N(xdimension.get_pixel(xvalue))} {N(ydimension.get_pixel(yvalue))}")
        result = Element("polyline",
                         points=",".join(points),
                         fill="none",
                         stroke=self.color)
        if self.opacity != 1:
            result["opacity"] = self.opacity
        result["stroke-width"] = self.linewidth
        result["stroke-linejoin"] = "round"
        result["stroke-linecap"] = "round"
        return result
