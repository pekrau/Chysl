"Timelines having events and periods."

import math

import constants
import schema
import utils
from color import Color
from chart import Chart, Layout, register
from dimension import Xdimension
from marker import Marker
from minixml import Element
from path import Path
from utils import N
from vector2 import Vector2


class Timelines(Chart):
    "Timelines having events and periods."

    DEFAULT_WIDTH = 600
    DEFAULT_SIZE = 18

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "entries"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "timelines"},
            "title": {
                "title": "Title of the chart.",
                "$ref": "#text",
            },
            "description": {
                "title": "Description of the chart. Rendered as <desc> in SVG.",
                "type": "string",
            },
            "width": {
                "title": "Width of the chart area (pixels).",
                "type": "number",
                "default": DEFAULT_WIDTH,
                "exclusiveMinimum": 0,
            },
            "frame": {
                "title": "Chart area frame specification.",
                "$ref": "#frame",
            },
            "legend": {
                "title": "Legend to be displayed or not.",
                "type": "boolean",
                "default": True,
            },
            "axis": {
                "title": "Time axis specification.",
                "$ref": "#axis",
            },
            "grid": {
                "title": "Grid specification.",
                "$ref": "#grid",
            },
            "entries": {
                "title": "Entries (events, periods) in the timelines.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "oneOf": [
                        {
                            "title": "Event at an instant in time.",
                            "type": "object",
                            "required": ["instant"],
                            "additionalProperties": False,
                            "properties": {
                                "instant": {
                                    "title": "Time of the event.",
                                    "$ref": "#fuzzy_number",
                                },
                                "label": {
                                    "title": "Description of the event.",
                                    "type": "string",
                                },
                                "timeline": {
                                    "title": "Timeline to place the event in.",
                                    "type": "string",
                                },
                                "marker": {
                                    "title": "Marker for event.",
                                    "$ref": "#marker",
                                },
                                "color": {
                                    "title": "Color of the event marker.",
                                    "type": "string",
                                    "format": "color",
                                    "default": "black",
                                },
                                "placement": {
                                    "title": "Placement of event label.",
                                    "enum": constants.PLACEMENTS,
                                    "default": constants.RIGHT,
                                },
                                "fuzzy": {
                                    "title": "Error bar marker for fuzzy number.",
                                    "type": "boolean",
                                    "default": True,
                                },
                                "href": {
                                    "title": "A URI for a link, absolute or relative.",
                                    "type": "string",
                                    "format": "uri-reference",
                                },
                            },
                        },
                        {
                            "title": "Period of time.",
                            "type": "object",
                            "required": ["begin", "end"],
                            "additionalProperties": False,
                            "properties": {
                                "begin": {
                                    "title": "Starting time of the period.",
                                    "$ref": "#fuzzy_number",
                                },
                                "end": {
                                    "title": "Ending time of the period.",
                                    "$ref": "#fuzzy_number",
                                },
                                "label": {
                                    "title": "Description of the period.",
                                    "type": "string",
                                },
                                "timeline": {
                                    "title": "Timeline to place the period in.",
                                    "type": "string",
                                },
                                "color": {
                                    "title": "Color of the period graphic.",
                                    "type": "string",
                                    "format": "color",
                                    "default": "white",
                                },
                                "placement": {
                                    "title": "Placement of period label.",
                                    "enum": constants.PLACEMENTS,
                                    "default": constants.CENTER,
                                },
                                "fuzzy": {
                                    "title": "Marker to use for fuzzy number.",
                                    "enum": constants.FUZZY_MARKERS,
                                    "default": constants.ERROR,
                                },
                                "href": {
                                    "title": "A URI for a link, absolute or relative.",
                                    "type": "string",
                                    "format": "uri-reference",
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
        description=None,
        width=None,
        frame=True,
        legend=True,
        axis=True,
        grid=True,
        entries=None,
    ):
        super().__init__(title=title, description=description)
        assert width is None or (isinstance(width, (int, float)) and width > 0)
        assert isinstance(legend, bool)
        assert isinstance(frame, (bool, dict))
        assert isinstance(axis, (bool, dict))
        assert isinstance(grid, (bool, dict))
        assert entries is None or isinstance(entries, list)

        self.width = width or self.DEFAULT_WIDTH
        self.frame = frame
        self.legend = legend
        self.axis = axis
        self.grid = grid
        self.entries = []
        if entries:
            for entry in entries:
                self.add(entry)

    def __iadd__(self, entry):
        self.add(entry)
        return self

    def add(self, entry):
        assert isinstance(entry, (dict, Event, Period))
        if isinstance(entry, dict):
            if "instant" in entry:
                entry = Event(**entry)
            elif "begin" in entry:
                entry = Period(**entry)
            else:
                raise ValueError(f"invalid entry in timeline: {entry}")
        assert isinstance(entry, (Event, Period))
        self.entries.append(entry)

    def as_dict(self):
        result = super().as_dict()
        result["entries"] = [e.as_dict() for e in self.entries]
        if self.width != self.DEFAULT_WIDTH:
            result["width"] = self.width
        if not self.legend:
            result["legend"] = False
        if self.frame is False or isinstance(self.frame, dict):
            result["frame"] = self.frame
        if self.axis is False or isinstance(self.axis, dict): # XXX Get from dimension as_dict
            result["axis"] = self.axis
        if self.grid is False or isinstance(self.grid, dict):
            result["grid"] = self.grid
        return result

    def build(self):
        "Create the SVG elements in the 'svg' attribute."
        super().build()

        # Determine the y position for each timeline; sets height of the chart area.
        timelines = dict()  # Key: timeline; value: y (pixels)
        self.height = 0
        for entry in self.entries:
            if entry.timeline not in timelines:
                self.height += constants.DEFAULT_LINE_WIDTH
                timelines[entry.timeline] = self.height
                self.height += self.DEFAULT_SIZE + constants.DEFAULT_LINE_WIDTH

        # Set up the time axis.
        dimension = Xdimension(self.width, self.axis)
        for entry in self.entries:
            dimension.update_span(entry.minmax())
        dimension.build()

        # Create the layout, add the different parts to it and load.
        layout = Layout(rows=2, columns=2, title=self.title)
        layout.add(0, 0, self.get_legend(timelines))
        layout.add(0, 1, self.get_frame())
        layout.add(0, 1, self.get_plot(dimension, timelines))
        layout.add(1, 1, dimension.get_labels(self.width))
        self.svg.load_layout(layout)

    def get_legend(self, timelines):
        "Get the element for the legend of the chart; possibly None."
        if not self.legend:
            return None

        y_offset = (
            self.DEFAULT_SIZE
            + constants.DEFAULT_FONT_SIZE
            - constants.DEFAULT_FONT_SIZE * constants.FONT_DESCEND
        ) / 2
        result = Element("g")
        result["class"] = "legend"
        result.total_width = 0
        result["font-family"] = constants.DEFAULT_FONT_FAMILY
        result["font-size"] = constants.DEFAULT_FONT_SIZE
        result["text-anchor"] = "end"
        for text, height in timelines.items():
            if not text:
                continue
            result += Element("text", text, y=N(height + y_offset))
            result.total_width = max(result.total_width, utils.get_text_width(text))
        result.total_height = self.height
        # Empirical factor 0.5
        padding = 0.5 * constants.DEFAULT_FONT_SIZE
        result.total_width += padding
        result["transform"] = f"translate({N(result.total_width - padding)}, 0)"
        return result

    def get_frame(self):
        "Get the element for the frame around the chart; possibly None."
        if not self.frame:
            return None

        if isinstance(self.frame, dict):
            thickness = self.frame.get("thickness") or constants.DEFAULT_FRAME_THICKNESS
            color = self.frame.get("color") or "black"
        else:
            thickness = constants.DEFAULT_FRAME_THICKNESS
            color = "black"
        result = Element(
            "rect",
            x=N(thickness / 2),
            y=N(thickness / 2),
            width=N(self.width + thickness),
            height=N(self.height + thickness),
            stroke=color,
            fill="none",
        )
        result["class"] = "frame"
        result["stroke-width"] = N(thickness)
        result.total_width = self.width + 2 * thickness
        result.total_height = self.height + 2 * thickness
        return result

    def get_plot(self, dimension, timelines):
        "Get the element for the chart plot area, grid and entries."
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

        # Add the time axis grid.
        if self.grid:
            if isinstance(self.grid, dict):
                color = self.grid.get("color") or constants.DEFAULT_GRID_COLOR
            else:
                color = constants.DEFAULT_GRID_COLOR
            result += dimension.get_grid(self.height, color)

        # Graphics for entries (periods and events).
        for entry in self.entries:
            result += entry.render_graphic(timelines[entry.timeline], dimension)

        # Labels for entries (periods and events). After graphics, to render on top.
        result += (labels := Element("g"))
        labels["class"] = "labels"
        labels["font-family"] = constants.DEFAULT_FONT_FAMILY
        labels["font-size"] = constants.DEFAULT_FONT_SIZE
        labels["text-anchor"] = "middle"
        for entry in self.entries:
            if label := entry.render_label(timelines[entry.timeline], dimension):
                labels += label

        return result


register(Timelines)


class _Temporal:
    "Abstract temporal entry in a timelines chart."

    def __init__(self, label=None, timeline=None, color=None):
        assert label is None or isinstance(label, str)
        assert timeline is None or isinstance(timeline, str)
        assert color is None or isinstance(color, str)

        self.label = label
        self.timeline = timeline or label
        self.color = color

    def as_dict(self):
        result = {}
        if self.label:
            result["label"] = self.label
        if self.timeline != self.label:
            result["timeline"] = self.timeline
        if self.color:
            result["color"] = self.color
        return result

    def minmax(self):
        raise NotImplementedError

    def render_graphic(self, y, dimension):
        raise NotImplementedError

    def render_label(self, y, dimension):
        raise NotImplementedError

    def render_graphic_error(self, instant, y, dimension):
        "Get the error bars for the fuzzy instant."
        assert isinstance(instant, dict)
        x = dimension.get_pixel(instant["value"])
        result = Element("g", stroke="black")
        try:  # If 'low' is given, then ignore 'error'.
            xlow = dimension.get_pixel(instant["low"])
        except KeyError:
            xlow = dimension.get_pixel(instant["value"] - instant.get("error", 0))
        result += Element(
            "path",
            d=Path(xlow, y + 0.25 * Timelines.DEFAULT_SIZE)
            .v(0.5 * Timelines.DEFAULT_SIZE)
            .m(0, -0.25 * Timelines.DEFAULT_SIZE)
            .H(x),
        )
        try:  # If 'high' is given, then ignore 'error'.
            xhigh = dimension.get_pixel(instant["high"])
        except KeyError:
            xhigh = dimension.get_pixel(instant["value"] + instant.get("error", 0))
        result += Element(
            "path",
            d=Path(xhigh, y + 0.25 * Timelines.DEFAULT_SIZE)
            .v(0.5 * Timelines.DEFAULT_SIZE)
            .m(0, -0.25 * Timelines.DEFAULT_SIZE)
            .H(x),
        )
        return result


class Event(_Temporal):
    "Event at a given instant in a timeline."

    DEFAULT_PLACEMENT = constants.RIGHT
    DEFAULT_MARKER = constants.OVAL

    def __init__(
        self,
        instant,
        label=None,
        timeline=None,
        marker=None,
        color=None,
        placement=None,
        fuzzy=None,
        href=None,
    ):
        super().__init__(label=label, timeline=timeline, color=color)
        assert isinstance(instant, (int, float, dict))
        assert marker is None or marker in constants.MARKERS
        assert placement is None or placement in constants.PLACEMENTS
        assert fuzzy is None or isinstance(fuzzy, bool)
        assert href is None or isinstance(href, str)

        self.instant = instant
        self.marker = marker or self.DEFAULT_MARKER
        self.placement = placement or self.DEFAULT_PLACEMENT
        self.fuzzy = fuzzy is None or fuzzy
        self.href = href

    def as_dict(self):
        result = super().as_dict()
        result["instant"] = self.instant
        if self.marker != self.DEFAULT_MARKER:
            result["marker"] = self.marker
        if self.placement != self.DEFAULT_PLACEMENT:
            result["placement"] = self.placement
        if not self.fuzzy:
            result["fuzzy"] = False
        if self.href:
            result["href"] = self.href
        return result

    def minmax(self):
        if isinstance(self.instant, dict):
            return (
                self.instant.get("low", self.instant["value"]),
                self.instant.get("high", self.instant["value"]),
            )
        else:
            return self.instant

    def render_graphic(self, y, dimension):
        if isinstance(self.instant, dict):
            x = dimension.get_pixel(self.instant["value"])
        else:
            x = dimension.get_pixel(self.instant)

        marker = Marker(self.marker, color=self.color, href=self.href)
        result = marker.get_graphic(x, y + Timelines.DEFAULT_SIZE / 2)
        result["class"] = "event"
        self.label_x_offset = marker.label_x_offset

        # Get error bars if fuzzy value; place below marker itself.
        if self.fuzzy and isinstance(self.instant, dict):
            result = Element(
                "g", self.render_graphic_error(self.instant, y, dimension), result
            )

        return result

    def render_label(self, y, dimension):
        if not self.label:
            return None

        match self.placement:

            case constants.LEFT:
                if isinstance(self.instant, dict):
                    value = ["value"]
                    try:
                        value = self.instant["low"]
                    except KeyError:
                        value = self.instant["value"] - self.instant.get("error", 0)
                    x = dimension.get_pixel(value) - 2
                else:
                    x = dimension.get_pixel(self.instant)
                    x -= self.label_x_offset + 2
                anchor = "end"

            case constants.CENTER:
                x = dimension.get_pixel(self.instant)
                anchor = "middle"

            case constants.RIGHT:
                if isinstance(self.instant, dict):
                    value = ["value"]
                    try:
                        value = self.instant["high"]
                    except KeyError:
                        value = self.instant["value"] + self.instant.get("error", 0)
                    x = dimension.get_pixel(value) + 2
                else:
                    x = dimension.get_pixel(self.instant)
                    x += self.label_x_offset + 2
                if self.marker == constants.NONE:
                    anchor = "middle"
                else:
                    anchor = "start"
                anchor = "start"

        label = Element(
            "text",
            self.label,
            x=N(x),
            y=N(
                y
                + (
                    Timelines.DEFAULT_SIZE
                    + constants.DEFAULT_FONT_SIZE
                    - constants.DEFAULT_FONT_SIZE * constants.FONT_DESCEND
                )
                / 2
            ),
        )
        label["class"] = "event-label"
        label["text-anchor"] = anchor
        return label


class Period(_Temporal):
    "Period of time in a timeline."

    DEFAULT_PLACEMENT = constants.CENTER
    DEFAULT_FUZZY = constants.ERROR

    def __init__(
        self,
        begin,
        end,
        label=None,
        timeline=None,
        color=None,
        placement=None,
        fuzzy=None,
        href=None,
    ):
        super().__init__(label=label, timeline=timeline, color=color)
        assert isinstance(begin, (int, float, dict))
        assert isinstance(end, (int, float, dict))
        assert placement is None or placement in constants.PLACEMENTS
        assert fuzzy is None or isinstance(fuzzy, str)
        assert href is None or isinstance(href, str)

        self.begin = begin
        self.end = end
        self.placement = placement or self.DEFAULT_PLACEMENT
        self.fuzzy = fuzzy or self.DEFAULT_FUZZY
        self.href = href

    def as_dict(self):
        result = super().as_dict()
        result["begin"] = self.begin
        result["end"] = self.end
        if self.placement != self.DEFAULT_PLACEMENT:
            result["placement"] = self.placement
        if self.fuzzy != self.DEFAULT_FUZZY:
            result["fuzzy"] = self.fuzzy
        if self.href:
            result["href"] = self.href
        return result

    def minmax(self):
        if isinstance(self.begin, dict):
            low = self.begin.get("low", self.begin["value"])
        else:
            low = self.begin
        if isinstance(self.end, dict):
            high = self.end.get("high", self.end["value"])
        else:
            high = self.end
        return (low, high)

    def render_graphic(self, y, dimension):
        # Simple case: do not show fuzzy values, or no fuzzy values.
        if (
            self.fuzzy == constants.NONE
            and not isinstance(self.begin, dict)
            and not isinstance(self.end, dict)
        ):
            result = Element(
                "rect",
                x=N(dimension.get_pixel(self.begin)),
                y=N(y),
                width=N(dimension.get_extent(self.begin, self.end)),
                height=Timelines.DEFAULT_SIZE,
                fill=self.color or "white",
            )
            result["stroke-width"] = constants.DEFAULT_LINE_WIDTH

        # Fuzzy value(s) to be shown.
        else:
            if isinstance(self.begin, dict):
                begin = self.begin["value"]
                try:  # If 'low' is given, then ignore 'error'.
                    low1 = self.begin["low"]
                except KeyError:
                    low1 = begin - self.begin.get("error", 0)
                try:  # If 'high' is given, then ignore 'error'.
                    high1 = self.begin["high"]
                except KeyError:
                    high1 = begin + self.begin.get("error", 0)
                x1 = dimension.get_pixel(low1)
                x2 = dimension.get_pixel(high1)
            else:
                begin = self.begin
                x1 = x2 = dimension.get_pixel(begin)

            if isinstance(self.end, dict):
                end = self.end["value"]
                try:  # If 'low' is given, then ignore 'error'.
                    low2 = self.end["low"]
                except KeyError:
                    low2 = end - self.end.get("error", 0)
                try:  # If 'high' is given, then ignore 'error'.
                    high2 = self.end["high"]
                except KeyError:
                    high2 = end + self.end.get("error", 0)
                x3 = dimension.get_pixel(low2)
                x4 = dimension.get_pixel(high2)
            else:
                end = self.end
                x3 = x4 = dimension.get_pixel(end)

            # The fuzzy regions overlap; adjust.
            if x2 > x3:
                x2 = (x2 + x3) / 2
                x3 = x2

            # Graphics depends on how to show fuzzy values.
            result = Element("g", stroke="black")
            result["stroke-width"] = constants.DEFAULT_LINE_WIDTH

            match self.fuzzy:

                case constants.ERROR:
                    result += Element(
                        "rect",
                        x=N(dimension.get_pixel(begin)),
                        y=N(y),
                        width=N(dimension.get_extent(begin, end)),
                        height=Timelines.DEFAULT_SIZE,
                        fill=self.color or "white",
                    )
                    if isinstance(self.begin, dict):
                        result += self.render_graphic_error(self.begin, y, dimension)
                    if isinstance(self.end, dict):
                        result += self.render_graphic_error(self.end, y, dimension)

                case constants.WEDGE:
                    path = (
                        Path(x2, y)
                        .L(x1, y + Timelines.DEFAULT_SIZE / 2)
                        .L(x2, y + Timelines.DEFAULT_SIZE)
                    )
                    if x2 < x3:
                        path.H(x3)
                    path.L(x4, y + Timelines.DEFAULT_SIZE / 2)
                    path.L(x3, y)
                    path.Z()
                    result += Element("path", d=path, fill=self.color or "white")

                case constants.GRADIENT:
                    # The constant-color part of the period.
                    if x2 < x3:
                        # In some viewers, there is a glitch between parts.
                        tweak = constants.DEFAULT_LINE_WIDTH / 4
                        # The filled rectangle.
                        result += Element(
                            "rect",
                            x=N(x2 - tweak),
                            y=N(y),
                            width=N(x3 - x2 + 2 * tweak),
                            height=Timelines.DEFAULT_SIZE,
                            fill=self.color or "white",
                            stroke="none",
                        )
                        # The horizontal lines of the filled rectangle.
                        result += Element(
                            "path",
                            d=Path(x2 - tweak, y)
                            .H(x3 + 2 * tweak)
                            .m(0, Timelines.DEFAULT_SIZE)
                            .H(x2 - tweak),
                        )
                    # The left gradient of the period.
                    if x1 < x2:
                        result += (defs := Element("defs"))
                        # The gradient-filled rectangle.
                        id1 = next(utils.unique_id)
                        defs += (fill1 := Element("linearGradient", id=id1))
                        fill1 += (stop := Element("stop", offset=0))
                        stop["stop-color"] = self.color or "white"
                        stop["stop-opacity"] = 0
                        fill1 += (stop := Element("stop", offset=1))
                        stop["stop-color"] = self.color or "white"
                        stop["stop-opacity"] = 1
                        result += Element(
                            "rect",
                            x=N(x1),
                            y=N(y),
                            width=N(x2 - x1),
                            height=Timelines.DEFAULT_SIZE,
                            fill=f"url(#{id1})",
                            stroke="none",
                        )
                        # Horizontal lines of the gradient-filled rectangle.
                        id2 = next(utils.unique_id)
                        defs += (stroke1 := Element("linearGradient", id=id2))
                        stroke1 += (stop := Element("stop", offset=0))
                        stop["stop-color"] = "black"
                        stop["stop-opacity"] = 0
                        stroke1 += (stop := Element("stop", offset=1))
                        stop["stop-color"] = "black"
                        stop["stop-opacity"] = 1
                        result += Element(
                            "path",
                            d=Path(x1, y).H(x2).m(0, Timelines.DEFAULT_SIZE).H(x1),
                            stroke=f"url(#{id2})",
                        )

                    # No left gradient; path line at beginning of rectangle.
                    else:
                        result += Element(
                            "line",
                            x1=N(x1),
                            y1=N(y),
                            x2=N(x1),
                            y2=N(y + Timelines.DEFAULT_SIZE),
                        )

                    # The right gradient of the period.
                    if x3 < x4:
                        result += (defs := Element("defs"))
                        id3 = next(utils.unique_id)
                        defs += (fill2 := Element("linearGradient", id=id3))
                        fill2 += (stop := Element("stop", offset=0))
                        stop["stop-color"] = self.color or "white"
                        stop["stop-opacity"] = 1
                        fill2 += (stop := Element("stop", offset=1))
                        stop["stop-color"] = self.color or "white"
                        stop["stop-opacity"] = 0
                        # The gradient-filled rectangle.
                        result += Element(
                            "rect",
                            x=N(x3),
                            y=N(y),
                            width=N(x4 - x3),
                            height=Timelines.DEFAULT_SIZE,
                            fill=f"url(#{id3})",
                            stroke="none",
                        )
                        # Horizontal lines of the gradient-filled rectangle.
                        id4 = next(utils.unique_id)
                        defs += (stroke2 := Element("linearGradient", id=id4))
                        stroke2 += (stop := Element("stop", offset=0))
                        stop["stop-color"] = "black"
                        stop["stop-opacity"] = 1
                        stroke2 += (stop := Element("stop", offset=1))
                        stop["stop-color"] = "black"
                        stop["stop-opacity"] = 0
                        result += Element(
                            "path",
                            d=Path(x3, y).H(x4).m(0, Timelines.DEFAULT_SIZE).H(x3),
                            stroke=f"url(#{id4})",
                        )

                    # No right gradient; path line at end of rectangle.
                    else:
                        result += Element(
                            "line",
                            x1=N(x3),
                            y1=N(y),
                            x2=N(x3),
                            y2=N(y + Timelines.DEFAULT_SIZE),
                        )

                case constants.TAPER:
                    raise NotImplementedError

        result["class"] = "period"
        if self.href:
            result = Element("a", result, href=self.href)

        return result

    def render_label(self, y, dimension):
        if not self.label:
            return None

        if isinstance(self.begin, dict):
            begin = self.begin["value"]
            try:
                low = self.begin["low"]
            except KeyError:
                low = begin - self.begin.get("error", 0)
        else:
            begin = self.begin
            low = begin

        if isinstance(self.end, dict):
            end = self.end["value"]
            try:
                high = self.end["low"]
            except KeyError:
                high = end + self.end.get("error", 0)
        else:
            end = self.end
            high = end

        color = "black"
        match self.placement:

            case constants.LEFT:
                x = dimension.get_pixel(low) - 2
                anchor = "end"

            case constants.CENTER:
                x = dimension.get_pixel((begin + end) / 2)
                anchor = "middle"
                if self.color:
                    color = Color(self.color).best_contrast

            case constants.RIGHT:
                x = dimension.get_pixel(high) + 2
                anchor = "start"

        label = Element(
            "text",
            self.label,
            x=N(x),
            y=N(
                y
                + (
                    Timelines.DEFAULT_SIZE
                    + constants.DEFAULT_FONT_SIZE
                    - constants.DEFAULT_FONT_SIZE * constants.FONT_DESCEND
                )
                / 2
            ),
            fill=color,
        )
        label["class"] = "period-label"
        label["text-anchor"] = anchor
        return label
