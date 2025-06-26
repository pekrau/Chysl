# timelines

- [Examples](#examples)
  - [universe](#universe)
  - [earth](#earth)
  - [universe_earth](#universe_earth)
  - [poster](#poster)
  - [dimensions](#dimensions)

- [Specification](#specification)

## Examples

### universe

![universe SVG](universe.svg)

```yaml
chysl: 0.5.1
chart: timelines
title:
  size: 24
  bold: true
  color: darkorchid
  text: Universe
entries:
- label: Big Bang
  timeline: Universe
  color: red
  instant: -13787000000
  marker: burst
- label: Milky Way galaxy
  timeline: Universe
  color: dodgerblue
  begin:
    value: -7500000000
    low: -8500000000
  end: 0
  fuzzy: gradient
  href: https://en.wikipedia.org/wiki/Milky_Way
- timeline: Universe
  color: white
  instant: -7500000000
  marker: galaxy
  href: https://en.wikipedia.org/wiki/Milky_Way
- label: Earth
  color: lightgreen
  begin: -4567000000
  end: 0
axis:
  max: 50000000
  absolute: true
  caption: Billion years ago
```
### earth

![earth SVG](earth.svg)

```yaml
chysl: 0.5.1
chart: timelines
title: Earth
entries:
- label: Earth
  color: skyblue
  begin: -4567000000
  end: 0
- label: Archean
  color: wheat
  begin:
    value: -4000000000
    low: -4100000000
    high: -3950000000
  end:
    value: -2500000000
    error: 200000000
  fuzzy: gradient
- label: LUCA?
  timeline: Unicellular
  instant: -4200000000
- label: Unicellular organisms
  timeline: Unicellular
  begin:
    value: -3480000000
    low: -4200000000
  end: 0
  fuzzy: gradient
- label: Eukaryotes
  begin:
    value: -1650000000
    error: 200000000
  end: 0
- label: Photosynthesis
  color: springgreen
  begin:
    value: -3400000000
    high: -2600000000
  end: 0
  fuzzy: gradient
- label: Plants
  timeline: Photosynthesis
  color: green
  begin:
    value: -470000000
    error: 50000000
  end: 0
  placement: left
  fuzzy: wedge
axis:
  max: 20000000
  absolute: true
  caption: Billion years ago
```
### universe_earth

![universe_earth SVG](universe_earth.svg)

```yaml
chysl: 0.5.1
chart: column
title: Universe and Earth
subcharts:
- chart: timelines
  title:
    size: 24
    bold: true
    color: darkorchid
    text: Universe
  entries:
  - label: Big Bang
    timeline: Universe
    color: red
    instant: -13787000000
    marker: burst
  - label: Milky Way galaxy
    timeline: Universe
    color: dodgerblue
    begin:
      value: -7500000000
      low: -8500000000
    end: 0
    fuzzy: gradient
    href: https://en.wikipedia.org/wiki/Milky_Way
  - timeline: Universe
    color: white
    instant: -7500000000
    marker: galaxy
    href: https://en.wikipedia.org/wiki/Milky_Way
  - label: Earth
    color: lightgreen
    begin: -4567000000
    end: 0
  legend: false
  axis:
    max: 50000000
    absolute: true
    caption: Billion years ago
- chart: timelines
  title: Earth
  entries:
  - label: Earth
    color: skyblue
    begin: -4567000000
    end: 0
  - label: Archean
    color: wheat
    begin:
      value: -4000000000
      low: -4100000000
      high: -3950000000
    end:
      value: -2500000000
      error: 200000000
    fuzzy: gradient
  - label: LUCA?
    timeline: Unicellular
    instant: -4200000000
  - label: Unicellular organisms
    timeline: Unicellular
    begin:
      value: -3480000000
      low: -4200000000
    end: 0
    fuzzy: gradient
  - label: Eukaryotes
    begin:
      value: -1650000000
      error: 200000000
    end: 0
  - label: Photosynthesis
    color: springgreen
    begin:
      value: -3400000000
      high: -2600000000
    end: 0
    fuzzy: gradient
  - label: Plants
    timeline: Photosynthesis
    color: green
    begin:
      value: -470000000
      error: 50000000
    end: 0
    placement: left
    fuzzy: wedge
  legend: false
  axis:
    max: 20000000
    absolute: true
    caption: Billion years ago
```
### poster

![poster SVG](poster.svg)

```yaml
chysl: 0.5.1
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
  scale: 1.5
- x: 0
  y: 150
  subchart:
    include: universe.yaml
- x: 50
  y: 290
  subchart:
    include: earth.yaml
```
### dimensions

![dimensions SVG](dimensions.svg)

```yaml
chysl: 0.5.1
chart: column
title: Dimension tick ranges
subcharts:
- chart: timelines
  title: 1 - 1.00001
  entries:
  - begin: 1
    end: 1.00001
- chart: timelines
  title: 1 - 1.0001
  entries:
  - begin: 1
    end: 1.0001
- chart: timelines
  title: 1 - 1.0002
  entries:
  - begin: 1
    end: 1.0002
- chart: timelines
  title: 1 - 1.1
  entries:
  - begin: 1
    end: 1.1
- chart: timelines
  title: 1 - 2
  entries:
  - begin: 1
    end: 2
- chart: timelines
  title: 1 - 5
  entries:
  - begin: 1
    end: 5
- chart: timelines
  title: 1 - 10
  entries:
  - begin: 1
    end: 10
- chart: timelines
  title: 1 - 2000
  entries:
  - begin: 1
    end: 2000
- chart: timelines
  title: 1 - 10000000
  entries:
  - begin: 1
    end: 10000000
- chart: timelines
  title: 1 - 10000000000
  entries:
  - begin: 1
    end: 10000000000
padding: 20
```
## Specification

[JSON Schema](timelines.md)

Timelines having events and periods.

- **chart**:
  - *required*
  - *const* 'timelines'
- **title**: Title of the chart.
  - *See* [text](schema_defs.md#text).
- **description**: Description of the chart. Rendered as <desc> in SVG.
  - *type*: string
- **width**: Width of the chart area (pixels).
  - *type*: float
  - *exclusiveMinimum*: 0
  - *default*: 600
- **frame**: Chart area frame specification.
  - *See* [frame](schema_defs.md#frame).
- **legend**: Legend to be displayed or not.
  - *type*: boolean
  - *default*: true
- **axis**: Time axis specification.
  - *See* [axis](schema_defs.md#axis).
- **grid**: Grid specification.
  - *See* [grid](schema_defs.md#grid).
- **entries**: Entries (events, periods) in the timelines.
  - *required*
  - *type*: sequence
  - *items*:
    - Alternative 1: Event at an instant in time.
      - *type*: mapping
      - **instant**: Time of the event.
        - *See* [fuzzy_number](schema_defs.md#fuzzy_number).
        - *required*
      - **label**: Description of the event.
        - *type*: string
      - **timeline**: Timeline to place the event in.
        - *type*: string
      - **marker**: Marker for event.
        - *See* [marker](schema_defs.md#marker).
      - **color**: Color of the event marker.
        - *type*: string
        - *format*: color
        - *default*: 'black'
      - **placement**: Placement of event label.
        - *one of*: 'left', 'center', 'right'
        - *default*: 'right'
      - **fuzzy**: Error bar marker for fuzzy number.
        - *type*: boolean
        - *default*: true
      - **href**: A link URL, absolute or relative.
        - *type*: string
        - *format*: uri-reference
    - Alternative 2: Period of time.
      - *type*: mapping
      - **begin**: Starting time of the period.
        - *See* [fuzzy_number](schema_defs.md#fuzzy_number).
        - *required*
      - **end**: Ending time of the period.
        - *See* [fuzzy_number](schema_defs.md#fuzzy_number).
        - *required*
      - **label**: Description of the period.
        - *type*: string
      - **timeline**: Timeline to place the period in.
        - *type*: string
      - **color**: Color of the period graphic.
        - *type*: string
        - *format*: color
        - *default*: 'white'
      - **placement**: Placement of period label.
        - *one of*: 'left', 'center', 'right'
        - *default*: 'center'
      - **fuzzy**: Marker to use for fuzzy number.
        - *one of*: 'error', 'wedge', 'gradient', 'none'
        - *default*: 'error'
      - **href**: A link URL, absolute or relative.
        - *type*: string
        - *format*: uri-reference

