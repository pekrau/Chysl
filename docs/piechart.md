# piechart

- [Examples](#examples)
  - [pyramid](#pyramid)
  - [day](#day)
  - [pies_column](#pies_column)
  - [pies_row](#pies_row)

- [Specification](#specification)

## Examples

### pyramid

![pyramid SVG](pyramid.svg)

```yaml
chysl: 0.5.1
chart: piechart
title: Pyramid
frame:
  thickness: 4
  color: gray
start: 132
palette:
- '#4c78a8'
- '#9ecae9'
- '#f58518'
slices:
- value: 7
  label: Shadow
- value: 18
  label: Sunny
- value: 70
  label: Sky
```
### day

[CSV data file](day.csv)

![day SVG](day.svg)

```yaml
chysl: 0.5.1
chart: piechart
title:
  size: 30
  text: Day
diameter: 400
total: 24
slices:
  source: day.csv
  map:
    value: hours
```
### pies_column

![pies_column SVG](pies_column.svg)

```yaml
chysl: 0.5.1
chart: column
title: Pies in column
subcharts:
- chart: piechart
  title: Strawberry pie
  slices:
  - value: 7
    label: Flour
    color: white
  - value: 2
    label: Eggs
    color: yellow
  - value: 3
    label: Butter
    color: gold
  - value: 3
    label: Strawberries
    color: orangered
    href: https://en.wikipedia.org/wiki/Strawberry
- chart: piechart
  title: Rhubarb pie
  diameter: 250
  slices:
  - value: 7
    label: Flour
    color: white
  - value: 2
    label: Eggs
    color: yellow
  - value: 3
    label: Butter
    color: gold
  - value: 3
    label: Rhubarb
    color: green
    href: https://en.wikipedia.org/wiki/Rhubarb
- chart: note
  title: Comment
  body: Strawberry pie is good.
  footer:
    italic: true
    text: Copyright 2025 Per Kraulis
padding: 10
```
### pies_row

![pies_row SVG](pies_row.svg)

```yaml
chysl: 0.5.1
chart: row
title: Pies in row
subcharts:
- chart: piechart
  title: Strawberry pie
  diameter: 300
  palette:
  - white
  - yellow
  - gold
  - red
  slices:
  - value: 7
    label: Flour
  - value: 2
    label: Eggs
  - value: 3
    label: Butter
  - value: 3
    label: Strawberries
    href: https://en.wikipedia.org/wiki/Strawberry
- chart: piechart
  title: Rhubarb pie
  palette:
  - white
  - yellow
  - gold
  - red
  slices:
  - value: 7
    label: Flour
  - value: 2
    label: Eggs
  - value: 3
    label: Butter
  - value: 3
    label: Rhubarb
    color: green
    href: https://en.wikipedia.org/wiki/Rhubarb
padding: 10
```
## Specification

[JSON Schema](piechart.md)

Pie chart displaying slices.

- **chart**:
  - *required*
  - *const* 'piechart'
- **title**: Title of the chart.
  - *See* [text](schema_defs.md#text).
- **description**: Description of the chart. Rendered as <desc> in SVG.
  - *type*: string
- **diameter**: Diameter of the pie chart.
  - *type*: float
  - *exclusiveMinimum*: 0
  - *default*: 200
- **frame**: Specification of the piechart perimeter.
  - *See* [frame](schema_defs.md#frame).
- **total**: Sum total x value to relate slice x values to.
  - *type*: float
  - *exclusiveMinimum*: 0
- **start**: Starting point for first slice; in degrees from the top.
  - *type*: float
- **palette**: Palette used for slices lacking explicit color specification.
  - *type*: sequence
  - *items*:
    - *type*: string
    - *format*: color
  - *default*: ['tomato', 'darkviolet', 'deeppink', 'deepskyblue', 'gold', 'yellowgreen']
- **slices**: Slices in the pie chart.
  - *required*
  - Alternative 1: Inline slices data.
    - *type*: sequence
    - *items*:
      - *type*: mapping
      - **value**: The value visualized by the slice.
        - *required*
        - *type*: float
        - *exclusiveMinimum*: 0
      - **label**: Description of the x value.
        - *type*: string
      - **color**: Color of the slice. Overrides the palette.
        - *type*: string
        - *format*: color
      - **href**: A link URL, absolute or relative.
        - *type*: string
        - *format*: uri-reference
  - Alternative 2: External source of slices data.
    - *See* [datasource](schema_defs.md#datasource).

