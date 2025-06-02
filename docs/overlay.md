# overlay

- [Examples](#examples)
  - [overlay](#overlay)

- [Specification](#specification)

## Examples

### overlay

![overlay SVG](overlay.svg)

```yaml
chysl: 0.3.7
chart: overlay
title: One scatterplot on top of another
layers:
- subchart:
    chart: scatter2d
    size: 60
    points:
    - x: 1
      y: 1
      color: gold
      href: https://en.wikipedia.org/wiki/Gold
    - x: 2
      y: 2
      color: blue
    - x: 3
      y: 3
      color: red
- opacity: 0.5
  subchart:
    chart: scatter2d
    size: 30
    points:
    - x: 1
      y: 1
      marker: alpha
    - x: 2
      y: 2
      color: white
      marker: beta
    - x: 3
      y: 3
      marker: gamma
```
## Specification

[JSON Schema](overlay.md)

Charts overlayed over one another, with optional opacity.

- **chart**:
  - *required*
  - *const* 'overlay'
- **title**:
  - *See* [title](schema_defs.md#title).
- **description**:
  - *See* [description](schema_defs.md#description).
- **layers**: Charts to overlay, with optional opacity.
  - *required*
  - *type*: sequence
  - *items*:
    - *type*: mapping
    - **subchart**:
      - *See* [chart_or_include](schema_defs.md#chart_or_include).
      - *required*
    - **opacity**:
      - *See* [opacity](schema_defs.md#opacity).

