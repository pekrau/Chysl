"2D chart plotting x/y data."

import constants
from chart import Chart
from dimension import Dimension
from path import Path
import utils


class Plot(Diagram):
    "2D chart plotting x/y data."

    DEFAULT_WIDTH = 600

    SCHEMA = {
        "title": __doc__,
        "$anchor": "plot",
        "type": "object",
        "required": ["entries"],
        "additionalProperties": False,
        "properties": {
            "title": {
                "title": "Title of the chart.",
                "$ref": "#text",
            },
            "width": {
                "title": "Width of chart, in pixels.",
                "type": "number",
                "default": DEFAULT_WIDTH,
                "exclusiveMinimum": 0,
            },
            "legend": {
                "title": "Display legend.",
                "type": "boolean",
                "default": True,
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
                "title": "Sets of data with visualization specifications.",
            },
        },
    }
