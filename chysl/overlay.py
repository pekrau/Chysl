"Charts overlayed over one another, with optional opacity."

import constants
import schema
from chart import Chart, register, parse
from minixml import Element
from utils import N


class Overlay(Chart):

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart", "layers"],
        "additionalProperties": False,
        "properties": {
            "chart": {"const": "overlay"},
            "title": {"$ref": "#title"},
            "description": {"$ref": "#description"},
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
                        "opacity": {"$ref": "#opacity"},
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
        """Create the SVG elements in the 'svg' attribute.
        Adds the title, if defined.
        Sets the 'svg', 'height' and 'width' attributes.
        """
        for subchart, opacity in self.layers:
            subchart.build()

        self.width = max([s.width for s, o in self.layers])

        super().build()

        for subchart, opacity in self.layers:
            self.svg += Element(
                "g",
                subchart.svg,
                transform=f"translate(0,{N(self.total_height)})",
                opacity=opacity,
            )

        self.total_height += max([s.total_height for s, o in self.layers])


register(Overlay)
