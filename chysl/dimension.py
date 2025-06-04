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


Tick = collections.namedtuple("Tick", ["position", "pixel", "label"], defaults=[None])


class Epoch(enum.StrEnum):
    ORDINAL = "ordinal"
    DATE = "Julian date"  # XXX not implemented
    DATETIME = "Julian date and time"  # XXX not implemented


class Dimension:
    """Graphics for coordinate axis.
    Store min/max and set or calculate base/first/last and ticks for the span.
    """

    def __init__(self, extent, reversed=False):
        assert isinstance(extent, (int, float)) and extent > 0
        assert isinstance(reversed, bool)

        self.extent = extent
        self.reversed = reversed
        self.min = None
        self.max = None

    def __repr__(self):
        fields = [
            f"{a}={getattr(self,a)}" for a in ["extent", "reversed", "min", "max"]
        ]
        return f"Dimension({', '.join(fields)})"

    @property
    def span(self):
        "Return current min and max values."
        return (self.min, self.max)

    def update_span(self, value):
        "Update current min and max values."
        assert isinstance(value, (int, float)) or isinstance(value, (tuple, list))

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

    def build(
        self,
        ticks=constants.DEFAULT_TICKS_TARGET,
        min=None,
        max=None,
        labels=True,
        factor=None,
        absolute=False,
    ):
        "Set or calculate tick positions and prepare graphics and labels."
        assert (isinstance(ticks, int) and ticks > 1) or (
            isinstance(ticks, (tuple, list))
        )
        assert isinstance(labels, bool)
        assert min is None or isinstance(min, (int, float))
        assert max is None or isinstance(max, (int, float))
        assert factor is None or (isinstance(factor, (int, float)) and factor > 0)

        self.labels = labels
        self.factor = factor

        if min is not None:
            self.min = min
        if max is not None:
            self.max = max
        span = self.max - self.min

        # Compute ticks; evaluate several different sets of positions.
        if isinstance(ticks, int):
            series = []
            self.magnitude = math.log10(span / ticks)
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
            score = abs(len(self.positions) - ticks)
            for magnitude, values in series[1:]:
                s = abs(len(values) - ticks)
                if s < score:
                    self.magnitude = magnitude
                    self.positions = values
                    score = s
            assert self.positions[0] <= self.min
            assert self.positions[1] > self.min
            assert self.positions[-1] >= self.max
            assert self.positions[-2] < self.max
            # If min and/or max set explicitly, exclude those positions.
            if min is None:
                self.first = self.positions[0]
            else:
                while self.positions and self.positions[0] < min:
                    self.positions.pop(0)
                self.first = min
            if max is None:
                self.last = self.positions[-1]
            else:
                while self.positions and self.positions[-1] > max:
                    self.positions.pop()
                self.last = max

        # Explicit tick positions given.
        else:
            self.magnitude = round(math.log10(span / len(ticks)))
            for tick in ticks:
                assert isinstance(tick, (int, float))
            assert list(ticks) == list(sorted(ticks))
            self.positions = ticks
            self.first = min(self.min, self.positions[0])
            self.last = max(self.max, self.positions[-1])

        self.scale = self.extent / (self.last - self.first)
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

    def get_pixel(self, position):
        "Convert position coordinate to pixel coordinate."
        if self.reversed:
            return self.extent + self.scale * (self.last - position)
        else:
            return self.scale * (position - self.first)

    def get_extent(self, begin, end):
        "Convert position extent to pixel extent."
        return self.scale * abs(end - begin)

    def get_ticks(self):
        return [
            Tick(
                value,
                self.get_pixel(value),
                label=self.format % self.func(value / self.factor),
            )
            for value in self.positions
            if self.first <= value <= self.last
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

    def get_grid(self, height, color):
        "Get the x grid lines at the ticks for the graphic."
        ticks = self.get_ticks()
        result = Element("path", stroke=color)
        result["class"] = "x-grid"
        path = Path(ticks[0].pixel, 0).V(height)
        for tick in ticks[1:]:
            path.M(tick.pixel, 0).V(height)
        result["d"] = path
        return result

    def get_labels(self, font_size):
        "Get the labels for the x dimension ticks."
        result = Element("g")
        result["class"] = "x-axis-labels"
        result["font-family"] = constants.DEFAULT_FONT_FAMILY
        result["font-size"] = font_size
        result["text-anchor"] = "middle"
        result["stroke"] = "none"
        result["fill"] = "black"
        if not self.labels:
            return result
        ticks = self.get_ticks()
        for tick in ticks:
            result += (
                label := Element(
                    "text",
                    tick.label,
                    x=N(tick.pixel),
                    # Empirical factor 0.9...
                    y=N(0.9 * font_size),
                )
            )
            if tick is ticks[0] and math.isclose(tick.position, self.first):
                label["text-anchor"] = "start"
            elif tick is ticks[-1] and math.isclose(tick.position, self.last):
                label["text-anchor"] = "end"
        return result


class Ydimension(Dimension):
    "Graphics for the y axis."

    def get_grid(self, xpxlow, xpxhigh, color):
        "Get the x grid lines at the ticks for the graphic."
        ticks = self.get_ticks()
        path = Path(xpxlow, ticks[0].pixel).H(xpxhigh)
        for tick in ticks[1:]:
            path.M(xpxlow, tick.pixel).H(xpxhigh)
        result = Element("path", d=path, stroke=color)
        result["class"] = "x-grid"
        return result

    def get_labels(self, width, font_size):
        "Get the labels for the y dimension ticks."
        result = Element("g")
        result["class"] = "y-axis-labels"
        result["text-anchor"] = "end"
        result["stroke"] = "none"
        result["fill"] = "black"
        result["font-size"] = font_size
        if not self.labels:
            return result
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
            if tick is ticks[0] and math.isclose(tick.position, self.first):
                label["y"] = N(tick.pixel)
            elif tick is ticks[-1] and math.isclose(tick.position, self.last):
                label["y"] = N(tick.pixel + 0.75 * font_size)
        return result
