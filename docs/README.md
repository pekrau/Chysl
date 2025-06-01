# ![Chysl](https://github.com/pekrau/Chysl/blob/main/docs/logo32.svg) Chysl 0.3.5

Charts defined in YAML for rendering into SVG. Charts can be combined in different ways.

This code has been lovingly hand-crafted. No AI tools were used in its development.

## YAML format

The YAML file must contain the software identification marker:

    chysl: {version}

where `{version}` is either `null` or the string representing the version of the software.

[JSON Schema](docs/schema_defs.md) for general definitions used in JSON schema of different charts.

## Charts

- [timelines](docs/timelines.md): Timelines having events and periods.

- [piechart](docs/piechart.md): Pie chart displaying slices.

- [scatter2d](docs/scatter2d.md): 2D scatter chart.

- [lines2d](docs/lines2d.md): 2D lines chart.

- [note](docs/note.md): Textual note with title, body and footer text.

- [column](docs/column.md): Charts stacked in a column.

- [row](docs/row.md): Charts arranged in a row.

- [overlay](docs/overlay.md): Charts overlayed over one another, with optional opacity.

- [board](docs/board.md): Chart to place charts at specified positions.

