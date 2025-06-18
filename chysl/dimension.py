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

    PADDING = 2

    def __init__(self, extent, axis=True, reversed=False):
        assert isinstance(extent, (int, float)) and extent > 0
        assert isinstance(axis, (bool, dict))
        assert isinstance(reversed, bool)

        self.extent = extent
        if isinstance(axis, bool):
            self.axis = {}
        else:
            self.axis = axis
        self.given_axis = axis
        self.reversed = reversed
        self.min = None
        self.max = None

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

    def build(self):
        "Set or calculate tick positions and prepare graphics and labels."
        ticks = self.axis.get("ticks") or constants.DEFAULT_TICKS_TARGET
        assert (isinstance(ticks, int) and ticks > 1) or (
            isinstance(ticks, (tuple, list))
        )

        # Set explicit min/max, if provided.
        if (min := self.axis.get("min")) is not None:
            assert isinstance(min, (int, float))
            self.min = min
        if (max := self.axis.get("max")) is not None:
            assert isinstance(max, (int, float))
            self.max = max
        span = self.max - self.min
        assert span > 0

        self.factor = self.axis.get("factor")
        assert self.factor is None or (
            isinstance(self.factor, (int, float)) and self.factor > 0
        )

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
        self.func = (lambda v: abs(v)) if self.axis.get("absolute") else (lambda v: v)

    def get_pixel(self, position):
        "Convert position coordinate to pixel coordinate."
        if self.reversed:
            return self.scale * (self.last - position)
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

    def get_grid(self, extent, color):
        raise NotImplementedError

    def get_labels(self, extent, font_size=constants.DEFAULT_FONT_SIZE):
        raise NotImplementedError


class Xdimension(Dimension):
    "Graphics for the x axis."

    def get_grid(self, height, color):
        "Get the x grid lines at the ticks for the graphic."
        ticks = self.get_ticks()
        path = Path(ticks[0].pixel, 0).V(height)
        for tick in ticks[1:]:
            path.M(tick.pixel, 0).V(height)
        result = Element("path", d=path, stroke=color)
        result["class"] = "x-grid"
        return result

    def get_labels(self, width, font_size=constants.DEFAULT_FONT_SIZE):
        "Get the labels for the x dimension ticks."
        labels = self.axis.get("labels")
        if labels is None:
            labels = True
        caption = self.axis.get("caption")
        if not self.given_axis or not (labels or caption):
            return None

        result = Element("g")
        result["class"] = "x-axis-labels"
        result["font-family"] = constants.DEFAULT_FONT_FAMILY
        result["font-size"] = font_size
        result["text-anchor"] = "middle"
        result["stroke"] = "none"
        result["fill"] = "black"
        result.total_width = width
        result.total_height = 0

        if labels:
            ticks = self.get_ticks()
            for tick in ticks:
                result += (
                    label := Element(
                        "text",
                        tick.label,
                        x=N(tick.pixel),
                        y=N(font_size),
                    )
                )
                if tick is ticks[0] and math.isclose(tick.position, self.first):
                    label["text-anchor"] = "start"
                elif tick is ticks[-1] and math.isclose(tick.position, self.last):
                    label["text-anchor"] = "end"
            result.total_height += font_size * (1 + constants.FONT_DESCEND)

        if caption:
            result.total_height += font_size
            result += (
                elem := Element(
                    "text",
                    caption,
                    x=N(self.get_pixel((self.first + self.last) / 2)),
                    y=N(result.total_height),
                )
            )
            elem["class"] = "x-axis-caption"
            result.total_height += font_size * constants.FONT_DESCEND + self.PADDING

        return result


class Ydimension(Dimension):
    "Graphics for the y axis."

    def get_grid(self, width, color):
        "Get the y grid lines at the ticks for the graphic."
        ticks = self.get_ticks()
        path = Path(0, ticks[0].pixel).H(width)
        for tick in ticks[1:]:
            path.M(0, tick.pixel).H(width)
        result = Element("path", d=path, stroke=color)
        result["class"] = "y-grid"
        return result

    def get_labels(self, height, font_size=constants.DEFAULT_FONT_SIZE):
        "Get the labels for the y dimension ticks."
        labels = self.axis.get("labels")
        if labels is None:
            labels = True
        caption = self.axis.get("caption")
        if not self.given_axis or not (labels or caption):
            return None

        result = Element("g")
        result["class"] = "y-axis-labels"
        result["font-family"] = constants.DEFAULT_FONT_FAMILY
        result["font-size"] = font_size
        result["text-anchor"] = "end"
        result["stroke"] = "none"
        result["fill"] = "black"
        result.total_width = 0
        result.total_height = height

        if labels:
            ticks = self.get_ticks()
            for tick in ticks:
                result += (
                    label := Element(
                        "text",
                        tick.label,
                        x=N(-self.PADDING),
                        y=N(tick.pixel + font_size / 3),
                    )
                )
                if tick is ticks[0] and math.isclose(tick.position, self.first):
                    if self.reversed:
                        label["y"] = N(tick.pixel)
                    else:
                        label["y"] = N(tick.pixel + 0.75 * font_size)
                elif tick is ticks[-1] and math.isclose(tick.position, self.last):
                    if self.reversed:
                        label["y"] = N(tick.pixel + 0.75 * font_size)
                    else:
                        label["y"] = N(tick.pixel)
                result.total_width = max(result.total_width, utils.get_text_width(tick.label))
            result.total_width += self.PADDING

        if caption:
            x = - (result.total_width + font_size * (1 + constants.FONT_DESCEND))
            y = self.get_pixel((self.first + self.last) / 2)
            result += (elem := Element(
                "text",
                caption,
                x=N(x),
                y=N(y),
                transform=f"translate({N(x)},{N(y)}) rotate(270) translate({N(-x)},{N(-y)})",
            )
                       )
            elem["text-anchor"] = "middle"
            result.total_width += font_size * (2 + constants.FONT_DESCEND)

        result["transform"] = f"translate({N(result.total_width)},0)"
        return result
