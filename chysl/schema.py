"Schema handling."

import json

import jsonschema

import constants


# Subschema for defs to be used in chart schemas.
DEFS = {
    "marker": {
        "$anchor": "marker",
        "title": "Symbol to use as data point marker.",
        "oneOf": [
            {
                "title": "Predefined symbols denoted by names.",
                "enum": constants.MARKERS,
            },
            {
                "title": "A single character as marker.",
                "type": "string",
                "minLength": 1,
                "maxLength": 1,
            },
        ],
    },
    "text": {
        "$anchor": "text",
        "title": "Text, with or without explicit styling.",
        "oneOf": [
            {
                "title": "Text with default styling.",
                "type": "string",
            },
            {
                "title": "Text with styling options.",
                "type": "object",
                "required": ["text"],
                "additionalProperties": False,
                "properties": {
                    "text": {
                        "title": "The text to display.",
                        "type": "string",
                    },
                    "font": {
                        "title": "Name of the font.",
                        "type": "string",
                        "default": constants.DEFAULT_FONT_FAMILY,
                    },
                    "size": {
                        "title": "Size of font (pixels). Default depends on context.",
                        "type": "number",
                        "minimumExclusive": 0,
                    },
                    "bold": {
                        "title": "Bold font.",
                        "type": "boolean",
                        "default": False,
                    },
                    "italic": {
                        "title": "Italics font.",
                        "type": "boolean",
                        "default": False,
                    },
                    "color": {
                        "title": "Color of text.",
                        "type": "string",
                        "format": "color",
                        "default": "black",
                    },
                    "placement": {
                        "title": "Placement of text. Ignored in some contexts.",
                        "enum": constants.PLACEMENTS,
                        "default": constants.CENTER,
                    },
                },
            },
        ],
    },
    "fuzzy_number": {
        "$anchor": "fuzzy_number",
        "title": "Number value, exact, or fuzzy with either low/high or error.",
        "oneOf": [
            {
                "title": "Exact number value.",
                "type": "number",
            },
            {
                "title": "Fuzzy number value,  with either low/high or error",
                "type": "object",
                "required": ["value"],
                "additionalProperties": False,
                "minProperties": 2,
                "properties": {
                    "value": {
                        "title": "Central value for the fuzzy number.",
                        "type": "number",
                    },
                    "low": {
                        "title": "Low value for the fuzzy number.",
                        "type": "number",
                    },
                    "high": {
                        "title": "High value for the fuzzy number.",
                        "type": "number",
                    },
                    "error": {
                        "title": "Symmetrical error around the central value.",
                        "type": "number",
                        "exclusiveMinimum": 0,
                    },
                },
            },
        ],
    },
    "frame": {
        "$anchor": "frame",
        "title": "Specification of the chart area frame.",
        "oneOf": [
            {
                "title": "Default chart area frame, or no frame.",
                "type": "boolean",
                "default": True,
            },
            {
                "title": "Specification of the chart area frame.",
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "thickness": {
                        "title": "Thickness of the frame (pixels). Default depends on the chart.",
                        "type": "number",
                        "minimumExclusive": 0,
                    },
                    "color": {
                        "title": "Color of the frame. Default depends on the chart.",
                        "type": "string",
                        "format": "color",
                    },
                    "radius": {
                        "title": "Radius of the frame corner curvature (pixels). Default depends on the chart.",
                        "type": "number",
                        "minimum": 0,
                    },
                },
            },
        ],
    },
    "axis": {
        "$anchor": "axis",
        "title": "Coordinate axis specification.",
        "oneOf": [
            {
                "title": "Display default axis, or no display.",
                "type": "boolean",
                "default": True,
            },
            {
                "title": "Coordinate axis specification.",
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "min": {
                        "title": "Explicit minimum for the axis.",
                        "type": "number",
                    },
                    "max": {
                        "title": "Explicit maximum for the axis.",
                        "type": "number",
                    },
                    "ticks": {
                        "title": "Explicit positions for axis ticks.",
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "title": "Axis coordinate of a tick.",
                            "type": "number",
                        },
                    },
                    "labels": {
                        "title": "Display tick labels, or not.",
                        "type": "boolean",
                        "default": True,
                    },
                    "factor": {
                        "title": "Factor to divide tick value by for label display. Default depends on context.",
                        "type": "number",
                        "minimumExclusive": 0,
                    },
                    "absolute": {
                        "title": "Display absolute values for tick labels.",
                        "type": "boolean",
                        "default": False,
                    },
                    "caption": {
                        "title": "Axis description.",
                        "type": "string",
                    },
                },
            },
        ],
    },
    "grid": {
        "$anchor": "grid",
        "title": "Coordinate grid, with optional styling.",
        "oneOf": [
            {
                "title": "Display default grid or not.",
                "type": "boolean",
                "default": True,
            },
            {
                "title": "Grid with styling.",
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "color": {
                        "title": "Color of grid lines.",
                        "type": "string",
                        "format": "color",
                        "default": "lightgray",
                    },
                },
            },
        ],
    },
    "chart_or_include": {
        "$anchor": "chart_or_include",
        "title": "Inline chart specification, or location (file of web resource) to read the chart specification from.",
        "oneOf": [
            {
                "title": "Specification of a chart.",
                "type": "object",
                "required": ["chart"],
                "properties": {
                    "chart": {"enum": constants.CHARTS},
                    # No need to fully specify contents here.
                },
            },
            {
                "title": "Read the chart specification (YAML) referenced by the URL.",
                "type": "object",
                "required": ["include"],
                "additionalProperties": False,
                "properties": {
                    "include": {
                        "type": "string",
                        "format": "uri-reference",
                    },
                },
            },
        ],
    },
    "datasource": {
        "$anchor": "datasource",
        "title": "Data from a file, web resource or database.",
        "oneOf": [
            {
                "title": "File path or web resource URL, with optional explicit file format and parameter map.",
                "type": "object",
                "required": ["source"],
                "additionalProperties": False,
                "properties": {
                    "source": {
                        "title": "File path or web resource URL.",
                        "type": "string",
                        "format": "uri-reference",
                    },
                    "format": {
                        "title": "File format.",
                        "enum": constants.FORMATS,
                    },
                    "map": {
                        "title": "For a chart parameter, specify the source data field to use.",
                        "type": "object",
                        "properties": {
                            # Not specified here; depends on the chart.
                        },
                    },
                },
            },
            {
                "title": "Sqlite database.",
                "type": "object",
                "required": ["database", "source", "select"],
                "additionalProperties": False,
                "properties": {
                    "database": {"const": "sqlite"},
                    "source": {
                        "title": "File path or URL for the Sqlite database file.",
                        "type": "string",
                        "format": "uri-reference",
                    },
                    "select": {
                        "title": "SQL 'select' statement retrieving the data from the database.",
                        "type": "string",
                    },
                },
            },
        ],
    },
    "field": {
        "$anchor": "field",
        "title": "For a chart parameter, give the source data field to use.",
        "oneOf": [
            {
                "title": "Name of the field in the source data; e.g. CSV column header.",
                "type": "string",
                "minLength": 1,
            },
            {
                "title": "Number of the field in the source data; e.g. CSV column number, starting with 1.",
                "type": "integer",
                "minimum": 1,
            },
            {
                "title": "Mapping of values in a field of source data to values in a chart parameter.",
                "type": "object",
                "required": ["field", "map"],
                "additionalProperties": False,
                "properties": {
                    "field": {
                        "title": "Name of the field in the source data; e.g. CSV column header.",
                        "type": "string",
                        "minLength": 1,
                    },
                    "map": {
                        "title": "Convert a string value in the source data to a value for the chart parameter.",
                        "type": "object",
                        "properties": {
                            # Not specified here; depends on the chart.
                        },
                    },
                },
            },
        ],
    },
}


def add_defs(schema):
    "Add the defs that are used by the schema, to make it self-contained."
    while True:
        if refs := find_defs(schema):
            schema["$defs"] = dict([(r, DEFS[r]) for r in refs])
        else:
            break
        # Newly included refs may refer to other, as yet un-included refs.
        if refs == find_defs(schema):
            break


def find_defs(schema):
    result = set()
    if isinstance(schema, dict):
        if "$ref" in schema:
            result.add(schema["$ref"][1:])
        else:
            for key, subschema in schema.items():
                result.update(find_defs(subschema))
    elif isinstance(schema, list):
        for subschema in schema:
            result.update(find_defs(subschema))
    return result


def get_validator(schema):
    format_checker = jsonschema.FormatChecker(["color", "uri-reference"])

    # How to add more checkers:
    # @format_checker.checks("color")
    # def color_format(value):
    #     try:
    #         webcolors.normalize_hex(value)
    #     except ValueError:
    #         try:
    #             webcolors.name_to_hex(value)
    #         except ValueError:
    #             return False
    #     return True

    return jsonschema.Draft202012Validator(schema=schema, format_checker=format_checker)


def check_schema(schema):
    get_validator(schema).check_schema(schema)


def is_valid(instance, schema):
    try:
        get_validator(schema).validate(instance)
    except jsonschema.exceptions.ValidationError as error:
        return False
    return True


def validate(instance, schema, path=None):
    try:
        get_validator(schema).validate(instance)
    except jsonschema.exceptions.ValidationError as error:
        if path:
            path = [path] + list(error.path)
        else:
            path = list(error.path)
        path = ".".join([str(p) for p in path])
        raise ValueError(f"{error.message} in instance '{path}'")
