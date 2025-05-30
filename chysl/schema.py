"Schema handling."

import json

import jsonschema

import constants


# Subschema for defs to be used in chart schemas.
DEFS = {
    "size": {
        "$anchor": "size",
        "title": "Size of graphical item, in approximate display pixel units.",
        "type": "number",
        "minimumExclusive": 0,
    },
    "color": {
        "$anchor": "color",
        "title": "Color specification; hex code '#rrggbb' or CSS3 color name.",
        "type": "string",
        "format": "color",
    },
    "opacity": {
        "$anchor": "opacity",
        "title": "Opacity in range [0.0, 1.0].",
        "type": "number",
        "minimum": 0,
        "maximum": 1,
        "default": 1,
    },
    "marker": {
        "$anchor": "marker",
        "title": "Symbol for use as a marker in a chart.",
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
                    "size": {
                        "title": "Size of font. Default depends on context.",
                        "$ref": "#size",
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
                    "anchor": {
                        "title": "Text anchor position. Ignored in some contexts.",
                        "enum": constants.ANCHORS,
                        "default": constants.MIDDLE,
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
    "uri": {
        "$anchor": "uri",
        "title": "A URI, absolute or relative.",
        "type": "string",
        "format": "uri-reference",
    },
    "axis": {
        "$anchor": "axis",
        "title": "Coordinate axis specification.",
        "oneOf": [
            {
                "title": "Display default axis.",
                "type": "boolean",
                "default": True,
            },
            {
                "title": "Axis details.",
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "color": {
                        "title": "Color of grid lines.",
                        "type": "string",
                        "format": "color",
                        "default": "gray",
                    },
                    "absolute": {
                        "title": "Display absolute values for ticks.",
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
    "chart_or_include": {
        "$anchor": "chart_or_include",
        "title": "Inline chart specification, or location (file of web resource) to read the chart specification from.",
        "oneOf": [
            {
                "title": "Read the chart specification (YAML) from the URI reference.",
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
            {
                "title": "Specification of a chart.",
                "type": "object",
                "required": ["chart"],
                "properties": {
                    "chart": {"enum": constants.CHARTS},
                    # No need to fully specify contents here.
                },
            },
        ],
    },
    "field": {
        "$anchor": "field",
        "title": "Mapping of a plot parameter to a field in source data.",
        "oneOf": [
            {
                "title": "Name of the field in the source data; CSV column header. The values are used directly.",
                "type": "string",
                "minLength": 1,
            },
            {
                "title": "Number of the field in the source data; CSV column number, starting with 1. The values are used directly.",
                "type": "integer",
                "minimum": 1,
            },
            {
                "title": "Mapping of values in source data to a plot parameter.",
                "type": "object",
                "required": ["field"],
                "additionalProperties": False,
                "properties": {
                    "field": {
                        "title": "Name of the field in the source data; CSV column header.",
                        "type": "string",
                        "minLength": 1,
                    },
                    "map": {
                        "title": "Map a string value in the source data to a value for the plot parameter.",
                        "type": "object",
                        "properties": {
                            # Any.
                        },
                    },
                },
            },
        ],
    },
    "datapoints": {
        "$anchor": "datapoints",
        "title": "Data provided inline, or from a file, web resource or database.",
        "oneOf": [
            {
                "title": "Inline data points.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "x": {"type": "number"},
                        "y": {"type": "number"},
                        "size": {"$ref": "#size"},
                        "color": {"$ref": "#color"},
                        "opacity": {"$ref": "#opacity"},
                        "marker": {"$ref": "#marker"},
                    },
                },
            },
            {
                "title": "Data from file, web resource or database.",
                "type": "object",
                "required": ["source"],
                "additionalProperties": False,
                "properties": {
                    "source": {
                        "oneOf": [
                            {
                                "title": "File path or href. File format is deduced from the extension, or 'csv' if not recognized.",
                                "type": "string",
                                "format": "uri-reference",
                            },
                            {
                                "title": "File path or href, with explicit file format.",
                                "type": "object",
                                "required": ["location", "format"],
                                "additionalProperties": False,
                                "properties": {
                                    "location": {
                                        "title": "File path or href.",
                                        "type": "string",
                                        "format": "uri-reference",
                                    },
                                    "format": {
                                        "title": "File format.",
                                        "enum": constants.FORMATS,
                                    },
                                },
                            },
                            {
                                "title": "Sqlite database.",
                                "type": "object",
                                "required": ["database", "location", "select"],
                                "additionalProperties": False,
                                "properties": {
                                    "database": {"const": "sqlite"},
                                    "location": {
                                        "title": "File path or href.",
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
                    "parameters": {
                        "title": "Mapping of plot parameters to the fields in the source data.",
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "x": {"$ref": "#field"},
                            "y": {"$ref": "#field"},
                            "size": {"$ref": "#field"},
                            "color": {"$ref": "#field"},
                            "opacity": {"$ref": "#field"},
                            "marker": {"$ref": "#field"},
                        },
                    },
                },
            },
        ],
    },
}


def add_defs(schema):
    "Add the defs that are used by the schema."
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
