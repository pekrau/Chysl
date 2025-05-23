"Abstract Chart, Entry and Container classes."

import icecream

icecream.install()

import csv
import io
import json
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


class Chart:
    "Abstract chart."

    DEFAULT_FONT_SIZE = 14
    DEFAULT_TITLE_FONT_SIZE = 18

    def __init__(self, title=None, entries=None):
        assert title is None or isinstance(title, (str, dict))
        assert entries is None or isinstance(entries, (tuple, list))

        self.title = title
        self.entries = []
        if entries:
            for entry in entries:
                self.append(entry)

    def __iadd__(self, entry):
        self.append(entry)
        return self

    def __eq__(self, other):
        if not isinstance(other, Chart):
            return False
        if self.__class__ != other.__class__:
            return False
        return self.as_dict() == other.as_dict()

    @property
    def name(self):
        return self.__class__.__name__.casefold()

    def append(self, entry):
        "Append the entry to the chart."
        self.entries.append(self.convert_entry(entry))

    def convert_entry(self, entry):
        """Convert and check that the entry is valid for the chart.
        Raise ValueError otherwise.
        """
        if isinstance(entry, dict):
            entry = parse(entry)
        if not isinstance(entry, Entry):
            raise ValueError(f"invalid entry '{entry}' for {self.name}")
        return entry

    def as_dict(self):
        result = {"chart": self.name}
        result.update(self.text_as_dict("title"))
        result.update(self.entries_as_dict())
        return result

    def text_as_dict(self, key):
        "Helper to convert possibly styled text entry to dict."
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
        ) is not None and size != self.DEFAULT_TITLE_FONT_SIZE:
            result["size"] = size
        if text.get("bold"):
            result["bold"] = True
        if text.get("italic"):
            result["italic"] = True
        if (color := text.get("color")) is not None and color != "black":
            result["color"] = color
        if (anchor := text.get("anchor")) is not None and anchor != "middle":
            result["anchor"] = anchor
        return {key: result}

    def entries_as_dict(self):
        result = []
        for entry in self.entries:
            try:  # This entry was included from another source.
                result.append({"include": entry.location})
            except AttributeError:
                result.append(entry.as_dict())
        if result:
            return {"entries": result}
        else:
            return {}

    def render(self, target=None, antialias=True, indent=2, restart_unique_id=False):
        """Render chart and return the SVG code.
        If target is provided, write into file given by path or open file object.
        """
        if restart_unique_id:
            utils.restart_unique_id()
        self.build()
        if antialias:
            extent = Vector2(self.width + 1, self.height + 1)
            transform = "translate(0.5, 0.5)"
        else:
            extent = Vector2(self.width, self.height)
            transform = None
        document = Element(
            "svg",
            xmlns=constants.SVG_XMLNS,
            width=utils.N(extent.x),
            height=utils.N(extent.y),
            viewBox=f"0 0 {utils.N(extent.x)} {utils.N(extent.y)}",
            transform=transform,
        )
        document += Element("desc", f"Chysl {constants.__version__} {self.name}")
        document += self.svg
        document.repr_indent = indent
        if isinstance(target, (str, pathlib.Path)):
            with open(target, "w") as outfile:
                outfile.write(repr(document))
        elif target is None:
            return repr(document)
        else:
            target.write(repr(document))

    def build(self):
        """Create the SVG elements in the 'svg' attribute. Adds the title, if given.
        Sets the 'svg' and 'height' attributes.
        Requires the 'width' attribute.
        To be extended in subclasses.
        """
        self.height = 0
        assert hasattr(self, "width")

        self.svg = Element("g", stroke="black", fill="white")
        self.svg["font-family"] = constants.DEFAULT_FONT_FAMILY
        self.svg["font-size"] = self.DEFAULT_FONT_SIZE

        if self.title:
            if isinstance(self.title, dict):
                text = self.title["text"] or ""
                size = self.title.get("size") or self.DEFAULT_TITLE_FONT_SIZE
                color = self.title.get("color") or "black"
                anchor = self.title.get("anchor") or "middle"
            else:
                text = self.title
                size = self.DEFAULT_TITLE_FONT_SIZE
                color = "black"
                anchor = "middle"
            self.height += size
            self.svg += (
                title := Element(
                    "text",
                    text,
                    x=utils.N(self.width / 2),
                    y=utils.N(self.height),
                    stroke="none",
                    fill=color,
                )
            )
            title["font-size"] = utils.N(size)
            title["text-anchor"] = anchor
            if isinstance(self.title, dict):
                if self.title.get("bold"):
                    title["font-weight"] = "bold"
                if self.title.get("italic"):
                    title["font-style"] = "italic"
            self.height += constants.DEFAULT_PADDING + constants.FONT_DESCEND * size

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
        content = {
            "chysl": {
                "version": constants.__version__,
                "software": f"Chysl (Python) {constants.__version__}",
            }
        }
        content.update(data)
        if isinstance(target, (str, pathlib.Path)):
            with open(target, "w") as outfile:
                yaml.dump(content, outfile, allow_unicode=True, sort_keys=False)
        elif target is None:
            return yaml.dump(content, allow_unicode=True, sort_keys=False)
        else:
            yaml.dump(content, outfile, allow_unicode=True, sort_keys=False)


class Entry:
    "Abstract entry as part of a chart."

    def __eq__(self, other):
        if not isinstance(other, Entry):
            return False
        if self.__class__ != other.__class__:
            return False
        return self.as_dict() == other.as_dict()

    @property
    def name(self):
        return self.__class__.__name__.casefold()

    def as_dict(self):
        return {"entry": self.name}


# Lookup for end-use classes. Key: name of class (lower case); value: class
_entity_lookup = {}


def register(cls):
    "Register the chart or entry for parsing."
    assert issubclass(cls, Chart) or issubclass(cls, Entry)
    if issubclass(cls, Chart):
        schema.check_schema(cls.SCHEMA)
    key = cls.__name__.casefold()
    if key in _entity_lookup:
        raise KeyError(f"entity '{key}' already registered")
    _entity_lookup[key] = cls


def get_class(name):
    "Return the class for the chart name."
    return _entity_lookup[name]


def parse(data):
    "Parse the data dictionary and return the instance for the entity it describes."
    assert isinstance(data, dict), data
    if "include" in data:
        location = data["include"]
        reader = Reader(location)
        reader.read()
        memo.check_add(reader)
        try:
            entry = reader.get_chart()
            entry.location = location  # Record the location for later output.
        except ValueError as error:
            raise ValueError(f"error reading from '{reader}': {error}")
        finally:
            memo.remove(reader)
    else:
        try:
            name = data.pop("entry")
        except KeyError:
            try:
                name = data.pop("chart")
            except KeyError:
                raise ValueError(f"no chart or entry declaration in '{data}'")
        try:
            cls = _entity_lookup[name]
        except KeyError:
            raise ValueError(f"no such entity '{name}'")
        entry = cls(**data)
    return entry


def retrieve(location):
    """Read and parse the YAML file given by its path or URI.
    Return a Chart instance.
    """
    reader = Reader(location)
    reader.read()
    return reader.get_chart()


class Reader:
    "Read data from a location; URI or file path."

    def __init__(self, location):
        self.location = str(location)
        parts = urllib.parse.urlparse(self.location)
        self.scheme = parts.scheme
        if self.scheme:
            self.location = self.location
        elif pathlib.Path(self.location).is_absolute():
            self.scheme = "file"
        else:
            self.location = str(pathlib.Path.cwd().joinpath(self.location).resolve())
            self.scheme = "file"

    def __repr__(self):
        return f"Reader('{self.location}')"

    def read(self):
        "Read the data from the location. Raise ValueError if any problem."
        if self.scheme == "file":
            try:
                with open(self.location) as infile:
                    self.content = infile.read()
            except OSError as error:
                raise ValueError(str(error))
        else:
            try:
                response = requests.get(self.location)
                response.raise_for_status()
                self.content = response.text
            except requests.exceptions.RequestException as error:
                raise ValueError(str(error))

    def parse(self, format):
        "Parse the content as YAML into data. Raise ValueError if any problem."
        assert format in constants.FORMATS
        match format:
            case "csv" | "tsv":
                dialect = "excel" if format == "csv" else "excel_tab"
                # Check if the content seems to have a header.
                # Tried 'Sniffer' but it didn't behave well.
                peek_reader = csv.reader(io.StringIO(self.content), dialect= dialect)
                first_record = next(peek_reader)
                for part in first_record:
                    try:
                        float(part)
                    except ValueError:
                        pass
                    else:
                        # Does not seem to be a header; row numbers for map.
                        fieldnames = list(range(1, len(first_record)+1))
                        break
                else:
                    # Has a header; use its field names.
                    fieldnames = None
                reader = csv.DictReader(io.StringIO(self.content), dialect="excel")
                self.data = list(reader)
            case "tsv":
                reader = csv.DictReader(io.StringIO(self.content), dialect="excel_tab")
                self.data = list(reader)
            case "json":
                try:
                    self.data = json.loads(self.content)
                except json.JSONDecodeError as error:
                    raise ValueError(f"cannot interpret data as JSON: {error}")
            case "yaml":
                try:
                    self.data = yaml.safe_load(self.content)
                except yaml.YAMLError as error:
                    raise ValueError(f"cannot interpret data as YAML: {error}")

    def get_chart(self):
        """Return the instance of a Chart subclass from the YAML data.
        The meta information is stored in attribute 'meta'.
        If any of the following tests fail, raises ValueError:
        - The presence and validity of the 'chysl' format identification marker.
        - The compatibility of the version of the file, if given.
        - Check the data against the appropriate schema.
        """
        self.parse("yaml")
        prepared = self.data.copy()
        try:
            self.meta = prepared.pop("chysl")
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
        # Do proper schema validation on the original data.
        try:
            name = prepared["chart"]
        except KeyError:
            raise ValueError("no 'chart' defined in the YAML file")
        try:
            cls = _entity_lookup[name]
        except KeyError:
            raise ValueError(f"unknown chart '{name}' specified in the YAML file")
        schema.validate(prepared, cls.SCHEMA)
        # Create the class instance from the data lacking the identification marker.
        return parse(prepared)
