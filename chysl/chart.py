"Abstract Chart, Entry and Container classes."

import icecream

icecream.install()

import copy
import csv
import io
import json
import pathlib
import sqlite3
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
        "Default implementation; to be overridden when required."
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
            width=N(extent.x),
            height=N(extent.y),
            viewBox=f"0 0 {N(extent.x)} {N(extent.y)}",
            transform=transform,
        )
        document += Element("desc", f"{self.name}; Chysl {constants.__version__}")
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
                    x=N(self.width / 2),
                    y=N(self.height),
                    stroke="none",
                    fill=color,
                )
            )
            title["font-size"] = N(size)
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
        content = dict(chysl=constants.__version__)
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
        reader = ChartReader(location)
        try:
            memo.check_add(reader)
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
        except yaml.YAMLError as error:
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
        # Do schema validation on the data.
        try:
            name = self.data["chart"]
        except KeyError:
            raise ValueError("no 'chart' defined in the YAML file")
        try:
            cls = _entity_lookup[name]
        except KeyError:
            raise ValueError(f"unknown chart '{name}' specified in the YAML file")
        schema.validate(self.data, cls.SCHEMA)
        # Create the class instance from the data.
        return parse(self.data)


class DatapointsReader:
    """Datapoints reader, YAML inline or read from a source:
    file, web resource, database.
    """

    def __init__(self, data, required=None):
        assert data is None or isinstance(data, (list, dict))
        self.source = None
        self.location = "inline"
        self.required = required

        if data is None:
            self.datapoints = []

        # YAML inline.
        if isinstance(data, list):
            if len(data) == 0:
                raise ValueError("No data in the list.")
            if not isinstance(data[0], dict):
                raise ValueError("First item in the list is not a dict.")
            self.datapoints = copy.deepcopy(data)  # For safety.

        # Data from file, web resource or database.
        elif isinstance(data, dict):
            self.read(data)

        if self.required and self.datapoints:
            for req in self.required:
                if req not in self.datapoints[0]:
                    raise ValueError(f"First datapoint does not contain '{req}'.")

    def __str__(self):
        if self.database:
            return f"DatapointsReader('{self.database}:{self.location}')"
        else:
            return f"DatapointsReader('{self.location}')"

    def __iter__(self):
        return iter(self.datapoints)

    def append(self, datapoint):
        isinstance(datapoint, dict)
        if self.required:
            for req in self.required:
                if req not in datapoint:
                    raise ValueError(f"Datapoint does not contain '{req}'.")
        self.datapoints.append(datapoint)

    def read(self, data):
        assert isinstance(data, dict)
        try:
            self.source = data["source"]
        except KeyError:
            raise ValueError("No 'source' given in data.")
        assert isinstance(self.source, (str, dict))

        # Optional mapping of parameters to the data fields.
        self.parameters = data.get("parameters")

        # File or web resource with implicit format.
        if isinstance(self.source, str):
            self.location = self.source
            self.format = pathlib.Path(self.location).suffix.lstrip(".")
            if self.format not in constants.FORMATS:
                self.format = "csv"
            self.read_file()

        elif isinstance(self.source, dict):
            try:
                self.location = self.source["location"]
            except KeyError:
                raise ValueError("no location specified for data source")
            try:
                self.database = self.source["database"]
            except KeyError:
                try:
                    self.format = self.source["format"]
                except KeyError:
                    raise ValueError("no format specified for data source")
                if self.format not in constants.FORMATS:
                    raise ValueError(
                        f"invalid format '{self.format}' specified for data source"
                    )
                self.read_file()
            else:
                self.read_database()

        # When data from external source, then apply given mapping.
        if self.parameters:
            for key in ("x", "y", "size", "color", "opacity", "marker"):
                if field := self.parameters.get(key):
                    getattr(self, f"map_{key}_field")(field)

    def read_file(self):
        # Tabular data; needs further parsing.
        if urllib.parse.urlparse(self.location).scheme:  # Probably http or https.
            try:
                response = requests.get(self.location)
                response.raise_for_status()
                content = response.text
            except requests.exceptions.RequestException as error:
                raise ValueError(str(error))
        else:
            try:
                with open(self.location) as infile:
                    content = infile.read()
            except OSError as error:
                raise ValueError(str(error))

        assert self.format in constants.FORMATS
        match self.format:

            case "csv" | "tsv":
                dialect = "excel" if self.format == "csv" else "excel_tab"
                # Check if the content seems to have a header.
                # (Tried 'csv.Sniffer' but it didn't behave well.)
                peek_reader = csv.reader(io.StringIO(content), dialect=dialect)
                first_record = next(peek_reader)
                for part in first_record:
                    try:
                        float(part)
                    except ValueError:
                        pass
                    else:
                        # Not a header; use column numbers for dict keys.
                        fieldnames = list(range(1, len(first_record) + 1))
                        break
                else:
                    # Has a header; use its field names.
                    fieldnames = None
                reader = csv.DictReader(
                    io.StringIO(content), fieldnames=fieldnames, dialect="excel"
                )
                self.datapoints = list(reader)

            case "json":
                try:
                    self.datapoints = json.loads(content)
                except json.JSONDecodeError as error:
                    raise ValueError(f"cannot interpret data as JSON: {error}")

            case "yaml":
                try:
                    self.datapoints = yaml.safe_load(content)
                except yaml.YAMLError as error:
                    raise ValueError(f"cannot interpret data as YAML: {error}")

    def read_database(self):
        # Currently only db interface available.
        assert self.database == "sqlite"
        try:
            self.select = self.source["select"]
        except KeyError:
            raise ValueError("no select specified for database data source")
        cnx = sqlite3.connect(f"file:{self.location}?mode=ro", uri=True)
        cnx.row_factory = self.sqlite_dict_factory
        cursor = cnx.execute(self.select)
        self.datapoints = list(cursor)

    def sqlite_dict_factory(self, cursor, row):
        try:
            fields = self.sqlite_dict_factory_fields
        except AttributeError:
            self.sqlite_dict_factory_fields = fields = [
                column[0] for column in cursor.description
            ]
        return {key: value for key, value in zip(fields, row)}

    def map_x_field(self, field):
        if isinstance(field, (str, int)):
            fieldname = field
        else:
            fieldname = field["field"]
        try:
            for dp in self.datapoints:
                dp["x"] = float(dp[fieldname])
        except (KeyError, IndexError):
            raise ValueError(f"no such field '{fieldname}' in data for parameter 'x'")
        except (ValueError, TypeError):
            raise ValueError(
                f"invalid value in field '{fieldname}' in data for parameter 'x'"
            )

    def map_y_field(self, field):
        if isinstance(field, (str, int)):
            fieldname = field
        else:
            fieldname = field["field"]
        try:
            for dp in self.datapoints:
                dp["y"] = float(dp[fieldname])
        except (KeyError, IndexError):
            raise ValueError(f"no such field '{fieldname}' in data for parameter 'y'")
        except (ValueError, TypeError):
            raise ValueError(
                f"invalid value in field '{fieldname}' in data for parameter 'y'"
            )

    def map_size_field(self, field):
        if isinstance(field, (str, int)):
            fieldname = field
        else:
            fieldname = field["field"]
        try:
            for dp in self.datapoints:
                try:
                    dp["size"] = float(dp[fieldname])
                except (KeyError, IndexError):
                    pass
                else:
                    if dp["size"] <= 0.0:
                        raise ValueError
        except (ValueError, TypeError):
            raise ValueError(
                f"invalid value in field '{fieldname}' in data for parameter 'size'"
            )

    def map_color_field(self, field):
        if isinstance(field, (str, int)):
            fieldname = field
            convert = lambda v: v
        else:
            fieldname = field["field"]
            convert = _Converter(field)
        for dp in self.datapoints:
            try:
                dp["color"] = convert(dp[fieldname])
            except (KeyError, IndexError):
                pass
            else:
                if not utils.is_color(dp["color"]):
                    raise ValueError(
                        f"invalid value in field '{fieldname}' in data for parameter 'color'"
                    )

    def map_opacity_field(self, field):
        if isinstance(field, (str, int)):
            fieldname = field
        else:
            fieldname = field["field"]
        try:
            for dp in self.datapoints:
                dp["opacity"] = float(dp[fieldname])
                if 1.0 < dp["opacity"] < 0.0:
                    raise ValueError
        except (KeyError, IndexError):
            pass
        except (ValueError, TypeError):
            raise ValueError(
                f"invalid value in field '{fieldname}' in data for parameter 'opacity'"
            )

    def map_marker_field(self, field):
        if isinstance(field, (str, int)):
            fieldname = field
            convert = lambda v: v
        else:
            fieldname = field["field"]
            convert = _Converter(field)
        for dp in self.datapoints:
            try:
                dp["marker"] = convert(dp[fieldname])
            except (KeyError, IndexError):
                pass
            if not utils.is_marker(dp["marker"]):
                raise ValueError(
                    f"invalid value in field '{fieldname}' in data for parameter 'marker'"
                )

    def as_dict(self):
        "Return the data as a dictionary."
        if self.source:
            result = dict(source=self.source)
            if self.parameters:
                result["parameters"] = self.parameters
        else:
            result = self.datapoints
        return result

    def minmax(self, field):
        dp = self.datapoints[0]
        value = dp[field]
        if isinstance(value, dict):
            try:
                low = value["low"]
            except KeyError:
                low = value["value"] - value["error"]
            try:
                high = value["high"]
            except KeyError:
                high = value["value"] + value["error"]
        else:
            low = value
            high = value
        for dp in self.datapoints[1:]:
            value = dp[field]
            if isinstance(value, dict):
                try:
                    low = min(low, value["low"])
                except KeyError:
                    low = min(low, value["value"] - value["error"])
                try:
                    high = max(high, value["high"])
                except KeyError:
                    high = max(high, value["value"] + value["error"])
            else:
                low = min(low, value)
                high = max(high, value)
        return (low, high)


class _Converter:
    "Map or compute new value from a value as given."

    def __init__(self, field):
        self.map = field.get("map")

    def __call__(self, value):
        if self.map is None:
            return value
        # Yes: if no match, then raise KeyError.
        return self.map[value]
