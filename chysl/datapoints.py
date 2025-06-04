"Datapoints reader, YAML inline or from a source: file, web resource, database."

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
import utils

# 'Real' data fields, with conversion and checking functions.
FIELDS = dict(
    x=dict(conv=float),
    y=dict(conv=float),
    size=dict(conv=float, check=lambda v: v > 0),
    color=dict(check=lambda c: utils.is_color(c)),
    marker=dict(check=lambda m: utils.is_marker(m)),
    label=dict(),
    opacity=dict(conv=float, check=lambda v: 1.0 < v < 0.0),
    href=dict(),
)


class DatapointsReader:
    "Datapoints reader, YAML inline or from a source: file, web resource, database."

    def __init__(self, data):
        assert data is None or isinstance(data, (tuple, list, dict))
        self.source = None
        self.location = "inline"

        self.datapoints = []
        # YAML inline.
        if isinstance(data, (tuple, list)):
            for datapoint in data:
                self.add(datapoint)
        # Data from file, web resource or database.
        elif isinstance(data, dict):
            self.read(data)

    def __str__(self):
        if self.database:
            return f"DatapointsReader('{self.database}:{self.location}')"
        else:
            return f"DatapointsReader('{self.location}')"

    def __iter__(self):
        return iter(self.datapoints)

    def add(self, datapoint):
        num = len(self.datapoints) + 1
        if not isinstance(datapoint, dict):
            raise ValueError(f"Datapoint {num} is not a dict.")
        self.datapoints.append(datapoint)

    def add_datapoint(
        self,
        x=None,
        y=None,
        size=None,
        color=None,
        marker=None,
        label=None,
        opacity=None,
        href=None,
    ):
        assert x is None or isinstance(x, (int, float))
        assert y is None or isinstance(y, (int, float))
        assert size is None or (isinstance(size, (int, float)) and size > 0)
        assert color is None or utils.is_color(color)
        assert marker is None or marker in constants.MARKERS
        assert label is Nont or isinstance(label, str)
        assert opacity is None or (
            isinstance(opacity, (int, float)) and (0 <= opacity <= 1)
        )
        assert href is None or isinstance(href, str)

        datapoint = {}
        if x is not None:
            datapoint["x"] = x
        if y is not None:
            datapoint["y"] = y
        if size is not None:
            datapoint["size"] = size
        if color is not None:
            datapoint["color"] = color
        if marker is not None:
            datapoint["marker"] = marker
        if label is not None:
            datapoint["label"] = label
        if opacity is not None:
            datapoint["opacity"] = opacity
        if href is not None:
            datapoint["href"] = href
        self.add(datapoint)

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

        # When data from external source, then apply given mapping (and conversion).
        if self.parameters:
            try:
                for key, kwargs in FIELDS.items():
                    if field := self.parameters.get(key):
                        converter = _Converter(field, **kwargs)
                        for datapoint in self.datapoints:
                            datapoint[key] = converter(datapoint)
            except KeyError:
                raise ValueError(
                    f"no such field '{field}' in data for parameter '{key}'"
                )
            except ValueError:
                raise ValueError(
                    f"invalid value in field '{field}' in data for parameter '{key}'"
                )

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
                datapoints = list(reader)

            case "json":
                try:
                    datapoints = json.loads(content)
                    if not isinstance(datapoints, list):
                        raise ValueError("JSON data is not a list")
                except (json.JSONDecodeError, ValueError) as error:
                    raise ValueError(f"cannot interpret data as JSON: {error}")

            case "yaml":
                try:
                    datapoints = yaml.safe_load(content)
                    if not isinstance(datapoints, list):
                        raise ValueError("YAML data is not a list")
                except (yaml.YAMLError, ValueError) as error:
                    raise ValueError(f"cannot interpret data as YAML: {error}")

        for datapoint in datapoints:
            self.add(datapoint)

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

    def as_dict(self):
        "Return the data as a dictionary."
        if self.source:
            result = dict(source=self.source)
            if self.parameters:
                result["parameters"] = self.parameters
        else:
            # Only output 'real' data, not ephemeral items used for display.
            result = []
            fieldnames = list(FIELDS.keys())
            for datapoint in self.datapoints:
                entry = {}
                for fieldname in fieldnames:
                    if (value := datapoint.get(fieldname)) is not None:
                        entry[fieldname] = value
                result.append(entry)
        return result

    def check_required(self, *required):
        "Check that all datapoints contain a non-None value in the given fields."
        assert all([isinstance(req, str) for req in required])

        for req in required:
            for num, datapoint in enumerate(self.datapoints):
                if datapoint.get(req) is None:
                    raise ValueError(
                        f"Datapoint {num+1} value for '{req}' is undefined."
                    )

    def minmax(self, field):
        datapoint = self.datapoints[0]
        value = datapoint[field]
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
        for datapoint in self.datapoints[1:]:
            value = datapoint[field]
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
    "Convert and map value from a value as given."

    def __init__(self, field, conv=None, check=None):
        if isinstance(field, (str, int)):
            self.fieldname = field
            self.map = None
        else:
            self.fieldname = field["field"]
            self.map = field.get("map")
        self.conv = conv or (lambda v: v)
        self.check = check

    def __call__(self, datapoint):
        try:
            value = self.conv(datapoint[self.fieldname])
        except (KeyError, IndexError):
            raise KeyError
        except (ValueError, TypeError):
            raise ValueError
        if self.map is not None:
            # KeyError should just be passed on.
            value = self.map[value]
        if self.check:
            self.check(value)
        return value
