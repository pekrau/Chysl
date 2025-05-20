# row

- [Examples](#examples)
- [Specification](#specification)
  - [rpies](#rpies)

## Examples

### rpies

![rpies SVG](rpies.svg)

```yaml
chysl:
  version: 0.1.0
  software: Chysl (Python) 0.1.0
  timestamp: '2025-05-20T06:45:53+00:00'
chart: row
title: Pies in row
entries:
- chart: piechart
  title: Strawberry pie
  entries:
  - entry: slice
    label: Flour
    value: 7
  - entry: slice
    label: Eggs
    value: 2
  - entry: slice
    label: Butter
    value: 3
  - entry: slice
    label: Strawberries
    value: 3
  diameter: 300
  palette:
  - white
  - yellow
  - gold
  - red
- chart: piechart
  title: Rhubarb pie
  entries:
  - entry: slice
    label: Flour
    value: 7
  - entry: slice
    label: Eggs
    value: 2
  - entry: slice
    label: Butter
    value: 3
  - entry: slice
    label: Rhubarb
    value: 3
    color: green
  palette:
  - white
  - yellow
  - gold
  - red
```
## Specification

[JSON Schema](row.md)

Charts arranged in a row.

- **chart**:
  - *required*
- **title**: Title of the column chart.
    - *definition*: See [here](timelines.md)
- **align**: Align charts vertically within the row.
  - *one of*: 'bottom', 'middle', 'top'
  - *default*: 'middle'
- **entries**: Component charts in the row.
  - *required*
  - *type*: sequence
  - *items*:
      - *definition*: See [here](column.md)

