"Dimension and Tick classes."

import collections
import enum
import itertools
import math

import utils

Tick = collections.namedtuple("Tick", ["user", "pixel", "label"], defaults=[None])


class Epoch(enum.StrEnum):
    ORDINAL = "ordinal"
    DATE = "Julian date"  # XXX not implemented
    DATETIME = "Julian date and time"  # XXX not implemented


class Dimension:
    "Store min/max and calculate base/first/last and ticks for the span."

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
        self.ticks = [
            Tick(
                value,
                self.get_pixel(value),
                label=self.format % self.func(value / self.factor),
            )
            for value in self.positions
        ]

    def get_ticks(self):
        return [
            Tick(
                value,
                self.get_pixel(value),
                label=self.format % self.func(value / self.factor),
            )
            for value in self.positions
        ]

    def get_pixel(self, user):
        "Convert user coordinate to pixel coordinate."
        if self.reversed:
            return self.end + self.scale * (self.last - user)
        else:
            return self.start + self.scale * (user - self.first)

    def get_width(self, begin, end):
        "Convert user width to pixel width."
        return self.scale * abs(end - begin)


class Xdimension(Dimension):
    "Label graphics for the x axis."

    pass


class Ydimension(Dimension):
    "Label graphics for the y axis."

    pass


if __name__ == "__main__":
    from icecream import ic

    for x in range(1, 8):
        d = Dimension()
        d.update_span([0, x])
        numbers = [t.user for t in d.get_ticks(5)]
        ic(x, d.base, d.step, numbers)
