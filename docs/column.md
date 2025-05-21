# column

- [Examples](#examples)
  - [universe_earth](#universe_earth)
  - [cpies](#cpies)
  - [cnotes](#cnotes)
  - [notes](#notes)

- [Specification](#specification)

## Examples

### universe_earth

![universe_earth SVG](universe_earth.svg)

```yaml
chysl:
  version: 0.2.4
  software: Chysl (Python) 0.2.4
chart: column
title: Universe and Earth
entries:
- chart: timelines
  title:
    text: Universe
    bold: true
    color: blue
  entries:
  - entry: event
    label: Big Bang
    timeline: Universe
    color: red
    instant: -13787000000
    marker: burst
  - entry: period
    label: Milky Way galaxy
    timeline: Universe
    color: navy
    begin:
      value: -7500000000
      low: -8500000000
    end: 0
    fuzzy: gradient
  - entry: period
    label: Earth
    color: lightgreen
    begin: -4567000000
    end: 0
  legend: false
  axis:
    absolute: true
    caption: Billion years ago
- chart: timelines
  title: Earth
  entries:
  - entry: period
    label: Earth
    begin: -4567000000
    end: 0
  - entry: period
    label: Archean
    color: wheat
    begin:
      value: -4000000000
      low: -4100000000
      high: -3950000000
    end:
      value: -2500000000
      error: 200000000
    fuzzy: gradient
  - entry: event
    label: LUCA?
    timeline: Unicellular
    instant: -4200000000
  - entry: period
    label: Unicellular organisms
    timeline: Unicellular
    begin:
      value: -3480000000
      low: -4200000000
    end: 0
    fuzzy: gradient
  - entry: period
    label: Eukaryotes
    begin: -1650000000
    end: 0
  - entry: period
    label: Engineers
    color: lightgray
    begin:
      value: -3300000000
      error: 200000000
    end: -1650000000
    fuzzy: wedge
  - entry: period
    label: Photosynthesis
    color: springgreen
    begin: -3400000000
    end: 0
  - entry: period
    label: Plants
    timeline: Photosynthesis
    color: green
    begin: -470000000
    end: 0
    placement: left
  legend: false
  axis:
    absolute: true
    caption: Billion years ago
```
### cpies

![cpies SVG](cpies.svg)

```yaml
chysl:
  version: 0.2.4
  software: Chysl (Python) 0.2.4
chart: column
title: Pies in column
entries:
- chart: piechart
  title: Strawberry pie
  entries:
  - entry: slice
    label: Flour
    value: 7
    color: white
  - entry: slice
    label: Eggs
    value: 2
    color: yellow
  - entry: slice
    label: Butter
    value: 3
    color: gold
  - entry: slice
    label: Strawberries
    value: 3
    color: orangered
  diameter: 100
- chart: piechart
  title: Rhubarb pie
  entries:
  - entry: slice
    label: Flour
    value: 7
    color: white
  - entry: slice
    label: Eggs
    value: 2
    color: yellow
  - entry: slice
    label: Butter
    value: 3
    color: gold
  - entry: slice
    label: Rhubarb
    value: 3
    color: green
- chart: note
  title: Comment
  body: Strawberry pie is good.
  footer:
    text: Copyright 2025 Per Kraulis
    italic: true
```
### cnotes

![cnotes SVG](cnotes.svg)

```yaml
chysl:
  version: 0.2.4
  software: Chysl (Python) 0.2.4
chart: column
entries:
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
- chart: note
  footer: Footer
- chart: note
  title: Header
  body: Body
  footer: Footer
  line: 0
- include: declaration.yaml
```
### notes

![notes SVG](notes.svg)

```yaml
chysl:
  version: 0.2.4
  software: Chysl (Python) 0.2.4
chart: board
entries:
- x: 0
  y: 0
  scale: 1.5
  component:
    chart: column
    entries:
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
    - chart: note
      footer: Footer
    - chart: note
      title: Header
      body: Body
      footer: Footer
      line: 0
    - include: declaration.yaml
```
## Specification

[JSON Schema](column.md)

Charts stacked in a column.

- **chart**:
  - *required*
  - *const* 'column'
- **title**: Title of the column chart.
  - *See* [text](schema_defs.md#text).
- **align**: Align charts horizontally within the column.
  - *one of*: 'left', 'center', 'right'
  - *default*: 'center'
- **entries**: Component charts in the column.
  - *required*
  - *type*: sequence
  - *items*:
    - *See* [chart_or_include](schema_defs.md#chart_or_include).

