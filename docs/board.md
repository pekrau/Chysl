# board

- [Examples](#examples)
  - [poster](#poster)
  - [notes](#notes)

- [Specification](#specification)

## Examples

### poster

![poster SVG](poster.svg)

```yaml
chysl: 0.4.0
chart: board
title: Poster
items:
- x: 150
  y: 10
  subchart:
    chart: note
    title: By Per Kraulis
    body: Ph.D.
    footer: Stockholm University
- x: 0
  y: 150
  subchart:
    include: universe.yaml
- x: 50
  y: 290
  subchart:
    include: earth.yaml
```
### notes

![notes SVG](notes.svg)

```yaml
chysl: 0.4.0
chart: board
items:
- x: 0
  y: 0
  subchart:
    chart: column
    title: Notes in a column
    subcharts:
    - chart: note
      title: Header
      body: Body
      footer: Footer
    - chart: note
      title: Header
      body: Body
    - chart: note
      body: Body
      footer: Footer
    - chart: note
      title: Header
    - chart: note
      body: Body
      width: 200
    - chart: note
      footer: Footer
      width: 200
    - chart: note
      title: Header
      body: Body (no lines)
      footer: Footer
      line: 0
      width: 200
    - include: declaration.yaml
    padding: 4
  scale: 1.5
```
## Specification

[JSON Schema](board.md)

Chart to place charts at specified positions, with optional opacity.

- **chart**:
  - *required*
  - *const* 'board'
- **title**: Title of the chart.
  - *See* [text](schema_defs.md#text).
- **description**: Description of the chart. Rendered as <desc> in SVG.
  - *type*: string
- **items**: Subcharts at specified positions.
  - *required*
  - *type*: sequence
  - *items*:
    - *type*: mapping
    - **subchart**:
      - *See* [chart_or_include](schema_defs.md#chart_or_include).
      - *required*
    - **x**: Absolute position of subchart. Left is 0.
      - *required*
      - *type*: float
      - *minimum*: 0
    - **y**: Absolute position of subchart. Top is 0.
      - *required*
      - *type*: float
      - *minimum*: 0
    - **scale**: Scaling of the subchart.
      - *type*: float
      - *exclusiveMinimum*: 0
      - *default*: 1
    - **opacity**: Opacity of the subchart.
      - *type*: float
      - *minimum*: 0
      - *maximum*: 1
      - *default*: 1

