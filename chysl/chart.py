"Abstract Chart class."

import icecream

icecream.install()

import pathlib
import urllib.parse

import requests
import requests.exceptions
import yaml

import constants
import memo
import schema
import utils
from minixml import Element
from vector2 import Vector2
from utils import N


class Chart:
    "Abstract chart."

    def __init__(self, title=None, description=None):
        assert title is None or isinstance(title, (str, dict))
        assert description is None or isinstance(description, (str, dict))
        self.title = title
        self.description = description

    def __eq__(self, other):
        if not isinstance(other, Chart):
            return False
        if self.__class__ != other.__class__:
            return False
        return self.as_dict() == other.as_dict()

    @property
    def name(self):
        return self.__class__.__name__.casefold()

    def as_dict(self):
        result = {"chart": self.name}
        result.update(self.text_as_dict("title"))
        if self.description:
            result["description"] = self.description
        return result

    def text_as_dict(self, key):
        "Helper method to convert optionally styled text entry to dict."
        try:
            text = getattr(self, key)
        except AttributeError:
            return {}
        if not text:
            return {}
        if isinstance(text, str):
            return {key: text}
        result = {"text": text["text"]}
        if (
            size := text.get("size")
        ) is not None and size != constants.DEFAULT_TITLE_FONT_SIZE:
            result["size"] = size
        if text.get("bold"):
            result["bold"] = True
        if text.get("italic"):
            result["italic"] = True
        if (color := text.get("color")) is not None and color != "black":
            result["color"] = color
        if (
            anchor := text.get("anchor")
        ) is not None and anchor != constants.DEFAULT_ANCHOR:
            result["anchor"] = anchor
        if (
            placement := text.get("placement")
        ) is not None and placement != constants.DEFAULT_PLACEMENT:
            result["placement"] = placement
        return {key: result}

    def render(self, target=None, antialias=True, indent=2, restart_unique_id=False):
        """Render chart and return the SVG code.
        If target is provided, write into file given by path or open file object.
        """
        if restart_unique_id:
            utils.restart_unique_id()

        self.build()

        if antialias:
            extent = Vector2(self.svg.total_width + 1, self.svg.total_height + 1)
            transform = "translate(0.5, 0.5)"
        else:
            extent = Vector2(self.svg.total_width, self.svg.total_height)
            transform = None

        document = Element(
            "svg",
            xmlns=constants.SVG_XMLNS,
            width=N(extent.x),
            height=N(extent.y),
            viewBox=f"0 0 {N(extent.x)} {N(extent.y)}",
            transform=transform,
        )
        document.repr_indent = indent

        if self.title:
            if isinstance(self.title, dict):
                title = self.title["text"]
            else:
                title = self.title
            if title:
                document += Element("title", title)
        if self.description:
            document += Element("desc", self.description)

        for elem in self.svg:
            document += elem

        if isinstance(target, (str, pathlib.Path)):
            with open(target, "w") as outfile:
                outfile.write(repr(document))
        elif target is None:
            return repr(document)
        else:
            target.write(repr(document))

    def build(self):
        """Create and add the SVG elements to the 'svg' attribute.
        To be extended in subclasses.
        """
        self.svg = SvgContainer()

    def get_title(self):
        "Get the element for the title of the chart; possibly None."
        if not self.title:
            return None

        font = constants.DEFAULT_FONT_FAMILY
        if isinstance(self.title, dict):
            text = self.title["text"] or ""
            size = self.title.get("size") or constants.DEFAULT_TITLE_FONT_SIZE
            color = self.title.get("color") or "black"
            italic = self.title.get("italice") or False
            bold = self.title.get("bold") or False
        else:
            text = self.title
            size = constants.DEFAULT_TITLE_FONT_SIZE
            color = "black"
            italic = False
            bold = False
        # Empirical factor 0.3...
        result = Element("text", text, y=N(0.3 * size), fill=color)
        result["class"] = "title"
        result["text-anchor"] = "middle"
        result["font-family"] = font
        result["font-size"] = N(size)
        if italic:
            result["font-style"] = "italic"
        if bold:
            result["font-weight"] = "bold"
        result.total_height = size * (1 + constants.FONT_DESCEND)
        result.total_width = utils.get_text_length(
            text, size, font=font, italic=italic, bold=bold
        )
        return result

    def save(self, target=None):
        """Output the chart as YAML.
        If target is provided, write into file given by path or open file object.
        """
        data = self.as_dict()
        try:
            schema.validate(data, self.SCHEMA)
        except ValueError:
            with open("error.yaml", "w") as outfile:
                yaml.dump(data, outfile, allow_unicode=True, sort_keys=False)
            raise
        content = dict(chysl=constants.__version__)
        content.update(data)
        if isinstance(target, (str, pathlib.Path)):
            with open(target, "w") as outfile:
                yaml.dump(content, outfile, allow_unicode=True, sort_keys=False)
        elif target is None:
            return yaml.dump(content, allow_unicode=True, sort_keys=False)
        else:
            yaml.dump(content, outfile, allow_unicode=True, sort_keys=False)


class SvgContainer:
    "Helper container for SVG elements and total width and height."

    def __init__(self ):
        self.elements = []
        self.total_width = 0
        self.total_height = 0

    def __iadd__(self, element):
        assert isinstance(element, Element)
        self.elements.append(element)
        return self

    def __iter__(self):
        return iter(self.elements)

    def load_layout(self, layout):
        assert isinstance(layout, Layout)
        self += layout.element()
        self.total_width = max(self.total_width, layout.total_width)
        self.total_height = max(self.total_height, layout.total_height)


class Layout:
    """Grid-based helper for layouting SVG elements of a chart.
    XXX Implement this:
    It is assumed that all elements that are added are located in
    a bounding box between (0, 0, total_width, total_height).
    """

    class Cell:

        def __init__(self):
            self.elements = []
            self.width = 0
            self.height = 0

        def append(self, element):
            self.elements.append(element)
            self.width = max(self.width, element.total_width)
            self.height = max(self.height, element.total_height)

    def __init__(self, rows=1, columns=1, title=None, hpadding=None, vpadding=None):
        assert rows >= 1
        assert columns >= 1
        assert title is None or isinstance(title, Element)

        self.rows = rows
        self.columns = columns
        self.title = title
        self.hpadding = hpadding if hpadding is not None else constants.DEFAULT_PADDING
        self.vpadding = vpadding if vpadding is not None else constants.DEFAULT_PADDING
        self.cells = [[self.Cell() for column in range(columns)] for row in range(rows)]

    def add(self, row, column, element):
        "The element must have 'total_width' and 'total_height' attributes."
        if element is None:
            return
        assert hasattr(element, "total_width"), element
        assert hasattr(element, "total_height"), element
        self.cells[row][column].append(element)

    def element(self):
        "Return the 'g' element containint the layouted elements, including title."
        for row in range(self.rows):
            max_height = 0
            for column in range(self.columns):
                max_height = max(max_height, self.cells[row][column].height)
            for column in range(self.columns):
                self.cells[row][column].max_height = max_height
        for column in range(self.columns):
            max_width = 0
            for row in range(self.rows):
                max_width = max(max_width, self.cells[row][column].width)
            for row in range(self.rows):
                self.cells[row][column].max_width = max_width

        if self.title is not None:
            y = self.title.total_height
        else:
            y = 0

        result = Element("g")
        result["class"] = "layout"
        for row in range(self.rows):
            x = 0
            for column in range(self.columns):
                cell = self.cells[row][column]
                for element in cell.elements:
                    xt = x + cell.max_width / 2
                    yt = y + cell.max_height / 2
                    result += Element(
                        "g",
                        element,
                        transform=f"translate({N(xt)},{N(yt)})",
                    )
                x += cell.max_width + self.hpadding
                if column < self.columns - 1:
                    x += self.hpadding
            y += self.cells[row][0].max_height
            if row < self.rows - 1:
                y += self.vpadding

        if self.title is not None:
            result += Element(
                "g",
                self.title,
                transform=f"translate({N(x/2)},{N(self.title.total_height/2)})",
            )

        self.total_width = result.total_width = x
        self.total_height = result.total_height = y

        return result


# Lookup for Chart subclasses. Key: name of class (lower case); value: class
_chart_class_lookup = {}


def register(cls):
    "Register the chart for parsing."
    assert issubclass(cls, Chart)
    schema.check_schema(cls.SCHEMA)
    key = cls.__name__.casefold()
    if key in _chart_class_lookup:
        raise KeyError(f"chart '{key}' already registered")
    _chart_class_lookup[key] = cls


def get_chart_class(name):
    "Return the class for the chart name."
    return _chart_class_lookup[name]


def parse(data):
    "Parse the data dictionary and return the instance for the chart it describes."
    assert isinstance(data, dict), data
    if "include" in data:
        location = data["include"]
        reader = ChartReader(location)
        try:
            memo.check_add(reader)
            chart = reader.get_chart()
            chart.location = location  # Record the location for later output.
        except ValueError as error:
            raise ValueError(f"error reading from '{reader}': {error}")
        finally:
            memo.remove(reader)
    else:
        try:
            name = data.pop("chart")
        except KeyError:
            raise ValueError(f"no chart declaration in '{data}'")
        try:
            cls = get_chart_class(name)
        except KeyError:
            raise ValueError(f"no such chart '{name}'")
        chart = cls(**data)
    return chart


def retrieve(location):
    """Read and parse the YAML file given by its path or URI.
    Return a Chart instance.
    """
    reader = ChartReader(location)
    try:
        memo.check_add(reader)
        return reader.get_chart()
    except ValueError as error:
        raise ValueError(f"error reading from '{reader}': {error}")
    finally:
        memo.remove(reader)


class ChartReader:
    "Read the chart specification from a location; file path or href."

    def __init__(self, location):
        self.location = str(location)

    def __str__(self):
        return f"Reader('{self.location}')"

    def get_chart(self):
        """Read the data, parse as YAML, and return the instance of a Chart subclass.
        The meta information is stored in attribute 'meta'.
        If any of the following tests fail, raises ValueError:
        - The presence and validity of the 'chysl' format identification marker.
        - The compatibility of the version of the file, if given.
        - Check the data against the appropriate schema.
        """
        parts = urllib.parse.urlparse(self.location)
        if not parts.scheme or parts.scheme == "file":
            try:
                with open(self.location) as infile:
                    content = infile.read()
            except OSError as error:
                raise ValueError(str(error))
        else:  # Assume URL such as 'http' or 'https'.
            try:
                response = requests.get(self.location)
                response.raise_for_status()
                content = response.text
            except requests.exceptions.RequestException as error:
                raise ValueError(str(error))

        try:
            self.data = yaml.safe_load(content)
            if not isinstance(self.data, dict):
                raise ValueError("must contain a top-level mapping")
        except (yaml.YAMLError, ValueError) as error:
            raise ValueError(f"cannot interpret data as YAML: {error}")
        # Process and remove the meta information.
        try:
            self.meta = self.data.pop("chysl")
        except KeyError:
            raise ValueError(
                "YAML data lacks the Chysl format identifiation marker 'chysl'"
            )
        if self.meta:
            if isinstance(self.meta, dict):
                version = self.meta.get("version")
            else:
                version = self.meta
                self.meta = dict(version=version)
            # XXX Currently checks for strict equality.
            if version != constants.__version__:
                raise ValueError(f"YAML data incompatible version {version}")
        # Do schema validation on the incoming data.
        try:
            name = self.data["chart"]
        except KeyError:
            raise ValueError("no 'chart' defined in the YAML file")
        try:
            cls = get_chart_class(name)
        except KeyError:
            raise ValueError(f"unknown chart '{name}' specified in the YAML file")
        schema.validate(self.data, cls.SCHEMA)
        # Create the class instance from the data.
        return parse(self.data)
