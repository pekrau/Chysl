"Schema handling."

import json

import jsonschema

import constants


# Subschema for defs to be used in chart schemas.
DEFS = {
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
                        "type": "number",
                        "exclusiveMinimum": 0,
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
        "title": "Chart specification, or 'include' of a file or web source.",
        "oneOf": [
            {
                "title": "Include another YAML file from the URI reference.",
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
                "title": "Specification of any chart.",
                "type": "object",
                "required": ["chart"],
                "properties": {
                    "chart": {"enum": constants.CHARTS},
                    # No need to fully specify contents here.
                },
            },
        ],
    },
    "data_or_source": {
        "$anchor": "data_or_source",
        "title": "Data provided in-line, or from a file or web source.",
        "oneOf": [
            {
                "title": "In-line data points.",
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["x", "y"],
                    "additionalProperties": False,
                    "properties": {
                        "x": {"$ref": "#fuzzy_number"},
                        "y": {"$ref": "#fuzzy_number"},
                        "color": {
                            "type": "string",
                            "format": "color",
                        },
                    },
                },
            },
            {
                "title": "Data from file or web source.",
                "type": "object",
                "required": ["source"],
                "additionalProperties": False,
                "properties": {
                    "source": {
                        "type": "string",
                        "format": "uri-reference",
                    },
                    "format": {
                        "title": "Format of data file. Inferred from file extension, if not provided.",
                        "enum": constants.FORMATS,
                        "default": "csv",
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
