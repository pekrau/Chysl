"Charts defined in YAML for rendering into SVG. Charts can be combined in different ways."

VERSION = (0, 5, 1)
__version__ = ".".join([str(n) for n in VERSION])

SVG_XMLNS = "http://www.w3.org/2000/svg"
SVG_CONTENT_TYPE = "image/svg+xml"
YAML_CONTENT_TYPE = "application/yaml"

JSONSCHEMA_ID = "https://github.com/pekrau/Chysl/blob/main/docs/schema.json"
JSONSCHEMA_VERSION = "https://json-schema.org/draft/2020-12/schema"

CHARTS = [
    "timelines",
    "piechart",
    "scatter2d",
    "lines2d",
    "note",
    "column",
    "row",
    "overlay",
    "board",
]

REL_TOL = 0.00005
ABS_TOL = 0.0005

FORMATS = ["csv", "tsv", "json", "yaml"]

DEFAULT_LINE_WIDTH = 1
DEFAULT_PADDING = 0
DEFAULT_ANCHOR = "middle"
DEFAULT_PLACEMENT = "center"
DEFAULT_FONT_FAMILY = "sans-serif"
DEFAULT_FONT_SIZE = 12
DEFAULT_TITLE_FONT_SIZE = 16
FONT_DESCEND = 0.3  # Empirical factor.

# See: https://austingil.com/css-named-colors/#bold
DEFAULT_PALETTE = [
    "tomato",
    "darkviolet",
    "deeppink",
    "deepskyblue",
    "gold",
    "yellowgreen",
]

BOTTOM = "bottom"
MIDDLE = "middle"
TOP = "top"
VERTICAL = [BOTTOM, MIDDLE, TOP]

LEFT = "left"
CENTER = "center"
RIGHT = "right"
HORIZONTAL = [LEFT, CENTER, RIGHT]

# XXX Add: above, below, left-above, left-below, right-above, right-below.
PLACEMENTS = [LEFT, CENTER, RIGHT]

# Markers
DISC = "disc"
CIRCLE = "circle"
OVAL = "oval"
OVAL_V = "oval-vertical"
OVAL_H = "oval-horizontal"
ELLIPSE = "ellipse"
ELLIPSE_V = "ellipse-vertical"
ELLIPSE_H = "ellipse-horizontal"
BLOCK = "block"
SQUARE = "square"
SQUARE_CROSS = "square-cross"
DIAMOND = "diamond"
DIAMOND_CROSS = "diamond-cross"
DIAMOND_F = "diamond-fill"
PYRAMID = "pyramid"
TRIANGLE = "triangle"
WEDGE = "wedge"
TRIGON = "trigon"
PENTAGON = "pentagon"
PENTAGON_F = "pentagon-fill"
HEXAGON = "hexagon"
HEXAGON_F = "hexagon-fill"
HEPTAGON = "heptagon"
HEPTAGON_F = "heptagon-fill"
OCTAGON = "octagon"
OCTAGON_F = "octagon-fill"
GEOMETRY_MARKERS = [
    DISC,
    CIRCLE,
    OVAL,
    OVAL_V,
    OVAL_H,
    ELLIPSE,
    ELLIPSE_V,
    ELLIPSE_H,
    BLOCK,
    SQUARE,
    SQUARE_CROSS,
    DIAMOND,
    DIAMOND_CROSS,
    DIAMOND_F,
    PYRAMID,
    TRIANGLE,
    WEDGE,
    TRIGON,
    PENTAGON,
    PENTAGON_F,
    HEXAGON,
    HEXAGON_F,
    HEPTAGON,
    HEPTAGON_F,
    OCTAGON,
    OCTAGON_F,
]
CROSS = "cross"
PLUS = "plus"
MINUS = "minus"
BAR = "bar"
CHECK = "check"
BURST = "burst"
INFINITY = "infinity"
NONE = "none"
SYMBOL_MARKERS = [
    CROSS,
    PLUS,
    MINUS,
    BAR,
    CHECK,
    BURST,
    INFINITY,
    NONE,
]
STAR = "star"
STAR_F = "star-fill"
GALAXY = "galaxy"
SUN = "sun"
MERCURY = "mercury"
VENUS = "venus"
EARTH = "earth"
MOON = "moon"
MARS = "mars"
JUPITER = "jupiter"
SATURN = "saturn"
URANUS = "uranus"
NEPTUNE = "neptune"
ASTRONOMY_MARKERS = [
    STAR,
    STAR_F,
    GALAXY,
    SUN,
    MERCURY,
    VENUS,
    EARTH,
    MOON,
    MARS,
    JUPITER,
    SATURN,
    URANUS,
    NEPTUNE,
]
ALPHA = "alpha"
BETA = "beta"
GAMMA = "gamma"
DELTA = "delta"
EPSILON = "epsilon"
ZETA = "zeta"
ETA = "eta"
THETA = "theta"
IOTA = "iota"
KAPPA = "kappa"
LAMBDA = "lambda"
MU = "mu"
NU = "nu"
XI = "xi"
OMICRON = "omicron"
PI = "pi"
RHO = "rho"
SIGMA = "sigma"
SIGMA1 = "sigma1"
SIGMA2 = "sigma2"
TAU = "tau"
UPSILON = "upsilon"
PHI = "phi"
CHI = "chi"
PSI = "psi"
OMEGA = "omega"
GREEK_MARKERS = [
    ALPHA,
    BETA,
    GAMMA,
    DELTA,
    EPSILON,
    ZETA,
    ETA,
    THETA,
    IOTA,
    KAPPA,
    LAMBDA,
    MU,
    NU,
    XI,
    OMICRON,
    PI,
    RHO,
    SIGMA,
    SIGMA1,
    SIGMA2,
    TAU,
    UPSILON,
    PHI,
    CHI,
    PSI,
    OMEGA,
]
MARKERS = GEOMETRY_MARKERS + SYMBOL_MARKERS + ASTRONOMY_MARKERS + GREEK_MARKERS

ERROR = "error"
WEDGE = "wedge"
GRADIENT = "gradient"
FUZZY_MARKERS = [ERROR, WEDGE, GRADIENT, NONE]

# Measured using Tkinter and 100pt characters in FreeSans, FreeSerif and FreeMono.
CHARACTER_WIDTHS = {
    "sans": {
        "a": {"n": 72, "i": 74, "b": 75, "ib": 74},
        "b": {"n": 75, "i": 75, "b": 83, "ib": 81},
        "c": {"n": 67, "i": 69, "b": 74, "ib": 74},
        "d": {"n": 75, "i": 74, "b": 83, "ib": 81},
        "e": {"n": 71, "i": 73, "b": 78, "ib": 74},
        "f": {"n": 37, "i": 35, "b": 46, "ib": 44},
        "g": {"n": 73, "i": 74, "b": 82, "ib": 81},
        "h": {"n": 71, "i": 72, "b": 81, "ib": 81},
        "i": {"n": 30, "i": 30, "b": 37, "ib": 37},
        "j": {"n": 32, "i": 32, "b": 37, "ib": 37},
        "k": {"n": 69, "i": 67, "b": 75, "ib": 74},
        "l": {"n": 29, "i": 30, "b": 36, "ib": 37},
        "m": {"n": 108, "i": 109, "b": 119, "ib": 119},
        "n": {"n": 72, "i": 72, "b": 82, "ib": 81},
        "o": {"n": 71, "i": 74, "b": 82, "ib": 81},
        "p": {"n": 75, "i": 75, "b": 83, "ib": 81},
        "q": {"n": 75, "i": 74, "b": 83, "ib": 81},
        "r": {"n": 44, "i": 43, "b": 52, "ib": 52},
        "s": {"n": 66, "i": 66, "b": 74, "ib": 74},
        "t": {"n": 37, "i": 35, "b": 45, "ib": 44},
        "u": {"n": 72, "i": 72, "b": 82, "ib": 81},
        "v": {"n": 66, "i": 66, "b": 72, "ib": 74},
        "w": {"n": 96, "i": 96, "b": 104, "ib": 104},
        "x": {"n": 63, "i": 65, "b": 73, "ib": 74},
        "y": {"n": 64, "i": 64, "b": 73, "ib": 74},
        "z": {"n": 65, "i": 67, "b": 68, "ib": 67},
        "A": {"n": 89, "i": 89, "b": 93, "ib": 96},
        "B": {"n": 89, "i": 89, "b": 94, "ib": 96},
        "C": {"n": 95, "i": 95, "b": 96, "ib": 96},
        "D": {"n": 93, "i": 94, "b": 97, "ib": 96},
        "E": {"n": 84, "i": 88, "b": 89, "ib": 89},
        "F": {"n": 80, "i": 80, "b": 84, "ib": 81},
        "G": {"n": 102, "i": 104, "b": 104, "ib": 104},
        "H": {"n": 96, "i": 96, "b": 100, "ib": 96},
        "I": {"n": 37, "i": 37, "b": 41, "ib": 37},
        "J": {"n": 70, "i": 68, "b": 76, "ib": 74},
        "K": {"n": 90, "i": 89, "b": 97, "ib": 96},
        "L": {"n": 75, "i": 74, "b": 83, "ib": 81},
        "M": {"n": 113, "i": 113, "b": 116, "ib": 111},
        "N": {"n": 97, "i": 97, "b": 100, "ib": 96},
        "O": {"n": 105, "i": 103, "b": 104, "ib": 104},
        "P": {"n": 87, "i": 86, "b": 90, "ib": 89},
        "Q": {"n": 105, "i": 103, "b": 104, "ib": 104},
        "R": {"n": 95, "i": 95, "b": 96, "ib": 96},
        "S": {"n": 89, "i": 87, "b": 91, "ib": 89},
        "T": {"n": 84, "i": 81, "b": 86, "ib": 81},
        "U": {"n": 96, "i": 96, "b": 98, "ib": 96},
        "V": {"n": 86, "i": 86, "b": 88, "ib": 89},
        "W": {"n": 125, "i": 125, "b": 128, "ib": 126},
        "X": {"n": 88, "i": 89, "b": 90, "ib": 89},
        "Y": {"n": 90, "i": 90, "b": 86, "ib": 89},
        "Z": {"n": 82, "i": 81, "b": 81, "ib": 81},
        "0": {"n": 74, "i": 74, "b": 74, "ib": 74},
        "1": {"n": 74, "i": 74, "b": 74, "ib": 74},
        "2": {"n": 74, "i": 74, "b": 74, "ib": 74},
        "3": {"n": 74, "i": 74, "b": 74, "ib": 74},
        "4": {"n": 74, "i": 74, "b": 74, "ib": 74},
        "5": {"n": 74, "i": 74, "b": 74, "ib": 74},
        "6": {"n": 74, "i": 74, "b": 74, "ib": 74},
        "7": {"n": 74, "i": 74, "b": 74, "ib": 74},
        "8": {"n": 74, "i": 74, "b": 74, "ib": 74},
        "9": {"n": 74, "i": 74, "b": 74, "ib": 74},
        "!": {"n": 44, "i": 37, "b": 44, "ib": 44},
        '"': {"n": 44, "i": 47, "b": 63, "ib": 63},
        "#": {"n": 74, "i": 74, "b": 74, "ib": 74},
        "$": {"n": 74, "i": 74, "b": 74, "ib": 74},
        "%": {"n": 119, "i": 119, "b": 119, "ib": 119},
        "&": {"n": 89, "i": 89, "b": 96, "ib": 96},
        "'": {"n": 27, "i": 25, "b": 33, "ib": 32},
        "(": {"n": 44, "i": 44, "b": 44, "ib": 44},
        ")": {"n": 44, "i": 44, "b": 44, "ib": 44},
        "*": {"n": 52, "i": 52, "b": 52, "ib": 52},
        "+": {"n": 78, "i": 78, "b": 78, "ib": 78},
        ",": {"n": 37, "i": 37, "b": 33, "ib": 37},
        "-": {"n": 44, "i": 44, "b": 44, "ib": 44},
        ".": {"n": 33, "i": 37, "b": 33, "ib": 37},
        "/": {"n": 37, "i": 37, "b": 37, "ib": 44},
        ":": {"n": 33, "i": 37, "b": 33, "ib": 44},
        ";": {"n": 33, "i": 37, "b": 33, "ib": 44},
        "<": {"n": 78, "i": 78, "b": 78, "ib": 78},
        "=": {"n": 78, "i": 78, "b": 78, "ib": 78},
        ">": {"n": 78, "i": 78, "b": 78, "ib": 78},
        "?": {"n": 74, "i": 74, "b": 81, "ib": 81},
        "@": {"n": 135, "i": 135, "b": 130, "ib": 130},
        "[": {"n": 37, "i": 37, "b": 44, "ib": 44},
        "\\": {"n": 37, "i": 37, "b": 37, "ib": 37},
        "]": {"n": 37, "i": 37, "b": 44, "ib": 44},
        "^": {"n": 63, "i": 63, "b": 78, "ib": 78},
        "_": {"n": 67, "i": 67, "b": 67, "ib": 74},
        "`": {"n": 44, "i": 44, "b": 44, "ib": 44},
        "{": {"n": 44, "i": 45, "b": 52, "ib": 52},
        "|": {"n": 33, "i": 35, "b": 37, "ib": 37},
        "}": {"n": 44, "i": 45, "b": 52, "ib": 52},
        "~": {"n": 67, "i": 78, "b": 67, "ib": 78},
        " ": {"n": 33, "i": 37, "b": 37, "ib": 37},
        "default": {
            "n": 69.6,
            "i": 69.87368421052632,
            "b": 73.3578947368421,
            "ib": 73.43157894736842,
        },
    },
    "sans-serif": {
        "a": {"n": 58, "i": 66, "b": 67, "ib": 68},
        "b": {"n": 67, "i": 63, "b": 73, "ib": 64},
        "c": {"n": 59, "i": 54, "b": 58, "ib": 57},
        "d": {"n": 67, "i": 67, "b": 74, "ib": 68},
        "e": {"n": 59, "i": 54, "b": 59, "ib": 56},
        "f": {"n": 50, "i": 57, "b": 52, "ib": 65},
        "g": {"n": 62, "i": 59, "b": 67, "ib": 65},
        "h": {"n": 66, "i": 67, "b": 74, "ib": 73},
        "i": {"n": 37, "i": 33, "b": 40, "ib": 39},
        "j": {"n": 46, "i": 40, "b": 51, "ib": 47},
        "k": {"n": 68, "i": 60, "b": 74, "ib": 68},
        "l": {"n": 34, "i": 33, "b": 37, "ib": 39},
        "m": {"n": 104, "i": 97, "b": 111, "ib": 102},
        "n": {"n": 65, "i": 66, "b": 74, "ib": 70},
        "o": {"n": 65, "i": 63, "b": 67, "ib": 63},
        "p": {"n": 67, "i": 63, "b": 73, "ib": 64},
        "q": {"n": 67, "i": 64, "b": 73, "ib": 66},
        "r": {"n": 46, "i": 49, "b": 57, "ib": 53},
        "s": {"n": 49, "i": 46, "b": 54, "ib": 47},
        "t": {"n": 38, "i": 33, "b": 45, "ib": 38},
        "u": {"n": 65, "i": 65, "b": 75, "ib": 71},
        "v": {"n": 62, "i": 61, "b": 64, "ib": 59},
        "w": {"n": 91, "i": 91, "b": 94, "ib": 87},
        "x": {"n": 64, "i": 58, "b": 68, "ib": 63},
        "y": {"n": 63, "i": 62, "b": 64, "ib": 58},
        "z": {"n": 56, "i": 52, "b": 59, "ib": 55},
        "A": {"n": 96, "i": 87, "b": 93, "ib": 93},
        "B": {"n": 84, "i": 79, "b": 88, "ib": 85},
        "C": {"n": 89, "i": 81, "b": 94, "ib": 83},
        "D": {"n": 96, "i": 94, "b": 97, "ib": 96},
        "E": {"n": 81, "i": 77, "b": 87, "ib": 84},
        "F": {"n": 75, "i": 77, "b": 82, "ib": 81},
        "G": {"n": 96, "i": 92, "b": 103, "ib": 94},
        "H": {"n": 95, "i": 94, "b": 104, "ib": 100},
        "I": {"n": 44, "i": 43, "b": 52, "ib": 50},
        "J": {"n": 51, "i": 57, "b": 67, "ib": 67},
        "K": {"n": 95, "i": 85, "b": 103, "ib": 88},
        "L": {"n": 81, "i": 76, "b": 87, "ib": 81},
        "M": {"n": 117, "i": 109, "b": 126, "ib": 117},
        "N": {"n": 97, "i": 90, "b": 97, "ib": 94},
        "O": {"n": 97, "i": 87, "b": 104, "ib": 90},
        "P": {"n": 77, "i": 75, "b": 85, "ib": 80},
        "Q": {"n": 96, "i": 87, "b": 104, "ib": 90},
        "R": {"n": 89, "i": 82, "b": 96, "ib": 89},
        "S": {"n": 71, "i": 61, "b": 76, "ib": 67},
        "T": {"n": 81, "i": 79, "b": 86, "ib": 79},
        "U": {"n": 96, "i": 94, "b": 97, "ib": 95},
        "V": {"n": 93, "i": 88, "b": 94, "ib": 94},
        "W": {"n": 126, "i": 118, "b": 131, "ib": 124},
        "X": {"n": 95, "i": 89, "b": 95, "ib": 93},
        "Y": {"n": 93, "i": 79, "b": 94, "ib": 85},
        "Z": {"n": 82, "i": 75, "b": 85, "ib": 75},
        "0": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "1": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "2": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "3": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "4": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "5": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "6": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "7": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "8": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "9": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "!": {"n": 44, "i": 44, "b": 44, "ib": 52},
        '"': {"n": 53, "i": 44, "b": 74, "ib": 74},
        "#": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "$": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "%": {"n": 107, "i": 111, "b": 107, "ib": 111},
        "&": {"n": 104, "i": 104, "b": 104, "ib": 104},
        "'": {"n": 27, "i": 27, "b": 37, "ib": 37},
        "(": {"n": 44, "i": 44, "b": 44, "ib": 44},
        ")": {"n": 44, "i": 44, "b": 44, "ib": 44},
        "*": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "+": {"n": 75, "i": 90, "b": 90, "ib": 90},
        ",": {"n": 33, "i": 33, "b": 33, "ib": 33},
        "-": {"n": 44, "i": 44, "b": 44, "ib": 44},
        ".": {"n": 33, "i": 33, "b": 33, "ib": 33},
        "/": {"n": 39, "i": 39, "b": 37, "ib": 45},
        ":": {"n": 33, "i": 33, "b": 44, "ib": 33},
        ";": {"n": 33, "i": 33, "b": 44, "ib": 33},
        "<": {"n": 75, "i": 76, "b": 90, "ib": 90},
        "=": {"n": 75, "i": 75, "b": 90, "ib": 90},
        ">": {"n": 75, "i": 76, "b": 90, "ib": 90},
        "?": {"n": 59, "i": 59, "b": 67, "ib": 67},
        "@": {"n": 115, "i": 104, "b": 124, "ib": 111},
        "[": {"n": 44, "i": 52, "b": 44, "ib": 44},
        "\\": {"n": 39, "i": 65, "b": 37, "ib": 53},
        "]": {"n": 44, "i": 52, "b": 44, "ib": 44},
        "^": {"n": 67, "i": 56, "b": 67, "ib": 76},
        "_": {"n": 67, "i": 67, "b": 67, "ib": 67},
        "`": {"n": 33, "i": 33, "b": 44, "ib": 44},
        "{": {"n": 44, "i": 44, "b": 53, "ib": 46},
        "|": {"n": 27, "i": 37, "b": 29, "ib": 36},
        "}": {"n": 44, "i": 44, "b": 53, "ib": 46},
        "~": {"n": 67, "i": 72, "b": 67, "ib": 76},
        " ": {"n": 33, "i": 33, "b": 33, "ib": 33},
        "default": {
            "n": 66.94736842105263,
            "i": 65.4421052631579,
            "b": 71.36842105263158,
            "ib": 68.84210526315789,
        },
    },
    "monospace": {"default": {"n": 80.0, "i": 80.0, "b": 80.0, "ib": 80.0}},
}
