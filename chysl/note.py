"Textual note with title, body and footer text."

import components
import constants
import schema
import utils
from chart import Chart, Layout, register
from minixml import Element
from path import Path
from utils import N


class NoteFrame(components.Frame):

    DEFAULT_THICKNESS = 5
    DEFAULT_COLOR = "gold"
    DEFAULT_RADIUS = 10


class Note(Chart):
    "Textual note with title, body and footer text."

    DEFAULT_WIDTH = 200
    DEFAULT_LINE = 1
    DEFAULT_BACKGROUND = "lightyellow"

    SCHEMA = {
        "title": __doc__,
        "type": "object",
        "required": ["chart"],
        "additionalProperties": False,
        "minProperties": 2,
        "properties": {
            "chart": {"const": "note"},
            "title": {
                "title": "Title of the note.",
                "$ref": "#text",
            },
            "body": {
                "title": "Body of the note.",
                "$ref": "#text",
            },
            "footer": {
                "title": "Footer of the note.",
                "$ref": "#text",
            },
            "description": {
                "title": "Description of the chart. Rendered as <desc> in SVG.",
                "type": "string",
            },
            "frame": {
                "title": "Specification of the note frame. Default is 5 pixels gold with radius 10.",
                "$ref": "#frame",
            },
            "line": {
                "title": "Thickness of lines between sections (pixels). Same color as frame.",
                "type": "number",
                "minimum": 0,
                "default": DEFAULT_LINE,
            },
            "background": {
                "title": "Background color of the note.",
                "type": "string",
                "format": "color",
                "default": DEFAULT_BACKGROUND,
            },
            "width": {
                "title": "Explicit width of note (pixels).",
                "type": "number",
                "minimumExclusive": 0,
            },
        },
    }

    schema.add_defs(SCHEMA)

    def __init__(
        self,
        title=None,  # Allow title, body, footer to be positional args.
        body=None,
        footer=None,
        description=None,  # Allow title, body, footer to be positional args.
        frame=True,
        line=None,
        background=None,
        width=None,
    ):
        super().__init__(title=title, description=description)
        assert body is None or isinstance(body, (str, dict))
        assert footer is None or isinstance(footer, (str, dict))
        assert isinstance(frame, (bool, dict))
        assert line is None or isinstance(line, (int, float))
        assert background is None or isinstance(background, str)
        assert width is None or isinstance(width, (int, float))

        self.body = components.Text(body)
        self.footer = components.Text(footer)
        self.frame = NoteFrame(frame)
        self.line = self.DEFAULT_LINE if line is None else line
        self.background = background or self.DEFAULT_BACKGROUND
        self.width = width

    def as_dict(self):
        result = super().as_dict()  # Deals with 'title'.
        result.update(self.body.as_dict("body"))
        result.update(self.footer.as_dict("footer"))
        result.update(self.frame.as_dict())
        if self.line != self.DEFAULT_LINE:
            result["line"] = self.line
        if self.background != self.DEFAULT_BACKGROUND:
            result["background"] = self.background
        if self.width:
            result["width"] = self.width
        return result

    def build(self):
        "Create the SVG elements in the 'svg' attribute."
        super().build()

        note = self.get_note()
        layout = Layout(rows=1, columns=1)
        layout.add(0, 0, self.frame.get_element(note.total_width, note.total_height))
        layout.add(0, 0, note)
        self.svg.load_layout(layout)

    def get_note(self):
        result = Element("g")
        result.total_width = self.width or 0
        result.total_height = 0

        if self.title:
            result += (title := self.title.get_element())
            if not self.width:
                result.total_width = max(result.total_width, title.total_width)

        if self.body:
            result += (body := self.body.get_element())
            if not self.width:
                result.total_width = max(result.total_width, body.total_width)

        if self.footer:
            result += (footer := self.footer.get_element())
            if not self.width:
                result.total_width = max(result.total_width, footer.total_width)

        if self.title:
            match self.title.placement:
                case constants.LEFT:
                    offset = 0
                case constants.CENTER:
                    offset = (result.total_width - title.total_width) / 2
                case constants.RIGHT:
                    offset = result.total_width - title.total_width
            title["transform"] = f"translate({N(offset)},0)"
            result.total_height += title.total_height

        if self.body:
            if self.title and self.line:
                result += (
                    line := Element(
                        "line",
                        x1=0,
                        y1=utils.N(result.total_height + self.line),
                        x2=utils.N(result.total_width),
                        y2=utils.N(result.total_height + self.line),
                        stroke=self.frame.color,
                    )
                )
                line["stroke-width"] = utils.N(self.line)
                result.total_height += self.line
            match self.body.placement:
                case constants.LEFT:
                    offset = 0
                case constants.CENTER:
                    offset = (result.total_width - body.total_width) / 2
                case constants.RIGHT:
                    offset = result.total_width - body.total_width
            body["transform"] = f"translate({N(offset)},{N(result.total_height)})"
            result.total_height += body.total_height

        if self.footer:
            if (self.title or self.body) and self.line:
                result += (
                    line := Element(
                        "line",
                        x1=0,
                        y1=utils.N(result.total_height + self.line),
                        x2=utils.N(result.total_width),
                        y2=utils.N(result.total_height + self.line),
                        stroke=self.frame.color,
                    )
                )
                line["stroke-width"] = utils.N(self.line)
                result.total_height += self.line
            match self.footer.placement:
                case constants.LEFT:
                    offset = 0
                case constants.CENTER:
                    offset = (result.total_width - footer.total_width) / 2
                case constants.RIGHT:
                    offset = result.total_width - footer.total_width
            footer["transform"] = f"translate({N(offset)},{N(result.total_height)})"
            result.total_height += footer.total_height

        return result


register(Note)
