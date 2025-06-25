"Data source: file, web resource, database."

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


class Datasource:
    "Abstract data source: file, web resource or database."

    DEFAULT_FORMAT = "csv"

    def __init__(self, spec, record_class):
        assert isinstance(spec, (str, dict))
        assert isinstance(record_class, type)

        self.record_class = record_class
        self.data = []
        self.source = spec["source"]

        # Database.
        self.database = spec.get("database")
        if self.database:
            self.select = spec["select"]
            self.read_database()

        # File or web resource.
        else:
            self.format = spec.get("format")
            if not self.format:
                self.format = pathlib.Path(self.source).suffix.lstrip(".")
                if self.format not in constants.FORMATS:
                    self.format = self.DEFAULT_FORMAT
            self.map = spec.get("map") or {}
            self.read_file_or_webresource()

    def add(self, record):
        assert isinstance(record, (dict, self.record_class))
        if isinstance(record, dict):
            try:
                for key, functions in self.record_class.fields.items():
                    if not functions:
                        continue
                    value = record.get(key)
                    if value is None:
                        if functions.get("required"):
                            raise ValueError(f"missing value for '{key}'")
                        continue
                    if convert := functions.get("convert"):
                        value = convert(value)
                    if check := functions.get("check"):
                        if not check(value):
                            raise ValueError(f"invalid value '{record[key]}'")
                    record[key] = value
            except (ValueError, TypeError) as error:
                raise ValueError(f"record # {len(self.data)}: {error}")
            record = self.record_class(**record)
        self.data.append(record)

    def read_database(self):
        # Currently Sqlite is the only db interface available.
        assert self.database == "sqlite"
        cnx = sqlite3.connect(f"file:{self.source}?mode=ro", uri=True)
        cnx.row_factory = self._sqlite_dict_factory
        for record in cnx.execute(self.select):
            self.add(record)

    def _sqlite_dict_factory(self, cursor, row):
        try:
            fields = self.sqlite_dict_factory_fields
        except AttributeError:
            self.sqlite_dict_factory_fields = fields = [
                column[0] for column in cursor.description
            ]
        return {key: value for key, value in zip(fields, row)}

    def read_file_or_webresource(self):
        assert self.format in constants.FORMATS

        if urllib.parse.urlparse(self.source).scheme:  # Probably http or https.
            try:
                response = requests.get(self.source)
                response.raise_for_status()
                content = response.text
            except requests.exceptions.RequestException as error:
                raise ValueError(str(error))
        else:
            try:
                with open(self.source) as infile:
                    content = infile.read()
            except OSError as error:
                raise ValueError(str(error))

        match self.format:

            case "csv" | "tsv":
                dialect = "excel" if self.format == "csv" else "excel_tab"
                # Check if the content has a header.
                # Heuristic: Is first value interpretable as float, then not a header.
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
                records = []
                # Special case for CSV: empty string converted to None.
                for record in reader:
                    for key, value in record.items():
                        if value == "":
                            record[key] = None
                    records.append(record)

            case "json":
                try:
                    records = json.loads(content)
                    if not isinstance(records, list):
                        raise ValueError("JSON data is not a list")
                except (json.JSONDecodeError, ValueError) as error:
                    raise ValueError(f"cannot interpret data as JSON: {error}")

            case "yaml":
                try:
                    records = yaml.safe_load(content)
                    if not isinstance(records, list):
                        raise ValueError("YAML data is not a list")
                except (yaml.YAMLError, ValueError) as error:
                    raise ValueError(f"cannot interpret data as YAML: {error}")

        for record in records:
            data = {}
            # Pick out only relevant data items; apply field key map if defined.
            for key in self.record_class.fields:
                field = self.map.get(key, key)
                if isinstance(field, dict):
                    value = record.get(field["field"])
                    data[key] = field["map"].get(value, value)
                else:
                    data[key] = record.get(field)
            self.add(data)

    def as_dict(self):
        result = dict(source=self.source)
        if self.database:
            result["database"] = self.database
            result["select"] = self.select
        else:
            if self.format != self.DEFAULT_FORMAT:
                result["format"] = self.format
            if self.map:
                result["map"] = self.map
        return result
