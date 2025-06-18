"Charts overlayed over one another, with optional opacity."

import components
import constants
import schema
import utils
from chart import Chart, Layout, register, parse
from minixml import Element


class Overlay(Chart):
    "Charts overlayed over one another, with optional opacity."

    TITLE_CLASS = components.CompoundTitle

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "layers"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "overlay"},
            "title": {
                "title": "Title of the chart.",
                "$ref": "#text",
            },
            "description": {
                "title": "Description of the chart. Rendered as <desc> in SVG.",
                "type": "string",
            },
            "layers": {
                "title": "Charts to overlay, with optional opacity.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "title": "Chart as layer, with specified opacity.",
                    "type": "object",
                    "required": ["subchart"],
                    "additionalProperties": False,
                    "properties": {
                        "subchart": {"$ref": "#chart_or_include"},
                        "opacity": {
                            "title": "Opacity of the subchart.",
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                            "default": 1,
                        },
                    },
                },
            },
        },
    }

    schema.add_defs(SCHEMA)

    def __init__(
        self,
        title=None,
        description=None,
        layers=None,
    ):
        super().__init__(title=title, description=description)
        assert layers is None or isinstance(layers, list)

        self.layers = []
        if layers:
            for layer in layers:
                self.add(layer)

    def __iadd__(self, layer):
        self.add(layer)
        return self

    def add(self, layer):
        assert isinstance(layer, dict)
        self.add_layer(*[layer.get(key) for key in ["subchart", "opacity"]])

    def add_layer(self, subchart, opacity=None):
        assert isinstance(subchart, (dict, Chart))
        assert (
            opacity is None or isinstance(opacity, (int, float)) and 0 <= opacity <= 1
        )
        if isinstance(subchart, dict):
            subchart = parse(subchart)
        opacity = 1 if opacity is None else opacity
        self.layers.append([subchart, opacity])

    def as_dict(self):
        result = super().as_dict()
        result["layers"] = []
        for subchart, opacity in self.layers:
            result["layers"].append(layer := {})
            if opacity != 1:
                layer["opacity"] = opacity
            try:  # This subchart was included from another source.
                layer["subchart"] = dict(include=subchart.location)
            except AttributeError:
                layer["subchart"] = subchart.as_dict()
        return result

    def build(self):
        "Create the SVG elements in the 'svg' attribute."
        super().build()
        layout = Layout(rows=1, columns=1, title=self.title)

        for subchart, opacity in self.layers:
            subchart.build()
            element = Element("g", *list(subchart.svg))
            element["class"] = "layer"
            if opacity != 1:
                element["opacity"] = utils.N(opacity)
            element.total_width = subchart.svg.total_width
            element.total_height = subchart.svg.total_height
            layout.add(0, 0, element)

        self.svg.load_layout(layout)


register(Overlay)
