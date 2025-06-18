"Function to generate a marker."

import math

import constants
import utils
from minixml import Element
from path import Path
from vector2 import Vector2
from utils import N


class Marker:
    "Create graphics and label for a marker."

    DEFAULT_SIZE = 18

    def __init__(self, marker, size=None, color=None, opacity=None, href=None):
        assert utils.is_marker(marker)
        assert color is None or utils.is_color(color)
        assert size is None or (isinstance(size, (int, float)) and size > 0)
        assert opacity is None or (
            isinstance(opacity, (int, float)) and 0 <= opacity <= 1
        )
        assert href is None or isinstance(href, str)

        self.marker = marker
        self.size = size or self.DEFAULT_SIZE
        self.color = color or "black"
        self.opacity = opacity
        self.href = href

    def get_graphic(self, x, y):
        """Return the graphic element for the marker, given the coordinates in pixels.
        The 'label_x_offset' member is set.
        """
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))

        match self.marker:

            case constants.DISC:
                elem = Element(
                    "circle",
                    cx=N(x),
                    cy=N(y),
                    r=N(self.size / 2),
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 2

            case constants.CIRCLE:
                elem = Element(
                    "circle",
                    cx=N(x),
                    cy=N(y),
                    r=N(0.9 * self.size / 2),
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = N(2 * self.size / self.DEFAULT_SIZE)
                self.label_x_offset = self.size / 2

            case constants.OVAL | constants.OVAL_V:
                elem = Element(
                    "ellipse",
                    cx=N(x),
                    cy=N(y),
                    rx=N(self.size / 5),
                    ry=N(self.size / 2),
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 5

            case constants.OVAL_H:
                elem = Element(
                    "ellipse",
                    cx=N(x),
                    cy=N(y),
                    rx=N(self.size / 2),
                    ry=N(self.size / 5),
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 2

            case constants.ELLIPSE | constants.ELLIPSE_V:
                elem = Element(
                    "ellipse",
                    cx=N(x),
                    cy=N(y),
                    rx=N(self.size / 5),
                    ry=N(self.size / 2),
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = N(2 * self.size / self.DEFAULT_SIZE)
                self.label_x_offset = self.size / 5

            case constants.ELLIPSE_H:
                elem = Element(
                    "ellipse",
                    cx=N(x),
                    cy=N(y),
                    rx=N(self.size / 2),
                    ry=N(self.size / 5),
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = N(2 * self.size / self.DEFAULT_SIZE)
                self.label_x_offset = self.size / 2

            case constants.BLOCK:
                elem = Element(
                    "rect",
                    x=N(x - self.size / 2),
                    y=N(y - self.size / 2),
                    width=N(self.size),
                    height=N(self.size),
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 2

            case constants.SQUARE:
                elem = Element(
                    "rect",
                    x=N(x - 0.9 * self.size / 2),
                    y=N(y - 0.9 * self.size / 2),
                    width=N(0.9 * self.size),
                    height=N(0.9 * self.size),
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = N(2 * self.size / self.DEFAULT_SIZE)
                self.label_x_offset = self.size / 2

            case constants.SQUARE_CROSS:
                elem = Element("g", fill="none", stroke=self.color)
                elem["stroke-width"] = N(2 * self.size / self.DEFAULT_SIZE)
                elem += Element(
                    "rect",
                    x=N(x - 0.9 * self.size / 2),
                    y=N(y - 0.9 * self.size / 2),
                    width=N(0.9 * self.size),
                    height=N(0.9 * self.size),
                )
                elem += Element(
                    "path",
                    d=Path(x - 0.9 * self.size / 2, y - 0.9 * self.size / 2)
                    .l(1.8 * self.size / 2, 1.8 * self.size / 2)
                    .M(x - 0.9 * self.size / 2, y + 0.9 * self.size / 2)
                    .l(1.8 * self.size / 2, -1.8 * self.size / 2),
                )
                self.label_x_offset = self.size / 2

            case constants.DIAMOND:
                path = (
                    Path(x, y - self.size / 2)
                    .L(x - self.size / 2, y)
                    .L(x, y + self.size / 2)
                    .L(x + self.size / 2, y)
                    .Z()
                )
                elem = Element("path", d=path, fill="none", stroke=self.color)
                elem["stroke-width"] = N(2 * self.size / self.DEFAULT_SIZE)
                self.label_x_offset = self.size / 2

            case constants.DIAMOND_CROSS:
                path = (
                    Path(x, y - self.size / 2)
                    .L(x - self.size / 2, y)
                    .L(x, y + self.size / 2)
                    .L(x + self.size / 2, y)
                    .Z()
                    .M(x, y - self.size / 2)
                    .v(self.size)
                    .M(x - self.size / 2, y)
                    .h(self.size)
                )
                elem = Element("path", d=path, fill="none", stroke=self.color)
                elem["stroke-width"] = N(2 * self.size / self.DEFAULT_SIZE)
                self.label_x_offset = self.size / 2

            case constants.DIAMOND_F:
                path = (
                    Path(x, y - self.size / 2)
                    .L(x - self.size / 2, y)
                    .L(x, y + self.size / 2)
                    .L(x + self.size / 2, y)
                    .Z()
                )
                elem = Element("path", d=path, fill=self.color, stroke="none")
                self.label_x_offset = self.size / 2

            case constants.PYRAMID:
                path = (
                    Path(x, y - 0.8 * self.size / 2)
                    .L(x - self.size / 2, y + self.size / 2)
                    .h(self.size)
                    .Z()
                )
                elem = Element("path", d=path, fill=self.color, stroke="none")
                self.label_x_offset = self.size / 2

            case constants.TRIANGLE:
                path = (
                    Path(x, y - 0.8 * self.size / 2)
                    .L(x - self.size / 2, y + self.size / 2)
                    .h(self.size)
                    .Z()
                )
                elem = Element("path", d=path, fill="none", stroke=self.color)
                elem["stroke-width"] = N(2 * self.size / self.DEFAULT_SIZE)
                self.label_x_offset = self.size / 2

            case constants.WEDGE:
                path = (
                    Path(x, y + 0.8 * self.size / 2)
                    .L(x - self.size / 2, y - self.size / 2)
                    .h(self.size)
                    .Z()
                )
                elem = Element("path", d=path, fill=self.color, stroke="none")
                self.label_x_offset = self.size / 2

            case constants.TRIGON:
                path = (
                    Path(x, y + 0.8 * self.size / 2)
                    .L(x - self.size / 2, y - self.size / 2)
                    .h(self.size)
                    .Z()
                )
                elem = Element("path", d=path, fill="none", stroke=self.color)
                elem["stroke-width"] = N(2 * self.size / self.DEFAULT_SIZE)
                self.label_x_offset = self.size / 2

            case constants.PENTAGON:
                # https://commons.wikimedia.org/wiki/File:Screw_Head_-_Pentagon_External.svg
                scale = self.size / 40
                elem = Element(
                    "path",
                    d="M20,3 38,16 31,37 9,37 2,16z",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-20, -20)",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 5
                self.label_x_offset = self.size / 2

            case constants.PENTAGON_F:
                # https://commons.wikimedia.org/wiki/File:Screw_Head_-_Pentagon_External.svg
                scale = self.size / 40
                elem = Element(
                    "path",
                    d="M20,3 38,16 31,37 9,37 2,16z",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-20, -20)",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 2

            case constants.HEXAGON:
                # https://commons.wikimedia.org/wiki/File:Hexagon_1.svg
                scale = self.size / 500
                elem = Element(
                    "polygon",
                    points="130.773,438.01 5.774,221.505 130.773,5 380.771,5 505.771,221.505 380.771,438.01",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-255.7, -221.5)",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 54
                self.label_x_offset = self.size / 2

            case constants.HEXAGON_F:
                # https://commons.wikimedia.org/wiki/File:Hexagon_1.svg
                scale = self.size / 500
                elem = Element(
                    "polygon",
                    points="130.773,438.01 5.774,221.505 130.773,5 380.771,5 505.771,221.505 380.771,438.01",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-255.7, -221.5)",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 2

            case constants.HEPTAGON:
                # https://commons.wikimedia.org/wiki/File:Screw_Head_-_Heptagon_External-01.svg
                scale = self.size / 40
                elem = Element(
                    "path",
                    d="m20 2 14.9 7.2 3.6 16-10.3 12.9h-16.4l-10.3-12.9 3.6-16z",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-20, -20)",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 5
                self.label_x_offset = self.size / 2

            case constants.HEPTAGON_F:
                # https://commons.wikimedia.org/wiki/File:Screw_Head_-_Heptagon_External-01.svg
                scale = self.size / 40
                elem = Element(
                    "path",
                    d="m20 2 14.9 7.2 3.6 16-10.3 12.9h-16.4l-10.3-12.9 3.6-16z",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-20, -20)",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 2

            case constants.OCTAGON:
                # https://commons.wikimedia.org/wiki/File:Octagon_2.svg
                scale = self.size / 600
                elem = Element(
                    "polygon",
                    points="151.447,505 5,358.553 5,151.447 151.447,5 358.553,5 505,151.447 505,358.553 358.553,505",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-255.7, -221.5)",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 75
                self.label_x_offset = self.size / 2

            case constants.OCTAGON_F:
                # https://commons.wikimedia.org/wiki/File:Octagon_2.svg
                scale = self.size / 600
                elem = Element(
                    "polygon",
                    points="151.447,505 5,358.553 5,151.447 151.447,5 358.553,5 505,151.447 505,358.553 358.553,505",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-255.7, -221.5)",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 2

            case constants.CROSS:
                center = Vector2(x, y)
                length = self.size * math.sqrt(2) / 4
                path = (
                    Path(center.x - length, center.y - length)
                    .L(center.x + length, center.y + length)
                    .M(center.x + length, center.y - length)
                    .L(center.x - length, center.y + length)
                )
                elem = Element("path", d=path, fill="none", stroke=self.color)
                elem["stroke-width"] = N(3 * self.size / self.DEFAULT_SIZE)
                self.label_x_offset = self.size / 2.5

            case constants.PLUS:
                center = Vector2(x, y)
                length = self.size * math.sqrt(2) / 4
                path = (
                    Path(x - self.size / 2, y)
                    .h(self.size)
                    .M(x, y - self.size / 2)
                    .v(self.size)
                )
                elem = Element("path", d=path, fill="none", stroke=self.color)
                elem["stroke-width"] = N(3 * self.size / self.DEFAULT_SIZE)
                self.label_x_offset = self.size / 2

            case constants.MINUS:
                elem = Element(
                    "rect",
                    x=N(x - self.size / 2),
                    y=N(y - self.size / 8),
                    width=N(self.size),
                    height=N(self.size / 4),
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 2

            case constants.BAR:
                elem = Element(
                    "rect",
                    x=N(x - self.size / 8),
                    y=N(y - self.size / 2),
                    width=N(self.size / 4),
                    height=N(self.size),
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 8

            case constants.CHECK:
                # https://www.svgrepo.com/svg/532154/check
                scale = self.size / 22
                elem = Element(
                    "path",
                    d="M4 12.6111L8.92308 17.5L20 6.5",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-12, -12)",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 3
                self.label_x_offset = self.size / 3

            case constants.BURST:
                center = Vector2(x, y)
                length = self.size * math.sqrt(2) / 4
                path = (
                    Path(x - self.size / 2, y)
                    .h(self.size)
                    .M(x, y - self.size / 2)
                    .v(self.size)
                    .M(center.x - length, center.y - length)
                    .L(center.x + length, center.y + length)
                    .M(center.x + length, center.y - length)
                    .L(center.x - length, center.y + length)
                )
                elem = Element("path", d=path, fill="none", stroke=self.color)
                elem["stroke-width"] = N(2 * self.size / self.DEFAULT_SIZE)
                elem["stroke-linecap"] = "round"
                self.label_x_offset = self.size / 2

            case constants.INFINITY:
                # https://www.svgrepo.com/svg/471556/infinity
                scale = self.size / 24
                elem = Element(
                    "path",
                    d="M18.1777 8C23.2737 8 23.2737 16 18.1777 16C13.0827 16 11.0447 8 5.43875 8C0.85375 8 0.85375 16 5.43875 16C11.0447 16 13.0828 8 18.1788 8H18.1777Z",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-12, -12)",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 3
                self.label_x_offset = self.size / 2.5

            case constants.STAR:
                # https://commons.wikimedia.org/wiki/File:Five-pointed_star.svg
                scale = self.size / 60
                elem = Element(
                    "path",
                    d="m25,1 6,17h18l-14,11 5,17-15-10-15,10 5-17-14-11h18z",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-25, -24)",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 5
                self.label_x_offset = self.size / 2

            case constants.STAR_F:
                # https://commons.wikimedia.org/wiki/File:Five-pointed_star.svg
                scale = self.size / 60
                elem = Element(
                    "path",
                    d="m25,1 6,17h18l-14,11 5,17-15-10-15,10 5-17-14-11h18z",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-25, -24)",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 3

            case constants.GALAXY:
                # https://commons.wikimedia.org/wiki/File:Galaxy_symbol_(rotated,_bold).svg
                scale = self.size / 12
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-6,-6)",
                    d="M8.316 1a5.553 5.553 0 0 1 1.629 3.94A3.443 3.443 0 0 1 6.5 8.378 2.127 2.127 0 0 1 4.375 6.25 1.315 1.315 0 0 1 5.69 4.936c.45 0 .813.365.812.813a.503.503 0 0 1-.147.355l-.71-.208a.502.502 0 0 0-.147.355c0 .449.363.813.812.813A1.315 1.315 0 0 0 7.625 5.75 2.127 2.127 0 0 0 5.5 3.622 3.443 3.443 0 0 0 2.055 7.06c0 1.538.622 2.93 1.629 3.939",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 1
                elem["stroke-linecap"] = "round"
                self.label_x_offset = self.size / 3

            case constants.SUN:
                # https://commons.wikimedia.org/wiki/File:Sun_symbol_(fixed_width).svg
                scale = self.size / 12
                circle = Element(
                    "path",
                    d="M110 60c0 27.617-22.383 50-50 50S10 87.617 10 60s22.383-50 50-50 50 22.383 50 50z",
                    transform="matrix(0.1 0 0 -0.1 0 12)",
                    fill="none",
                    stroke=self.color,
                )
                circle["stroke-width"] = 9
                circle["stroke-linecap"] = "round"
                elem = Element(
                    "g",
                    Element(
                        "path",
                        d="M6 5.102a.899.899 0 1 0 0 1.797.899.899 0 0 0 0-1.797Z",
                        fill=self.color,
                        stroke="none",
                    ),
                    circle,
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-6,-6)",
                )
                self.label_x_offset = self.size / 2.5

            case constants.MERCURY:
                # https://commons.wikimedia.org/wiki/File:Mercury_symbol_(fixed_width).svg
                scale = self.size / 12
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-6,-6)",
                    d="M8 5a1.999 1.999 0 1 0-4 0 1.999 1.999 0 1 0 4 0ZM4 1a1.999 1.999 0 1 0 4 0M6 11V7M4 9h4",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 1
                elem["stroke-linecap"] = "round"
                self.label_x_offset = self.size / 5

            case constants.VENUS:
                # https://commons.wikimedia.org/wiki/File:Earth_symbol_(fixed_width).svg
                scale = self.size / 12
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-6,-6)",
                    d="M6 11V7M4 9h4m1-5a3 3 0 0 1-3 3 3 3 0 0 1-3-3 3 3 0 0 1 3-3 3 3 0 0 1 3 3Z",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 1
                elem["stroke-linecap"] = "round"
                self.label_x_offset = self.size / 4

            case constants.EARTH:
                # https://commons.wikimedia.org/wiki/File:Venus_symbol_(fixed_width).svg
                scale = self.size / 12
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-6,-6)",
                    d="M11 6A5 5 0 1 0 1 6a5 5 0 0 0 10 0zm-5 5V1M1 6h10",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 1
                elem["stroke-linecap"] = "round"
                self.label_x_offset = self.size / 2.5

            case constants.MOON:
                # https://commons.wikimedia.org/wiki/File:Moon_crescent_symbol_(fixed_width).svg
                scale = self.size / 12
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-6,-6)",
                    d="M3.5 1a5 5 0 1 1 0 10c1.785-1.031 2.887-2.938 2.887-5S5.285 2.031 3.5 1z",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 1
                self.label_x_offset = self.size / 5

            case constants.MARS:
                # https://commons.wikimedia.org/wiki/File:Mars_crescent_symbol_(fixed_width).svg
                scale = self.size / 12
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-6,-6)",
                    d="M9 7c0-2.207-1.793-4-4-4S1 4.793 1 7s1.793 4 4 4 4-1.793 4-4ZM7.828 4.172 11 1M9.23 1H11v1.77",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 1
                elem["stroke-linecap"] = "round"
                self.label_x_offset = self.size / 2.5

            case constants.JUPITER:
                # https://en.wikipedia.org/wiki/File:Jupiter_symbol_(fixed_width).svg
                scale = self.size / 12
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-6,-6)",
                    d="M2.25 1a4.33 4.33 0 0 1 0 7.5h7.5M7.25 6v5",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 1
                elem["stroke-linecap"] = "round"
                self.label_x_offset = self.size / 3

            case constants.SATURN:
                # https://en.wikipedia.org/wiki/File:Saturn_symbol_(fixed_width).svg
                scale = self.size / 12
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-6,-6)",
                    d="M3 3h4M5 1v5a1.999 1.999 0 1 1 3.414 1.414C7.508 8.32 7 9.72 7 11",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 0.8
                elem["stroke-linecap"] = "round"
                self.label_x_offset = self.size / 4

            case constants.URANUS:
                # https://commons.wikimedia.org/wiki/File:Uranus_symbol_(fixed_width).svg
                scale = self.size / 12
                circle = Element(
                    "path",
                    d="M60 60v50M35 85l25 25 25-25m0-50c0 13.79-11.21 25-25 25S35 48.79 35 35s11.21-25 25-25 25 11.21 25 25Z",
                    transform="matrix(0.1 0 0 -0.1 0 12)",
                    fill="none",
                    stroke=self.color,
                )
                circle["stroke-width"] = 9
                circle["stroke-linecap"] = "round"
                elem = Element(
                    "g",
                    Element(
                        "path",
                        d="M6 7.602a.899.899 0 1 0 0 1.797.899.899 0 0 0 0-1.797Z",
                        fill=self.color,
                        stroke="none",
                    ),
                    circle,
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-6,-6)",
                )
                self.label_x_offset = self.size / 4

            case constants.NEPTUNE:
                # https://en.wikipedia.org/wiki/File:Neptune_symbol_(fixed_width).svg
                scale = self.size / 12
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(scale)}) translate(-6,-6)",
                    d="M6 11V1M3.5 7.25h5M2.25 1a3.751 3.751 0 0 0 7.5 0",
                    fill="none",
                    stroke=self.color,
                )
                elem["stroke-width"] = 1
                elem["stroke-linecap"] = "round"
                self.label_x_offset = self.size / 3

            case constants.ALPHA:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_alpha.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m239.84 120.88h31.498l-19.084 85.787q-5.5604 24.458-7.5968 30.016 7.4117 34.093 21.493 34.093 16.676 0 17.232-22.975h6.6701q-0.5282 21.493-7.9671 34.834-7.2262 13.155-19.084 13.155-9.8203 0-14.637-7.9673-4.8147-7.9673-10.376-32.61-19.27 40.578-62.997 40.578-29.831 0-47.433-23.161-17.602-23.346-17.602-66.702 0-42.616 19.27-66.332 19.269-23.716 46.321-23.716 19.084 0 31.313 13.526 12.229 13.526 21.679 44.098zm-16.305 72.632q-8.7082-29.831-19.455-46.507-10.746-16.861-25.755-16.861-33.907 0-33.907 79.302 0 75.226 32.425 75.226 28.163 0 41.689-66.332z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 3

            case constants.BETA:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_beta.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m150.53 371.75h-30.572q6.6701-31.313 6.6701-56.697v-201.78q0-31.498 5.5604-46.877 5.7425-15.379 22.048-27.052 16.49-11.858 41.134-11.858 29.275 0 49.101 15.564 20.01 15.379 20.01 43.913 0 33.351-31.684 54.659 47.248 22.234 47.248 69.852 0 25.94-12.599 46.507-12.414 20.381-28.904 29.09-16.305 8.7085-39.096 8.7085-25.94 0-42.245-19.455v34.463q0 35.575-6.6701 60.959zm6.6702-112.1q14.452 23.902 40.393 23.902 25.013 0 36.686-18.158 11.673-18.343 11.673-44.469 0-20.011-7.7822-40.763-7.5966-20.937-19.64-31.869-11.117 2.7791-20.011 2.7791-18.713 0-18.713-9.8202 0-8.8936 15.749-8.8936 9.8203 0 24.458 4.4471 13.155-22.234 13.155-48.359 0-23.346-10.376-35.76-10.191-12.414-26.681-12.414-13.155 0-22.604 7.4113-9.2642 7.4116-12.785 17.787-3.5229 10.191-3.5229 33.537z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 3

            case constants.GAMMA:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_gamma.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m244.01 120.88h38.169l-74.299 155.82q2.7774 25.014 2.7774 43.727 0 52.065-19.455 52.065-14.081 0-14.081-21.864 0-28.534 20.751-71.52-4.0749-26.681-11.487-64.294-7.2261-37.613-15.008-53.918-7.5968-16.305-21.864-16.305-23.346 0-25.014 34.834h-6.6702q0-61.144 36.316-61.144 20.937 0 31.128 24.828 10.191 24.643 20.938 107.47z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.DELTA:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_delta.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m202.13 132.55q-9.2643-10.376-25.755-24.828-18.158-15.935-24.458-25.014-6.2997-9.2642-6.2997-20.196 0-16.305 15.193-25.569 15.193-9.4495 39.651-9.4495 24.458 0 42.615 8.3378 18.343 8.3379 18.343 22.975 0 7.0408-4.4448 11.673-4.4448 4.632-10.376 4.632-8.5227 0-20.011-12.785-11.673-12.97-19.825-18.158-7.9673-5.373-18.714-5.373-13.711 0-22.605 6.1144-8.7088 6.1144-8.7088 15.564 0 8.8936 7.2262 16.676 7.2262 7.7819 37.242 28.349 32.054 22.049 45.21 34.463 13.34 12.414 21.678 30.202 8.3383 17.787 8.3383 37.613 0 34.834-24.643 61.515-24.458 26.496-57.253 26.496-29.831 0-50.398-21.308-20.566-21.308-20.566-56.882 0-34.278 22.604-57.253 22.79-22.975 55.956-27.793zm8.1521 8.5231q-53.177 8.7083-53.177 73.002 0 33.166 13.155 51.509 13.341 18.343 30.943 18.343 18.343 0 30.201-17.602 11.858-17.787 11.858-47.989 0-43.727-32.981-77.264z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.EPSILON:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_epsilon.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m175.45 200.74q-36.501-12.97-36.501-39.28 0-20.752 19.27-33.166 19.455-12.414 48.174-12.414 26.125 0 41.503 8.7085 15.379 8.5231 15.379 20.567 0 6.2997-4.8204 11.117-4.8149 4.632-11.117 4.632-10.376 0-17.047-14.452-9.2642-20.011-27.793-20.011-14.637 0-24.087 9.6348-9.4498 9.6347-9.4498 26.866 0 33.907 35.019 33.907 3.705 0 8.5231-0.74103 8.3384-1.1108 12.97-1.1108 11.302 0 11.302 6.4849 0 7.2261-11.488 7.2261-4.0749 0-12.229-1.2972-6.1147-1.1108-9.4498-1.1108-37.057 0-37.057 37.798 0 18.343 9.8203 29.646 9.8203 11.117 27.422 11.117 22.049 0 29.275-22.79 3.705-12.044 8.1522-16.676 4.6326-4.632 12.229-4.632 6.2996 0 11.302 4.632 5.1905 4.4467 5.1905 11.488 0 16.861-18.899 27.978-18.899 10.932-45.766 10.932-29.46 0-52.435-14.082-22.79-14.082-22.79-37.613 0-29.46 45.395-43.357z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.ZETA:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_zeta.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m182.03 28.42 2.9652 6.6704q-18.343 7.5966-18.343 21.678 0 9.8202 6.6701 15.008 6.8551 5.1882 15.564 5.1882 0.92746 0 2.7772-0.18798 13.341-14.082 32.24-26.866 18.899-12.785 30.016-12.785 8.5231 0 8.5231 6.8554 0 12.229-17.417 24.272-17.417 11.858-48.36 16.676-50.027 51.324-50.027 120.62 0 28.534 11.302 42.801 11.302 14.082 40.022 14.082 3.153 0 14.452-0.74104 12.785-0.55772 17.417-0.55772 21.678 0 31.128 14.082 9.6347 14.082 9.6347 34.093 0 29.275-14.823 46.136-14.823 17.046-40.577 17.046-24.273 0-24.273-16.305 0-12.785 12.97-12.785 3.705 0 13.896 3.1501 8.5233 2.7791 15.193 2.7791 11.488 0 18.158-9.079 6.8557-8.8936 6.8557-20.196 0-12.599-7.4111-18.343-7.4117-5.7436-24.458-5.7436-3.8928 0-18.899 1.1108-6.8551 0.36974-11.302 0.36974-66.517 0-66.517-80.784 0-74.485 54.103-131.74-13.897-0.36974-23.161-7.2261-9.0787-6.8556-9.0787-19.826 0-21.308 30.757-29.46z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.ETA:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_eta.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m180.26 152.38q29.09-36.501 57.068-36.501 43.727 0 43.727 64.294v137.48q0 35.204 7.0412 54.103h-31.313q-6.2996-17.417-6.2996-63.738v-131.92q0-19.084-5.9292-28.163-5.929-9.2643-20.752-9.2643-22.234 0-43.542 24.643v127.29h-30.572v-127.29q0-17.231-3.5172-23.716-3.3351-6.4849-11.488-6.4849-13.155 0-16.12 25.94h-6.6702q3.5229-43.172 35.575-43.172 14.267 0 23.346 10.006 9.0793 9.82 9.4498 26.496z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.THETA:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_theta.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m201.67 27.494q31.313 0 52.806 36.686 21.493 36.501 21.493 95.237 0 63.367-23.161 99.869-23.16 36.501-53.547 36.501-29.831 0-52.621-35.389-22.605-35.575-22.605-96.348 0-60.959 22.42-98.757 22.605-37.798 55.215-37.798zm39.837 127.85q0-117.1-41.134-117.1-42.245 0-42.245 117.1zm-83.379 11.488q0 60.588 11.303 89.493 11.302 28.719 30.387 28.719 41.318 0 41.689-118.21z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.IOTA:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_iota.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m241.78 253.73h6.6702q-3.517 42.06-35.575 42.06-11.302 0-19.454-6.1145-7.9678-6.2996-10.747-14.082-2.5952-7.9671-2.5952-27.422v-61.329q0-29.646-2.2254-37.983-2.2253-8.3378-11.117-8.3378-5.1905 0-12.599 2.779l-2.5952-6.6702 51.139-20.752h8.1522v133.78q0 16.49 3.153 22.605 3.1471 6.1144 11.488 6.1144 12.599 0 16.305-24.643z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 5

            case constants.KAPPA:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_kappa.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m164.61 115.87v80.97l48.174-50.953q28.719-30.016 53.918-30.016 9.8202 0 15.749 4.6322 6.1147 4.6322 6.1147 12.044 0 7.2261-4.8147 11.488-4.6328 4.2615-10.746 4.2615-5.3726 0-14.267-4.8176-8.8936-4.8176-13.711-4.8176-9.6347 0-21.308 12.599l-32.425 35.019 61.144 76.708q15.935 20.011 42.245 20.752v6.8556h-60.032l-70.038-90.975v90.975h-30.757v-103.76q0-30.572-2.4074-38.354-2.4074-7.9673-10.932-7.9673-5.1905 0-12.599 2.7791l-2.5953-6.6704 51.139-20.752z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 3

            case constants.LAMBDA:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_lambda.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m283.93 237.24h6.6701q0 29.275-9.6347 42.616-9.4498 13.34-23.717 13.34-11.673 0-22.42-8.7085-10.746-8.8936-19.269-47.248l-15.935-71.891-55.215 125.25h-35.019l79.302-170.83q-6.2996-33.166-15.193-49.101-8.8936-15.934-22.048-15.934-10.561 0-18.528 8.1525-7.7823 7.9673-8.7088 24.828h-6.6701q0.5282-27.237 10.932-43.542 10.376-16.49 25.94-16.49 10.005 0 18.899 8.3378 9.0788 8.1526 15.564 28.163 6.6702 19.826 20.567 82.452l13.155 58.735q7.9673 36.501 16.676 48.915 8.893 12.229 21.122 12.229 20.751 0 23.531-29.275z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.MU:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_mu.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m222.51 259.84q-33.536 35.945-58.365 35.945-15.934 0-29.645-12.229v9.8202q0 17.046 5.1846 34.278 5.9292 19.084 5.9292 25.199 0 8.523-5.3726 14.082-5.3724 5.5587-13.34 5.5587-8.1526 0-12.97-6.4849-4.8148-6.4849-4.8148-15.564 0-6.6704 4.8148-24.087 5.5604-19.27 5.5604-37.428v-168.05h30.572v109.87q0 16.676 2.7772 24.458 2.9652 7.7821 10.191 12.785 7.4117 4.8176 16.676 4.8176 16.49 0 42.801-22.605v-129.33h30.757v128.77q0 16.305 3.3351 22.605 3.335 6.1145 11.303 6.1145 12.599 0 16.305-24.643h6.6702q-3.5229 42.06-35.575 42.06-13.896 0-23.161-9.2643-9.0787-9.4495-9.6347-26.681z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.NU:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_nu.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m198.15 295.79-40.948-121.55q-4.0749-12.043-10.747-23.716-6.6701-11.673-18.343-11.673-5.5606 0-12.229 2.4086l-2.5952-6.4851 46.136-18.899h8.1522l48.73 142.48 30.201-61.7q8.3383-16.676 8.3383-26.125 0-7.5968-3.153-21.308-2.4074-10.005-2.4074-15.008 0-18.343 19.826-18.343 17.602 0 17.602 16.676 0 16.49-24.458 62.997l-52.991 100.24z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.XI:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_xi.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m178.04 27.679v7.0408q-18.158 2.5941-18.158 15.935 0 14.452 20.752 18.528 11.858-12.785 27.978-22.419 16.12-9.8202 28.719-9.8202 9.4498 0 9.4498 8.5231 0 11.302-18.529 22.234-18.528 10.932-44.283 11.302-15.193 15.379-15.193 32.61 0 18.158 17.787 29.831 26.681-14.638 56.327-14.638 20.381 0 20.381 10.191 0 6.8556-10.746 11.673-10.747 4.8176-30.943 4.8176-16.861 0-32.795-2.4084-48.73 31.128-48.73 70.593 0 17.417 12.229 28.904 12.229 11.488 39.651 11.488 4.8204 0 12.97-0.55771 21.308-1.6676 28.719-1.6676 22.419 0 32.61 14.452 10.191 14.452 10.191 36.131 0 30.387-16.675 46.136-16.676 15.935-37.613 15.935-11.117 0-18.343-4.6322-7.2262-4.4471-7.2262-12.229 0-5.5587 3.705-8.8936 3.8928-3.3351 8.7082-3.3351 3.3351 0 9.4498 2.0381 11.487 3.7055 18.343 3.7055 12.599 0 19.826-8.7083 7.2262-8.7085 7.2262-21.864 0-9.2643-5.5604-16.49-5.5604-7.0409-18.158-7.0409-5.5604 0-13.34 0.36974-23.161 1.2972-30.943 1.2972-32.981 0-52.621-19.27-19.64-19.27-19.64-49.471 0-47.433 52.251-79.487-18.899-15.008-18.899-34.278 0-18.158 15.935-36.131-26.496-6.6702-26.496-27.052 0-22.79 31.684-23.346z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.OMICRON:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_omicron.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m200.19 115.87q38.539 0 61.885 29.275 19.825 25.014 19.825 57.438 0 22.79-10.932 46.136-10.932 23.346-30.201 35.204-19.084 11.858-42.615 11.858-38.354 0-60.959-30.572-19.084-25.755-19.084-57.809 0-23.346 11.488-46.321 11.673-23.161 30.572-34.092 18.899-11.117 40.022-11.117zm-5.7425 12.044q-9.8203 0-19.826 5.929-9.8202 5.7437-15.935 20.381-6.1142 14.638-6.1142 37.613 0 37.057 14.637 63.923 14.823 26.866 38.91 26.866 17.972 0 29.646-14.823 11.673-14.823 11.673-50.953 0-45.21-19.455-71.15-13.155-17.787-33.536-17.787z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.PI:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_pi.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m290.51 120.88v27.052h-42.986l-3.705 56.327q-1.1092 14.638-1.1092 25.384 0 25.755 5.9292 31.498 6.1147 5.5586 14.638 5.5586 17.787 0 21.123-22.42h6.6701q-6.1147 51.509-41.133 51.509-16.305 0-26.31-10.005-9.8203-10.005-9.8203-29.646 0-12.97 3.8928-54.844l5.0027-53.362h-39.281q-3.8928 67.444-9.4497 98.572-5.3726 31.128-12.043 40.207-6.4852 9.079-17.787 9.079-8.5233 0-14.452-5.0026-5.7425-5.0026-5.7425-13.155 0-7.782 10.005-21.308 14.637-19.64 21.863-40.763 7.2262-21.308 10.932-67.629h-12.599q-15.194 0-23.346 6.8555-7.9671 6.6703-15.193 19.27h-6.6712q5.3726-19.826 13.897-32.61 8.5227-12.785 17.416-16.676 9.0793-3.8911 32.054-3.8911z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.RHO:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_rho.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m151.73 371.75h-31.684q6.8557-21.308 6.8557-64.479v-104.5q0-44.283 25.014-65.591 25.013-21.308 55.215-21.308 32.795 0 52.806 22.605 20.01 22.419 20.01 58.921 0 39.836-24.828 69.111-24.828 29.275-56.697 29.275-21.493 0-40.948-13.711v24.272q0 38.725-5.7423 65.406zm5.7425-132.66q0 22.419 11.858 34.278 11.858 11.673 30.202 11.673 21.678 0 36.13-18.529 14.637-18.714 14.637-49.286 0-38.725-19.826-61.329-19.825-22.605-44.098-22.605-16.49 0-22.79 10.376-6.1147 10.191-6.1147 33.351z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.SIGMA | constants.SIGMA1:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_sigma1.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m291.99 120.88v27.052h-72.261q23.716 13.526 38.725 34.278 15.008 20.567 15.008 43.727 0 30.201-23.902 50.027-23.716 19.826-53.918 19.826-35.76 0-61.699-27.978-25.94-28.163-25.94-65.406 0-26.31 13.526-46.506 13.711-20.196 31.684-27.608 18.158-7.4114 48.915-7.4114zm-84.675 27.052h-6.4852q-27.793 0-44.468 13.896-16.49 13.711-16.49 43.172 0 31.313 17.416 55.4 17.417 23.902 40.763 23.902 18.713 0 30.942-17.973 12.229-18.158 12.229-43.727 0-40.577-33.907-74.67z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.SIGMA2:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_sigma2.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m134.04 224.27q0-45.58 27.607-76.893 27.793-31.499 65.776-31.499 17.973 0 27.237 6.2997 9.2643 6.1144 9.2643 15.193 0 5.5587-4.2629 9.2643-4.0749 3.7055-9.2642 3.7055-6.8557 0-19.826-4.8176-15.193-5.5585-25.199-5.5585-26.496 0-41.69 22.419-15.193 22.234-15.193 53.177 0 22.605 11.488 34.278 11.673 11.673 39.837 11.673 7.9671 0 16.861-0.36974 7.5968-0.18798 9.8203-0.18798 20.751 0 30.016 13.34 9.4492 13.155 9.4492 33.907 0 28.719-15.564 46.507-15.379 17.787-40.022 17.787-24.643 0-24.643-16.49 0-12.043 11.858-12.043 4.0749 0 18.158 3.8911 6.2996 1.853 10.376 1.853 8.8936 0 17.602-7.9673 8.8938-7.9673 8.8938-23.902 0-22.79-20.382-22.79-3.705 0-8.8938 0.36974-15.564 1.2972-22.79 1.2972-29.46 0-47.989-19.27-18.528-19.455-18.528-53.177z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.TAU:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_tau.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m217.7 147.93-5.3726 53.177q-1.2972 13.896-1.2972 27.793 0 26.496 6.1147 32.24 6.2997 5.5587 14.267 5.5587 17.787 0 21.123-22.42h6.8557q-6.1147 51.509-40.948 51.509-36.501 0-36.501-41.874 0-21.122 4.0749-52.621l6.8557-53.362h-18.343q-15.193 0-23.716 5.1882-8.3378 5.0027-15.564 20.381h-6.6702q5.9292-20.381 14.081-32.24 8.1528-12.044 15.564-16.12 7.4117-4.2616 22.049-4.2616h91.16v27.052z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.UPSILON:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_upsilon.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m221.68 115.87q33.537 4.0763 49.471 28.349 16.12 24.272 16.12 56.141 0 39.095-23.346 67.258-23.346 28.163-55.771 28.163-17.973 0-32.795-9.6349-14.823-9.8202-19.825-23.716-5.0026-13.896-5.0026-39.095v-61.329q0-16.676-3.153-22.79-3.1471-6.1145-11.673-6.1145-12.414 0-16.306 24.828h-6.67q2.4074-42.06 36.131-42.06 11.487 0 18.899 5.9292 7.5965 5.929 10.376 13.711 2.9651 7.5967 2.9651 27.978v62.256q0 21.864 2.4075 32.981 2.5951 10.932 11.303 17.973 8.8938 7.0409 19.455 7.0409 17.787 0 28.719-20.567 10.932-20.752 10.932-62.441 0-37.242-8.1528-54.845-8.1528-17.787-25.199-23.346z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.PHI:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_phi.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m178.41 115.87v6.6704q-40.948 10.561-40.948 77.449 0 72.447 50.954 85.231v-107.65q0-23.531 2.9651-34.278 2.9652-10.932 12.97-19.084 10.191-8.3378 24.458-8.3378 25.014 0 46.321 23.531 21.493 23.531 21.493 61.329 0 35.389-22.048 63.182-21.864 27.793-66.147 31.684v76.152h-20.011v-76.152q-38.539-3.3351-61.885-28.719-23.161-25.569-23.161-66.332 0-36.686 21.123-59.847 21.123-23.346 53.918-24.828zm30.016 169.35q58.365-8.7083 58.365-75.411 0-30.757-12.599-51.509-12.414-20.937-29.275-20.937-6.1141 0-10.376 4.4467-4.0749 4.2616-5.1905 10.191-0.92746 5.9292-0.92746 23.346z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.CHI:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_chi.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m240.95 120.88h32.425l-67.444 132.66 12.229 51.695q6.1147 25.755 14.082 32.61 8.1528 6.8556 19.64 6.8556 27.052 0 28.905-31.498h6.8557q-0.35265 27.607-10.747 43.357-10.376 15.935-27.978 15.935-15.378 0-24.458-9.8202-9.0787-9.82-16.119-38.91l-12.229-51.509-49.471 99.498h-32.425l71.705-142.48-10.376-43.727q-5.7425-23.902-11.488-32.24-5.7425-8.5231-17.972-8.5231-21.678 0-26.866 32.981h-6.8556q0-25.94 8.8936-42.616 9.0787-16.861 26.866-16.861 15.379 0 22.976 11.302 7.7816 11.302 14.823 40.948l9.6348 40.022z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.PSI:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_psi.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m210.1 284.67q19.641-5.7436 27.978-22.049 8.5231-16.49 13.34-63.738 4.0749-38.725 7.0412-51.695 3.1471-13.155 12.229-20.937 9.0787-7.9673 23.902-7.9673 8.7088 0 18.899 2.5941v7.0409q-2.0375-0.18798-3.5229-0.18798-7.9673 0-13.526 9.6348-5.5606 9.6348-9.6348 48.174-3.8928 34.278-8.7088 48.915-4.6326 14.452-15.193 28.534-10.376 13.896-22.975 20.937-12.599 7.0409-29.831 10.561v77.264h-20.196v-77.264q-17.972-3.7055-30.942-11.302-12.97-7.5968-22.791-21.308-9.6347-13.896-14.452-28.163-4.6326-14.452-8.7088-51.139-3.8928-35.945-9.4492-45.395-5.5604-9.4495-13.341-9.4495-1.6676 0-3.705 0.18798v-7.0409q10.191-2.5941 18.899-2.5941 14.638 0 23.716 7.9673 9.0793 7.7819 12.414 20.937 3.5229 12.97 6.4846 46.692 5.0027 55.215 14.452 70.408 9.6348 15.193 27.422 20.381v-166.39h20.196z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 4

            case constants.OMEGA:
                # https://commons.wikimedia.org/wiki/File:Greek_lc_omega.svg
                elem = Element(
                    "path",
                    transform=f"translate({N(x)}, {N(y)}) scale({N(1.3*self.size/400)}) translate(-200,-200)",
                    d="m200.28 259.1q-16.119 36.686-49.286 36.686-23.161 0-42.616-21.308-19.27-21.493-19.27-61.7 0-32.981 11.488-53.733 11.673-20.937 30.387-32.054 18.713-11.117 49.841-11.117v6.8556q-27.422 0-42.616 22.605-15.194 22.605-15.194 64.109 0 42.06 9.8203 57.624 10.005 15.564 23.531 15.564 8.7088 0 16.861-5.3732 8.3383-5.373 11.673-11.302 3.3351-6.1144 10.191-24.828-11.673-24.458-11.673-51.694 0-41.319 16.861-41.319 16.861 0 16.861 38.169 0 26.311-12.229 54.844 13.341 41.504 38.169 41.504 13.896 0 23.902-14.452 10.191-14.638 10.191-55.03 0-33.722-6.6701-51.509-6.4852-17.973-19.455-27.978-12.97-10.191-31.684-10.932v-6.8556q31.128 0 49.842 11.302 18.714 11.302 30.201 31.869 11.488 20.567 11.488 53.177 0 40.763-18.713 62.256-18.528 21.308-43.357 21.308-34.092 0-48.545-36.686z",
                    fill=self.color,
                    stroke="none",
                )
                self.label_x_offset = self.size / 3

            case constants.NONE:
                elem = Element("g", fill=self.color, stroke="none")
                self.label_x_offset = 0

            case _:
                if len(self.marker) != 1:
                    raise NotImplementedError(self.marker)
                elem = Element(
                    "text",
                    self.marker,
                    x=N(x),
                    y=N(y + self.size / 3.5),
                    fill=self.color,
                    stroke="none",
                )
                elem["font-family"] = "sans-serif"
                elem["font-weight"] = "bold"
                elem["text-anchor"] = "middle"
                elem["font-size"] = self.size
                self.label_x_offset = self.size / 3

        elem["class"] = f"marker {self.marker}"
        if self.opacity is not None and self.opacity != 1:
            elem["opacity"] = N(self.opacity)
        if self.href:
            elem = Element("a", elem, href=self.href)

        return elem
