"Create documentation from JSON Schema."

import json

import constants
import chart
import schema
from test import run_tests, TESTS

TERMS = {"array": "sequence", "object": "mapping", "number": "float"}


def term(v):
    return TERMS.get(v, v)


def make_docs():
    result = []
    result.append(
        f"# ![Chysl](https://github.com/pekrau/Chysl/blob/main/docs/logo32.svg) Chysl {constants.__version__}\n\n"
    )
    result.append(constants.__doc__)
    result.append("\n\n")

    result.append("The YAML file must contain the software identification marker:\n\n")
    result.append("    chysl: {version}\n\n")
    result.append(
        f"where `{{version}}` is either `null` or the string representing the version of the software.\n\n"
    )

    result.append("[JSON Schema](docs/schema_defs.md) for definitions used in chart JSON schema.\n\n")

    run_tests()

    result.append("## Charts\n\n")
    for name in constants.CHARTS:
        chartschema = chart.get_class(name).SCHEMA
        result.append(f"- [{name}](docs/{name}.md): {chartschema['title']}\n\n")

    with open("../README.md", "w") as outfile:
        outfile.write("".join(result))

    result = []
    result.append("# Schema definitions\n")
    for name, subschema in schema.DEFS.items():
        result.append(f"\n## {name}\n")
        result.extend(output_schema(subschema))
    with open("../docs/schema_defs.md", "w") as outfile:
        outfile.write("".join(result))

    for name in constants.CHARTS:
        chartschema = chart.get_class(name).SCHEMA
        with open(f"../docs/{name}.json", "w") as outfile:
            json.dump(chartschema, outfile, ensure_ascii=False, indent=2)
        result = []
        result.append(f"# {name}\n\n")
        result.append("- [Examples](#examples)\n")
        for test in TESTS[name]:
            result.append(f"  - [{test}](#{test})\n")
        result.append("\n")
        result.append("- [Specification](#specification)\n\n")
        result.append("## Examples\n\n")
        for test in TESTS[name]:
            result.append(f"### {test}\n\n")
            result.append(f"![{test} SVG]({test}.svg)\n\n")
            with open(f"../docs/{test}.yaml") as infile:
                code = infile.read()
            result.append(f"```yaml\n{code}```\n")
        result.append("## Specification\n\n")
        result.append(f"[JSON Schema]({name}.md)\n")
        href = f"{name}.md"
        result.extend(output_schema(chartschema, href=href))
        with open(f"../docs/{href}", "w") as outfile:
            outfile.write("".join(result) + "\n")


def output_schema(schema, level=0, required=False, href=None):
    result = []
    prefix = "  " * level

    if level == 0:
        result.append(f"\n{prefix}{schema['title']}\n\n")

    if ref := schema.get("$ref"):
        result.append(f"{prefix}- *See* [{ref[1:]}](schema_defs.md{ref}).\n")

    if required:
        result.append(f"{prefix}- *required*\n")

    if const := schema.get("const"):
        result.append(f"{prefix}- *const* '{const}'\n")

    if type := schema.get("type"):
        match type:
            case "object":
                if level != 0:
                    result.append(f"{prefix}- *type*: {term(type)}\n")
                required = set(schema.get("required") or [])
                for key, subschema in schema["properties"].items():
                    if title := subschema.get("title"):
                        result.append(f"{prefix}- **{key}**: {title}\n")
                    else:
                        result.append(f"{prefix}- **{key}**:\n")
                    result.extend(
                        output_schema(
                            subschema, level + 1, required=key in required, href=href
                        )
                    )
            case "array":
                result.append(f"{prefix}- *type*: {term(type)}\n")
                result.append(f"{prefix}- *items*:\n")
                result.extend(output_schema(schema["items"], level + 1, href=href))
            case "integer" | "number":
                result.append(f"{prefix}- *type*: {term(type)}\n")
                for constraint in (
                    "minimum",
                    "exclusiveMinimum",
                    "maximum",
                    "exclusiveMaximum",
                    "minItems",
                    "maxItems",
                ):
                    try:
                        value = schema[constraint]
                        result.append(f"{prefix}- *{constraint}*: {value}\n")
                    except KeyError:
                        pass
            case _:
                result.append(f"{prefix}- *type*: {term(type)}\n")

    elif enum := schema.get("enum"):
        values = []
        for value in enum:
            if isinstance(value, str):
                value = f"'{value}'"
            values.append(value)
        result.append(f"{prefix}- *one of*: {', '.join(values)}\n")

    elif oneof := schema.get("oneOf"):
        for number, subschema in enumerate(oneof):
            result.append(
                f"{prefix}- Alternative {number+1}: {subschema.get('title') or ''}\n"
            )
            result.extend(output_schema(subschema, level + 1, href=href))

    elif anyof := schema.get("anyOf"):
        for number, subschema in enumerate(anyof):
            result.append(f"{prefix}- Option {number+1}\n")
            result.extend(output_schema(subschema, level + 1, href=href))

    if format := schema.get("format"):
        result.append(f"{prefix}- *format*: {format}\n")

    try:
        value = schema["default"]
        if isinstance(value, str):
            value = f"'{value}'"
        elif isinstance(value, bool):
            value = str(value).lower()
        result.append(f"{prefix}- *default*: {value}\n")
    except KeyError:
        pass

    return result


if __name__ == "__main__":
    make_docs()
