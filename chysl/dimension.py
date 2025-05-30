"Dimension classes."

import collections
import enum
import itertools
import math

import constants
import utils
from minixml import Element
from path import Path
from utils import N


Tick = collections.namedtuple("Tick", ["user", "pixel", "label"], defaults=[None])


class Epoch(enum.StrEnum):
    ORDINAL = "ordinal"
    DATE = "Julian date"  # XXX not implemented
    DATETIME = "Julian date and time"  # XXX not implemented


class Dimension:
    """Graphics for axis.
    Store min/max and calculate base/first/last and ticks for the span.
    """

    def __init__(self, width, start=0, end=0, reversed=False):
        assert isinstance(width, (int, float)) and width > 0
        assert isinstance(start, (int, float)) and start >= 0
        assert isinstance(end, (int, float)) and end >= 0
        assert isinstance(reversed, bool)

        self.width = width
        self.start = start
        self.end = end
        self.reversed = reversed
        self.min = None
        self.max = None

    @property
    def span(self):
        "Return current min and max values."
        return (self.min, self.max)

    def update_span(self, value):
        "Update current min and max values."
        if self.min is None:
            if isinstance(value, (tuple, list)):
                self.min = min(*value)
            else:
                self.min = value
        elif isinstance(value, (tuple, list)):
            self.min = min(self.min, *value)
        else:
            self.min = min(self.min, value)
        if self.max is None:
            if isinstance(value, (tuple, list)):
                self.max = max(*value)
            else:
                self.max = value
        elif isinstance(value, (tuple, list)):
            self.max = max(self.max, *value)
        else:
            self.max = max(self.max, value)

    def expand_span(self, fraction):
        expansion = fraction * (self.max - self.min)
        self.min -= expansion
        self.max += expansion

    def update_start(self, value):
        if isinstance(value, (tuple, list)):
            self.start = max(self.start, *value)
        else:
            self.start = max(self.start, value)

    def update_end(self, value):
        if isinstance(value, (tuple, list)):
            self.end = max(self.end, *value)
        else:
            self.end = max(self.end, value)

    def build(self, number=8, factor=None, absolute=False):
        "Compute tick positions and prepare graphics and labels."
        assert isinstance(number, int) and number > 1
        assert factor is None or isinstance(factor, (int, float)) and factor >= 0

        span = self.max - self.min
        self.magnitude = math.log10(span / number)
        self.factor = factor
        series = []
        for magnitude in [math.floor(self.magnitude), math.ceil(self.magnitude)]:
            for base in [1, 2, 5]:
                step = base * 10**magnitude
                if self.min == 0:
                    first = 0
                else:
                    first = math.floor(self.min / step) * step
                values = []
                i = itertools.count(0)
                value = first
                while value <= self.max:
                    value = first + next(i) * step
                    values.append(value)
                prev_length = len(values) + 1
                while len(values) >= 2 and len(values) != prev_length:
                    prev_length = len(values)
                    if values[0] < self.min and (
                        values[1] < self.min or math.isclose(values[1], self.min)
                    ):
                        values.pop()
                    if values[-1] > self.max and (
                        values[-2] > self.max or math.isclose(values[-2], self.max)
                    ):
                        values.pop()
                series.append((magnitude, values))
        self.magnitude, self.positions = series[0]
        score = abs(len(self.positions) - number)
        for magnitude, values in series[1:]:
            s = abs(len(values) - number)
            if s < score:
                self.magnitude = magnitude
                self.positions = values
                score = s
        assert self.positions[0] <= self.min
        assert self.positions[1] > self.min
        assert self.positions[-1] >= self.max
        assert self.positions[-2] < self.max
        self.first = self.positions[0]
        self.last = self.positions[-1]
        self.scale = (self.width - self.start - self.end) / (self.last - self.first)
        self.step = 10**self.magnitude
        if self.magnitude < 0:
            self.format = f"%.{-self.magnitude}f"
        else:
            self.format = "%d"
        if self.factor is None:
            if self.magnitude // 3 > 1:
                self.factor = 10 ** (3 * (self.magnitude // 3))
            else:
                self.factor = 1
        self.func = (lambda v: abs(v)) if absolute else (lambda v: v)

    def get_pixel(self, user):
        "Convert user coordinate to pixel coordinate."
        if self.reversed:
            return self.end + self.scale * (self.last - user)
        else:
            return self.start + self.scale * (user - self.first)

    def get_width(self, begin, end):
        "Convert user width to pixel width."
        return self.scale * abs(end - begin)

    def get_ticks(self):
        return [
            Tick(
                value,
                self.get_pixel(value),
                label=self.format % self.func(value / self.factor),
            )
            for value in self.positions
        ]

    def get_frame(self, pxlow, pxhigh, color, linewidth):
        raise NotImplementedError

    def get_grid(self, pxlow, pxhigh):
        raise NotImplementedError

    def get_labels(self, baseline, font_size):
        raise NotImplementedError

    def get_clippath(self, pxlow, pxhigh):
        raise NotImplementedError


class Xdimension(Dimension):
    "Graphics for the x axis."

    def get_frame(self, ypxlow, ypxhigh, color, linewidth):
        "Return the frame around the graphics."
        result = Element(
            "rect",
            x=N(self.get_pixel(self.first)),
            y=N(ypxlow),
            width=N(self.get_width(self.first, self.last)),
            height=N(ypxhigh - ypxlow),
            stroke=color,
        )
        result["stroke-width"] = linewidth
        return result

    def get_clippath(self, ypxlow, ypxhigh):
        "Return a tuple (id, clippath) for the graphics."
        id = next(utils.unique_id)
        return (
            id,
            Element(
                "defs",
                Element(
                    "clipPath",
                    Element(
                        "rect",
                        x=N(self.get_pixel(self.first)),
                        y=N(ypxlow),
                        width=N(self.get_width(self.first, self.last)),
                        height=N(ypxhigh - ypxlow),
                    ),
                    id=id,
                ),
            ),
        )

    def get_grid(self, ypxlow, ypxhigh, color):
        "Get the x grid lines at the ticks for the graphic."
        ticks = self.get_ticks()
        path = Path(ticks[0].pixel, ypxlow).V(ypxhigh)
        for tick in ticks[1:]:
            path.M(tick.pixel, ypxlow).V(ypxhigh)
        path.M(ticks[0].pixel, ypxlow).H(self.width)
        path.M(ticks[0].pixel, ypxhigh).H(self.width)
        return Element("path", d=path, stroke=color)

    def get_labels(self, height, font_size):
        "Get the labels for the x dimension ticks."
        result = Element("g")
        result["text-anchor"] = "middle"
        result["stroke"] = "none"
        result["fill"] = "black"
        result["font-size"] = font_size
        height += font_size
        ticks = self.get_ticks()
        for tick in ticks:
            result += (
                label := Element(
                    "text",
                    tick.label,
                    x=N(tick.pixel),
                    y=N(height),
                )
            )
            if tick is ticks[0]:
                label["text-anchor"] = "start"
            elif tick is ticks[-1]:
                label["text-anchor"] = "end"
        return result


class Ydimension(Dimension):
    "Graphics for the y axis."

    def get_label_length(self, font_size):
        "Get the length of the longest tick label."
        result = 0
        for tick in self.get_ticks():
            result = max(
                result,
                utils.get_text_length(
                    tick.label, constants.DEFAULT_FONT_FAMILY, font_size
                ),
            )
        return result

    def get_frame(self, xpxlow, xpxhigh, color, linewidth):
        "Return the frame around the graphics."
        result = Element(
            "rect",
            x=N(xpxlow),
            y=N(self.get_pixel(self.first)),
            width=N(xpxhigh - xpxlow),
            height=N(self.get_width(self.first, self.last)),
            stroke=color,
        )
        result["stroke-width"] = linewidth
        return result

    def get_clippath(self, xpxlow, xpxhigh):
        "Return a tuple (id, clippath) for the graphics."
        id = next(utils.unique_id)
        return (
            id,
            Element(
                "defs",
                Element(
                    "clipPath",
                    Element(
                        "rect",
                        x=N(xpxlow),
                        y=N(self.get_pixel(self.first)),
                        width=N(xpxhigh - xpxlow),
                        height=N(self.get_width(self.first, self.last)),
                    ),
                    id=id,
                ),
            ),
        )

    def get_grid(self, xpxlow, xpxhigh, color):
        "Get the x grid lines at the ticks for the graphic."
        ticks = self.get_ticks()
        path = Path(xpxlow, ticks[0].pixel).H(xpxhigh)
        for tick in ticks[1:]:
            path.M(xpxlow, tick.pixel).H(xpxhigh)
        path.M(xpxlow, ticks[0].pixel).V(self.width)
        path.M(xpxhigh, ticks[0].pixel).V(self.width)
        return Element("path", d=path, stroke=color)

    def get_labels(self, width, font_size):
        "Get the labels for the y dimension ticks."
        result = Element("g")
        result["text-anchor"] = "end"
        result["stroke"] = "none"
        result["fill"] = "black"
        result["font-size"] = font_size
        ticks = self.get_ticks()
        for tick in ticks:
            result += (
                label := Element(
                    "text",
                    tick.label,
                    x=N(width - constants.DEFAULT_PADDING),
                    y=N(tick.pixel + font_size / 3),
                )
            )
            if tick is ticks[0]:
                label["y"] = N(tick.pixel)
            elif tick is ticks[-1]:
                label["y"] = N(tick.pixel + 0.75 * font_size)
        return result
