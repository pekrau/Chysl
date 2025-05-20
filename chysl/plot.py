"2D chart plotting x/y data."

import copy
import pathlib

import constants
import schema
import utils
from chart import Chart, Entry, Reader, Element
from dimension import Dimension
from path import Path


class Plot(Chart):
    "2D chart plotting x/y data."

    DEFAULT_WIDTH = 600

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "entries"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "plot"},
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
                            "title": "Scatter plot.",
                            "type": "object",
                            "required": ["entry", "data"],
                            "additionalProperties": False,
                            "properties": {
                                "entry": {"const": "scatter"},
                                "data": {"$ref": "#data_or_source"},
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
        if not isinstance(entry, Scatter):
            raise ValueError(f"invalid entry for plot: {entry}; not a Scatter")
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
            xdimension.update_span(entry.xminmax)
            ydimension.update_span(entry.yminmax)
        xdimension.expand_span(0.05)
        ydimension.expand_span(0.05)
        ydimension.update_right(self.height)
        # XXX This is a kludge.
        xdimension.update_left(
            utils.get_text_length(
                "99", constants.DEFAULT_FONT_FAMILY, self.DEFAULT_FONT_SIZE
            )
            + constants.DEFAULT_PADDING
        )
        xdimension.update_right(constants.DEFAULT_PADDING)
        xticks = xdimension.get_ticks()
        yticks = ydimension.get_ticks()
        self.height += self.width - self.height

        # X axis grid and its labels.
        if self.xaxis:
            if isinstance(self.xaxis, dict):
                absolute = bool(self.xaxis.get("absolute"))
                color = self.xaxis.get("color") or "gray"
                caption = self.xaxis.get("caption")
            else:
                absolute = False
                color = "gray"
                caption = None
            self.svg += (xaxis := Element("g"))
            ticks = xdimension.get_ticks(absolute=absolute)
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
                        x=utils.N(tick.pixel),
                        y=utils.N(self.height),
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
                absolute = bool(self.yaxis.get("absolute"))
                color = self.yaxis.get("color") or "gray"
                caption = self.yaxis.get("caption")
            else:
                absolute = False
                color = "gray"
                caption = None
            self.svg += (yaxis := Element("g"))
            ticks = ydimension.get_ticks(absolute=absolute)
            left = xdimension.get_pixel(xdimension.first)
            right = xdimension.get_pixel(xdimension.last)
            path = Path(left, ticks[0].pixel)
            path.H(right)
            for tick in ticks[1:]:
                path.M(left, tick.pixel).H(right)
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
                        x=utils.N(xdimension.left - constants.DEFAULT_PADDING),
                        y=utils.N(tick.pixel + self.DEFAULT_FONT_SIZE / 3),
                    )
                )
                if tick is ticks[0]:
                    label["y"] = utils.N(tick.pixel)
                elif tick is ticks[-1]:
                    label["y"] = utils.N(tick.pixel + self.DEFAULT_FONT_SIZE)

        # Graphics for entries.
        self.svg += (graphics := Element("g"))
        for entry in self.entries:
            graphics += entry.render_graphic(xdimension, ydimension)


class Scatter(Entry):
    "Scatter plot."

    DEFAULT_SIZE = 5

    def __init__(self, data):
        assert isinstance(data, (list, dict))

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

        # Data from file or web source.
        else:
            self.source = data.copy()
            try:
                source = data["source"]
            except KeyError:
                raise ValueError("No 'source' given in data.")
            format = data.get("format")
            if not format:
                format = pathlib.Path(source).suffix.lstrip(".") or "csv"
            if format not in constants.FORMATS:
                raise ValueError(f"Unknown format '{format}' specified.")
            reader = Reader(source)
            reader.read()
            reader.parse(format)
            self.data = []
            for record in reader.data:
                point = {"x": float(record["x"]), "y": float(record["y"])}
                if (color := record.get("color")) is not None:
                    point["color"] = color
                # XXX Add other properties if any.
                self.data.append(point)

    def as_dict(self):
        result = super().as_dict()
        try:
            # Data from file or web source.
            result["data"] = self.source
        except AttributeError:
            # Explicit data points.
            result["data"] = data = []
            for point in self.data:
                item = {"x": point["x"], "y": point["y"]}
                if (color := point.get("color")) is not None:
                    item["color"] = color
                # XXX Add other properties if any.
                data.append(item)
        return result

    @property
    def xminmax(self):
        return self.minmax("x")

    @property
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

    def render_graphic(self, xdimension, ydimension):
        g = Element("g", stroke="none", fill="black")
        for point in self.data:
            xvalue = point["x"]
            if isinstance(xvalue, dict):
                xvalue = xvalue["value"]
            yvalue = point["y"]
            if isinstance(yvalue, dict):
                yvalue = yvalue["value"]
            g += Element(
                "circle",
                cx=xdimension.get_pixel(xvalue),
                cy=ydimension.get_pixel(yvalue),
                r=self.DEFAULT_SIZE,
                fill=point.get("color") or "black",
            )
        return g
