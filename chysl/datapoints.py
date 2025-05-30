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


class DatapointsReader:
    "Datapoints reader, YAML inline or from a source: file, web resource, database."

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

    def add(self, datapoint):
        assert isinstance(datapoint, dict)
        if self.required:
            for req in self.required:
                if datapoint.get(req) is None:
                    raise ValueError(f"Datapoint value for '{req}' is undefined.")
        self.datapoints.append(datapoint)

    def add_datapoint(self, x, y=None, marker=None, size=None, color=None, opacity=None):
        assert isinstance(x, (int, float))
        assert y is None or isinstance(y, (int, float))
        assert markers is None or marker in constants.MARKERS
        assert size is None or (isinstance(size, (int, float)) and size > 0)
        assert color is None or utils.is_color(color)
        assert opacity is None or (
            isinstance(opacity, (int, float)) and (0 <= opacity <= 1)
        )

        datapoint = dict(x=x)
        if y is not None:
            datapoint["y"] = y
        if marker is not None:
            datapoint["marker"] = marker
        if size is not None:
            datapoint["size"] = size
        if color is not None:
            datapoint["color"] = color
        if opacity is not None:
            datapoint["opacity"] = opacity
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
