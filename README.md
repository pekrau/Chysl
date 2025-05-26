# ![Chysl](https://github.com/pekrau/Chysl/blob/main/docs/logo32.svg) Chysl 0.2.11

Charts defined in YAML for rendering into SVG. Charts are hierarchically composable.

The YAML file must contain the software identification marker:

    chysl: {version}

where `{version}` is either `null` or the string representing the version of the software.

[JSON Schema](docs/schema_defs.md) for general definitions used in JSON schema of different charts.

This code has been lovingly hand-crafted. No AI tools were used in its development.

## Charts

- [timelines](docs/timelines.md): Timelines having events and periods.

- [piechart](docs/piechart.md): Pie chart containing slices.

- [note](docs/note.md): Textual note with title, body and footer text.

- [plot2d](docs/plot2d.md): 2D chart plotting x/y data; scatter, etc.

- [column](docs/column.md): Charts stacked in a column.

- [row](docs/row.md): Charts arranged in a row.

- [board](docs/board.md): Chart to place charts at specified positions.

