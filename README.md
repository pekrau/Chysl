# ![Chysl](https://github.com/pekrau/Chysl/blob/main/docs/logo64.svg) Chysl 0.1.0

Charts defined in YAML for rendering into SVG. Charts are hierarchically composable.

The YAML file must contain the software identification marker:

    chysl: {version}

where `{version}` is either `null` or the string representing the version of the software.

## Diagrams

- [timelines](docs/timelines.md): Timelines having events and periods.

- [piechart](docs/piechart.md): Pie chart containing slices.

- [note](docs/note.md): Textual note with title, body and footer text.

- [column](docs/column.md): Charts stacked in a column.

- [row](docs/row.md): Charts arranged in a row.

- [board](docs/board.md): Chart to place charts at specified positions.

