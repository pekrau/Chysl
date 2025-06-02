# timelines

- [Examples](#examples)
  - [universe](#universe)
  - [earth](#earth)
  - [universe_earth](#universe_earth)
  - [markers](#markers)
  - [poster](#poster)
  - [dimensions](#dimensions)

- [Specification](#specification)

## Examples

### universe

![universe SVG](universe.svg)

```yaml
chysl: 0.3.7
chart: timelines
title:
  text: Universe
  bold: true
  color: blue
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
  absolute: true
  caption: Billion years ago
grid: false
```
### earth

![earth SVG](earth.svg)

```yaml
chysl: 0.3.7
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
  absolute: true
  caption: Billion years ago
```
### universe_earth

![universe_earth SVG](universe_earth.svg)

```yaml
chysl: 0.3.7
chart: column
title: Universe and Earth
subcharts:
- chart: timelines
  title:
    text: Universe
    bold: true
    color: blue
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
    absolute: true
    caption: Billion years ago
  grid: false
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
    absolute: true
    caption: Billion years ago
```
### markers

![markers SVG](markers.svg)

```yaml
chysl: 0.3.7
chart: column
subcharts:
- chart: scatter2d
  title: Geometry markers
  width: 300
  xaxis:
    min: 0
    max: 3.5
    labels: false
  yaxis:
    labels: false
  xgrid: false
  ygrid: false
  points:
  - x: 0.2
    y: 1
    color: gray
    marker: disc
    label: disc
  - x: 1.2
    y: 1
    color: coral
    marker: circle
    label: circle
  - x: 2.2
    y: 1
    color: dodgerblue
    marker: oval
    label: oval
  - x: 0.2
    y: 2
    color: orange
    marker: oval-vertical
    label: oval-vertical
  - x: 1.2
    y: 2
    color: lime
    marker: oval-horizontal
    label: oval-horizontal
  - x: 2.2
    y: 2
    color: gray
    marker: ellipse
    label: ellipse
  - x: 0.2
    y: 3
    color: coral
    marker: ellipse-vertical
    label: ellipse-vertical
  - x: 1.2
    y: 3
    color: dodgerblue
    marker: ellipse-horizontal
    label: ellipse-horizontal
  - x: 2.2
    y: 3
    color: orange
    marker: block
    label: block
  - x: 0.2
    y: 4
    color: lime
    marker: square
    label: square
  - x: 1.2
    y: 4
    color: gray
    marker: square-cross
    label: square-cross
  - x: 2.2
    y: 4
    color: coral
    marker: diamond
    label: diamond
  - x: 0.2
    y: 5
    color: dodgerblue
    marker: diamond-cross
    label: diamond-cross
  - x: 1.2
    y: 5
    color: orange
    marker: diamond-fill
    label: diamond-fill
  - x: 2.2
    y: 5
    color: lime
    marker: pyramid
    label: pyramid
  - x: 0.2
    y: 6
    color: gray
    marker: triangle
    label: triangle
  - x: 1.2
    y: 6
    color: coral
    marker: wedge
    label: wedge
  - x: 2.2
    y: 6
    color: dodgerblue
    marker: trigon
    label: trigon
  - x: 0.2
    y: 7
    color: orange
    marker: pentagon
    label: pentagon
  - x: 1.2
    y: 7
    color: lime
    marker: pentagon-fill
    label: pentagon-fill
  - x: 2.2
    y: 7
    color: gray
    marker: hexagon
    label: hexagon
  - x: 0.2
    y: 8
    color: coral
    marker: hexagon-fill
    label: hexagon-fill
  - x: 1.2
    y: 8
    color: dodgerblue
    marker: heptagon
    label: heptagon
  - x: 2.2
    y: 8
    color: orange
    marker: heptagon-fill
    label: heptagon-fill
  - x: 0.2
    y: 9
    color: lime
    marker: octagon
    label: octagon
  - x: 1.2
    y: 9
    color: gray
    marker: octagon-fill
    label: octagon-fill
- chart: scatter2d
  title: Symbol markers
  width: 300
  xaxis:
    min: 0
    max: 3.5
    labels: false
  yaxis:
    labels: false
  xgrid: false
  ygrid: false
  points:
  - x: 0.2
    y: 1
    color: coral
    marker: cross
    label: cross
  - x: 1.2
    y: 1
    color: dodgerblue
    marker: plus
    label: plus
  - x: 2.2
    y: 1
    color: orange
    marker: minus
    label: minus
  - x: 0.2
    y: 2
    color: lime
    marker: bar
    label: bar
  - x: 1.2
    y: 2
    color: gray
    marker: check
    label: check
  - x: 2.2
    y: 2
    color: coral
    marker: burst
    label: burst
  - x: 0.2
    y: 3
    color: dodgerblue
    marker: infinity
    label: infinity
  - x: 1.2
    y: 3
    color: orange
    marker: none
    label: none
- chart: scatter2d
  title: Astronomy markers
  width: 300
  xaxis:
    min: 0
    max: 3.5
    labels: false
  yaxis:
    labels: false
  xgrid: false
  ygrid: false
  points:
  - x: 0.2
    y: 1
    color: lime
    marker: star
    label: star
  - x: 1.2
    y: 1
    color: gray
    marker: star-fill
    label: star-fill
  - x: 2.2
    y: 1
    color: coral
    marker: galaxy
    label: galaxy
  - x: 0.2
    y: 2
    color: dodgerblue
    marker: sun
    label: sun
  - x: 1.2
    y: 2
    color: orange
    marker: mercury
    label: mercury
  - x: 2.2
    y: 2
    color: lime
    marker: venus
    label: venus
  - x: 0.2
    y: 3
    color: gray
    marker: earth
    label: earth
  - x: 1.2
    y: 3
    color: coral
    marker: moon
    label: moon
  - x: 2.2
    y: 3
    color: dodgerblue
    marker: mars
    label: mars
  - x: 0.2
    y: 4
    color: orange
    marker: jupiter
    label: jupiter
  - x: 1.2
    y: 4
    color: lime
    marker: saturn
    label: saturn
  - x: 2.2
    y: 4
    color: gray
    marker: uranus
    label: uranus
  - x: 0.2
    y: 5
    color: coral
    marker: neptune
    label: neptune
- chart: scatter2d
  title: Greek markers
  width: 300
  xaxis:
    min: 0
    max: 3.5
    labels: false
  yaxis:
    labels: false
  xgrid: false
  ygrid: false
  points:
  - x: 0.2
    y: 1
    color: dodgerblue
    marker: alpha
    label: alpha
  - x: 1.2
    y: 1
    color: orange
    marker: beta
    label: beta
  - x: 2.2
    y: 1
    color: lime
    marker: gamma
    label: gamma
  - x: 0.2
    y: 2
    color: gray
    marker: delta
    label: delta
  - x: 1.2
    y: 2
    color: coral
    marker: epsilon
    label: epsilon
  - x: 2.2
    y: 2
    color: dodgerblue
    marker: zeta
    label: zeta
  - x: 0.2
    y: 3
    color: orange
    marker: eta
    label: eta
  - x: 1.2
    y: 3
    color: lime
    marker: theta
    label: theta
  - x: 2.2
    y: 3
    color: gray
    marker: iota
    label: iota
  - x: 0.2
    y: 4
    color: coral
    marker: kappa
    label: kappa
  - x: 1.2
    y: 4
    color: dodgerblue
    marker: lambda
    label: lambda
  - x: 2.2
    y: 4
    color: orange
    marker: mu
    label: mu
  - x: 0.2
    y: 5
    color: lime
    marker: nu
    label: nu
  - x: 1.2
    y: 5
    color: gray
    marker: xi
    label: xi
  - x: 2.2
    y: 5
    color: coral
    marker: omicron
    label: omicron
  - x: 0.2
    y: 6
    color: dodgerblue
    marker: pi
    label: pi
  - x: 1.2
    y: 6
    color: orange
    marker: rho
    label: rho
  - x: 2.2
    y: 6
    color: lime
    marker: sigma
    label: sigma
  - x: 0.2
    y: 7
    color: gray
    marker: sigma1
    label: sigma1
  - x: 1.2
    y: 7
    color: coral
    marker: sigma2
    label: sigma2
  - x: 2.2
    y: 7
    color: dodgerblue
    marker: tau
    label: tau
  - x: 0.2
    y: 8
    color: orange
    marker: upsilon
    label: upsilon
  - x: 1.2
    y: 8
    color: lime
    marker: phi
    label: phi
  - x: 2.2
    y: 8
    color: gray
    marker: chi
    label: chi
  - x: 0.2
    y: 9
    color: coral
    marker: psi
    label: psi
  - x: 1.2
    y: 9
    color: dodgerblue
    marker: omega
    label: omega
```
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
### dimensions

![dimensions SVG](dimensions.svg)

```yaml
chysl: 0.3.7
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
```
## Specification

[JSON Schema](timelines.md)

Timelines having events and periods.

- **chart**:
  - *required*
  - *const* 'timelines'
- **title**:
  - *See* [title](schema_defs.md#title).
- **description**:
  - *See* [description](schema_defs.md#description).
- **width**: Width of the chart, including legends etc.
  - *type*: float
  - *exclusiveMinimum*: 0
  - *default*: 600
- **legend**: Display legend.
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
      - **href**:
        - *See* [uri](schema_defs.md#uri).
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
      - **href**:
        - *See* [uri](schema_defs.md#uri).

