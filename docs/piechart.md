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
chysl: 0.3.2
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
chysl: 0.3.2
chart: piechart
title:
  text: Day
  size: 30
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
chysl: 0.3.2
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
- chart: note
  title: Comment
  body: Strawberry pie is good.
  footer:
    text: Copyright 2025 Per Kraulis
    italic: true
```
### pies_row

![pies_row SVG](pies_row.svg)

```yaml
chysl: 0.3.2
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
```
## Specification

[JSON Schema](piechart.md)

Pie chart displaying slices.

- **chart**:
  - *required*
  - *const* 'piechart'
- **title**: Title of the pie chart.
  - *See* [text](schema_defs.md#text).
- **diameter**: Diameter of the pie chart.
  - *type*: float
  - *exclusiveMinimum*: 0
  - *default*: 200
- **total**: Total value to relate slice values to.
  - *type*: float
  - *exclusiveMinimum*: 0
- **start**: Starting point for first slice; in degrees from the top.
  - *type*: float
- **palette**: Palette for slice colors; used for slices lacking color specification.
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
    - **color**: Color of the slice.
      - *See* [color](schema_defs.md#color).

