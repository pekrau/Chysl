"Graphical components with styling."

import constants
import utils
from minixml import Element


class Text:
    "Text with optional styling, possibly more than one line."

    DEFAULT_FONT = constants.DEFAULT_FONT_FAMILY
    DEFAULT_SIZE = constants.DEFAULT_FONT_SIZE
    DEFAULT_BOLD = False
    DEFAULT_ITALIC = False
    DEFAULT_COLOR = "black"
    DEFAULT_PLACEMENT = constants.CENTER

    def __init__(self, spec):
        assert spec is None or isinstance(spec, (str, dict))

        if isinstance(spec, dict):
            self.text = spec["text"]
            self.font = spec.get("font") or self.DEFAULT_FONT
            self.size = spec.get("size") or self.DEFAULT_SIZE
            self.bold = spec.get("bold") or self.DEFAULT_BOLD
            self.italic = spec.get("italic") or self.DEFAULT_ITALIC
            self.color = spec.get("color") or self.DEFAULT_COLOR
            self.placement = spec.get("placement") or self.DEFAULT_PLACEMENT
        else:
            self.text = spec
            self.font = self.DEFAULT_FONT
            self.size = self.DEFAULT_SIZE
            self.bold = self.DEFAULT_BOLD
            self.italic = self.DEFAULT_ITALIC
            self.color = self.DEFAULT_COLOR
            self.placement = self.DEFAULT_PLACEMENT

    def __str__(self):
        return self.text or ""

    def __bool__(self):
        return bool(self.text)

    def as_dict(self, key="text"):
        result = {}
        if not self:
            return result
        if self.font != self.DEFAULT_FONT:
            result["font"] = self.font
        if self.size != self.DEFAULT_SIZE:
            result["size"] = self.size
        if self.bold != self.DEFAULT_BOLD:
            result["bold"] = self.bold
        if self.italic != self.DEFAULT_ITALIC:
            result["italic"] = self.italic
        if self.color != self.DEFAULT_COLOR:
            result["color"] = self.color
        if self.placement != self.DEFAULT_PLACEMENT:
            result["placement"] = self.placement
        if result:
            result["text"] = self.text
            return {key: result}
        else:
            return {key: self.text}

    def get_element(self):
        """Return the SVG element for the text, with 'total_width', 'total_height'.
        Returns None if no text to display.
        """
        if not self:
            return None

        result = Element("g")
        result.total_width = 0
        result.total_height = 0
        result["fill"] = self.color
        result["font-family"] = self.font
        result["font-size"] = self.size
        if self.bold:
            result["font-weight"] = "bold"
        if self.italic:
            result["font-style"] = "italic"

        for line in self.text.split("\n"):
            result.total_height += self.size
            width = utils.get_text_width(
                line,
                size=self.size,
                bold=self.bold,
                italic=self.italic,
            )
            result.total_width = max(result.total_width, width)
            result += Element("text", line, y=utils.N(result.total_height))

        match self.placement:
            case constants.LEFT:
                pass
            case constants.CENTER:
                result["text-anchor"] = "middle"
                for text in result:
                    text["x"] = utils.N(result.total_width / 2)
            case constants.RIGHT:
                result["text-anchor"] = "end"
                for text in result:
                    text["x"] = utils.N(result.total_width)

        # Empirical factor 0.4
        result.total_height += self.size * (constants.FONT_DESCEND + 0.3)

        return result


class Title(Text):
    "Title text (larger default font size) with optional styling."

    DEFAULT_SIZE = constants.DEFAULT_TITLE_FONT_SIZE


class CompoundTitle(Title):
    "Title text for compound charts, with optional styling."

    DEFAULT_SIZE = 22
