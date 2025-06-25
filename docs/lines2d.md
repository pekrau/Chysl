# lines2d

- [Examples](#examples)
  - [lines_random_walks](#lines_random_walks)

- [Specification](#specification)

## Examples

### lines_random_walks

[Sqlite database file](lines_random_walks.db)

![lines_random_walks SVG](lines_random_walks.svg)

```yaml
chysl: 0.5.0
chart: lines2d
title: 'Random walks (source: db)'
lines:
- thickness: 10
  color: blue
  opacity: 0.25
  href: https://en.wikipedia.org/wiki/Random_walk
  line:
  - x: -15
    y: -15
  - x: -15
    y: 15
  - x: 15
    y: 15
  - x: 15
    y: -15
  - x: -15
    y: -15
- color: red
  line:
    source: lines_random_walks.db
    database: sqlite
    select: SELECT x, y FROM walks WHERE run=1 ORDER BY i
- color: green
  line:
    source: lines_random_walks.db
    database: sqlite
    select: SELECT x, y FROM walks WHERE run=2 ORDER BY i
- color: blue
  line:
    source: lines_random_walks.db
    database: sqlite
    select: SELECT x, y FROM walks WHERE run=3 ORDER BY i
- color: lime
  line:
    source: lines_random_walks.db
    database: sqlite
    select: SELECT x, y FROM walks WHERE run=4 ORDER BY i
- color: orange
  line:
    source: lines_random_walks.db
    database: sqlite
    select: SELECT x, y FROM walks WHERE run=5 ORDER BY i
- color: cyan
  line:
    source: lines_random_walks.db
    database: sqlite
    select: SELECT x, y FROM walks WHERE run=6 ORDER BY i
- color: gold
  line:
    source: lines_random_walks.db
    database: sqlite
    select: SELECT x, y FROM walks WHERE run=7 ORDER BY i
- color: dodgerblue
  line:
    source: lines_random_walks.db
    database: sqlite
    select: SELECT x, y FROM walks WHERE run=8 ORDER BY i
- color: gray
  line:
    source: lines_random_walks.db
    database: sqlite
    select: SELECT x, y FROM walks WHERE run=9 ORDER BY i
```
## Specification

[JSON Schema](lines2d.md)

2D lines chart.

- **chart**:
  - *required*
  - *const* 'lines2d'
- **title**: Title of the chart.
  - *See* [text](schema_defs.md#text).
- **description**: Description of the chart. Rendered as <desc> in SVG.
  - *type*: string
- **lines**: Array of lines.
  - *required*
  - *type*: sequence
  - *items*:
    - *type*: mapping
    - **line**:
      - *required*
      - Alternative 1: Inline list of 2D points.
        - *type*: sequence
        - *items*:
          - *type*: mapping
          - **x**:
            - *type*: float
          - **y**:
            - *type*: float
      - Alternative 2: External source of 2D points data.
        - *See* [datasource](schema_defs.md#datasource).
    - **thickness**: Thickness of the line (pixels).
      - *type*: float
      - *default*: 1
    - **color**: Color of the line.
      - *type*: string
      - *format*: color
      - *default*: 'black'
    - **opacity**: Opacity of the line.
      - *type*: float
      - *minimum*: 0
      - *maximum*: 1
      - *default*: 1
    - **href**: A link URL, absolute or relative.
      - *type*: string
      - *format*: uri-reference
- **width**: Width of the chart.
  - *type*: float
  - *exclusiveMinimum*: 0
  - *default*: 600
- **height**: Height of the chart.
  - *type*: float
  - *exclusiveMinimum*: 0
  - *default*: 600
- **frame**: Chart area frame specification.
  - *See* [frame](schema_defs.md#frame).
- **xaxis**: X axis specification.
  - *See* [axis](schema_defs.md#axis).
- **yaxis**: Y axis specification.
  - *See* [axis](schema_defs.md#axis).
- **xgrid**: X grid specification.
  - *See* [grid](schema_defs.md#grid).
- **ygrid**: Y grid specification.
  - *See* [grid](schema_defs.md#grid).
- **thickness**: Default thickness of the lines (pixels).
  - *type*: float
  - *default*: 1
- **color**: Default line color.
  - *type*: string
  - *format*: color
  - *default*: 'black'
- **opacity**: Default line opacity.
  - *type*: float
  - *minimum*: 0
  - *maximum*: 1
  - *default*: 1

