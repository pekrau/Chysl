# board

- [Examples](#examples)
  - [poster](#poster)
  - [notes](#notes)

- [Specification](#specification)

## Examples

### poster

![poster SVG](poster.svg)

```yaml
chysl: 0.3.7
chart: board
title: Poster
items:
- x: 250
  y: 10
  subchart:
    chart: note
    title: By Per Kraulis
    body: Ph.D.
    footer: Stockholm University
- x: 0
  y: 100
  subchart:
    include: universe.yaml
- x: 50
  y: 230
  subchart:
    include: earth.yaml
```
### notes

![notes SVG](notes.svg)

```yaml
chysl: 0.3.7
chart: board
items:
- x: 0
  y: 0
  subchart:
    chart: column
    subcharts:
    - chart: note
      title: Header
      description: Body
      body: Footer
    - chart: note
      title: Header
      description: Body
    - chart: note
      body: Body
      footer: Footer
    - chart: note
      title: Header
    - chart: note
      body: Body
    - chart: note
      footer: Footer
    - chart: note
      title: Header
      description: Body
      body: Footer
      line: 0
    - include: declaration.yaml
  scale: 1.5
```
## Specification

[JSON Schema](board.md)

Chart to place charts at specified positions.

- **chart**:
  - *required*
  - *const* 'board'
- **title**:
  - *See* [title](schema_defs.md#title).
- **description**:
  - *See* [description](schema_defs.md#description).
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
    - **opacity**:
      - *See* [opacity](schema_defs.md#opacity).

