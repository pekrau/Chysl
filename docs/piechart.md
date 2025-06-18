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
chysl: 0.4.0
chart: piechart
title: Pyramid
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

![day SVG](day.svg)

```yaml
chysl: 0.4.0
chart: piechart
title:
  size: 30
  text: Day
diameter: 400
total: 24
slices:
- value: 8
  label: Sleep
  color: gray
- value: 1
  label: Breakfast
  color: lightgreen
- value: 2
  label: Gym
  color: lightblue
- value: 1
  label: Read
  color: navy
- value: 1
  label: Lunch
  color: lightgreen
- value: 0.4
  label: Shuteye
  color: gray
- value: 4.6
  label: Write
  color: pink
- value: 1
  label: Dinner
  color: lightgreen
- value: 3
  label: TV
  color: orange
- value: 2
  label: Read
  color: navy
```
### pies_column

![pies_column SVG](pies_column.svg)

```yaml
chysl: 0.4.0
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
```
### pies_row

![pies_row SVG](pies_row.svg)

```yaml
chysl: 0.4.0
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
- **total**: Total value to relate slice values to.
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
  - *type*: sequence
  - *items*:
    - *type*: mapping
    - **value**: The value visualized by the slice.
      - *required*
      - *type*: float
      - *exclusiveMinimum*: 0
    - **label**: Description of the value.
      - *type*: string
    - **color**: Color of the slice. Overrides the palette.
      - *type*: string
      - *format*: color
    - **href**: A URI for a link, absolute or relative.
      - *type*: string
      - *format*: uri-reference

