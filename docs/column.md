# column

- [Examples](#examples)
  - [universe_earth](#universe_earth)
  - [pies_column](#pies_column)
  - [notes_column](#notes_column)
  - [notes](#notes)
  - [markers](#markers)
  - [dimensions](#dimensions)

- [Specification](#specification)

## Examples

### universe_earth

![universe_earth SVG](universe_earth.svg)

```yaml
chysl:
  version: 0.2.7
  software: Chysl (Python) 0.2.7
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
    color: dodgerblue
    begin:
      value: -7500000000
      low: -8500000000
    end: 0
    fuzzy: gradient
  - entry: event
    label: ''
    timeline: Universe
    color: navy
    instant: -8500000000
    marker: galaxy
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
### pies_column

![pies_column SVG](pies_column.svg)

```yaml
chysl:
  version: 0.2.7
  software: Chysl (Python) 0.2.7
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
### notes_column

![notes_column SVG](notes_column.svg)

```yaml
chysl:
  version: 0.2.7
  software: Chysl (Python) 0.2.7
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
  version: 0.2.7
  software: Chysl (Python) 0.2.7
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
### markers

![markers SVG](markers.svg)

```yaml
chysl:
  version: 0.2.7
  software: Chysl (Python) 0.2.7
chart: row
title: Markers
entries:
- chart: column
  entries:
  - chart: timelines
    title: Geometry markers
    entries:
    - entry: period
      label: Length
      begin: 0
      end: 3
    - entry: event
      label: disc
      timeline: Row 1
      color: gray
      instant: 0.25
      marker: disc
    - entry: event
      label: circle
      timeline: Row 1
      color: coral
      instant: 1.25
      marker: circle
    - entry: event
      label: oval
      timeline: Row 1
      color: dodgerblue
      instant: 2.25
    - entry: event
      label: oval-vertical
      timeline: Row 2
      color: orange
      instant: 0.25
      marker: oval-vertical
    - entry: event
      label: oval-horizontal
      timeline: Row 2
      color: lime
      instant: 1.25
      marker: oval-horizontal
    - entry: event
      label: ellipse
      timeline: Row 2
      color: gray
      instant: 2.25
      marker: ellipse
    - entry: event
      label: ellipse-vertical
      timeline: Row 3
      color: coral
      instant: 0.25
      marker: ellipse-vertical
    - entry: event
      label: ellipse-horizontal
      timeline: Row 3
      color: dodgerblue
      instant: 1.25
      marker: ellipse-horizontal
    - entry: event
      label: block
      timeline: Row 3
      color: orange
      instant: 2.25
      marker: block
    - entry: event
      label: square
      timeline: Row 4
      color: lime
      instant: 0.25
      marker: square
    - entry: event
      label: diamond
      timeline: Row 4
      color: gray
      instant: 1.25
      marker: diamond
    - entry: event
      label: diamond-fill
      timeline: Row 4
      color: coral
      instant: 2.25
      marker: diamond-fill
    - entry: event
      label: pyramid
      timeline: Row 5
      color: dodgerblue
      instant: 0.25
      marker: pyramid
    - entry: event
      label: triangle
      timeline: Row 5
      color: orange
      instant: 1.25
      marker: triangle
    - entry: event
      label: wedge
      timeline: Row 5
      color: lime
      instant: 2.25
      marker: wedge
    - entry: event
      label: trigon
      timeline: Row 6
      color: gray
      instant: 0.25
      marker: trigon
    - entry: event
      label: pentagon
      timeline: Row 6
      color: coral
      instant: 1.25
      marker: pentagon
    - entry: event
      label: pentagon-fill
      timeline: Row 6
      color: dodgerblue
      instant: 2.25
      marker: pentagon-fill
    - entry: event
      label: hexagon
      timeline: Row 7
      color: orange
      instant: 0.25
      marker: hexagon
    - entry: event
      label: hexagon-fill
      timeline: Row 7
      color: lime
      instant: 1.25
      marker: hexagon-fill
    - entry: event
      label: heptagon
      timeline: Row 7
      color: gray
      instant: 2.25
      marker: heptagon
    - entry: event
      label: heptagon-fill
      timeline: Row 8
      color: coral
      instant: 0.25
      marker: heptagon-fill
    - entry: event
      label: octagon
      timeline: Row 8
      color: dodgerblue
      instant: 1.25
      marker: octagon
    - entry: event
      label: octagon-fill
      timeline: Row 8
      color: orange
      instant: 2.25
      marker: octagon-fill
    - entry: event
      label: bar
      timeline: Row 9
      color: lime
      instant: 0.25
      marker: bar
    - entry: event
      label: bar-vertical
      timeline: Row 9
      color: gray
      instant: 1.25
      marker: bar-vertical
    - entry: event
      label: bar-horizontal
      timeline: Row 9
      color: coral
      instant: 2.25
      marker: bar-horizontal
    legend: false
    axis: false
  - chart: timelines
    title: Symbol markers
    entries:
    - entry: period
      label: Length
      begin: 0
      end: 3
    - entry: event
      label: cross
      timeline: Row 1
      color: dodgerblue
      instant: 0.25
      marker: cross
    - entry: event
      label: plus
      timeline: Row 1
      color: orange
      instant: 1.25
      marker: plus
    - entry: event
      label: check
      timeline: Row 1
      color: lime
      instant: 2.25
      marker: check
    - entry: event
      label: burst
      timeline: Row 2
      color: gray
      instant: 0.25
      marker: burst
    - entry: event
      label: infinity
      timeline: Row 2
      color: coral
      instant: 1.25
      marker: infinity
    - entry: event
      label: none
      timeline: Row 2
      color: dodgerblue
      instant: 2.25
      marker: none
    legend: false
    axis: false
  - chart: timelines
    title: Astronomy markers
    entries:
    - entry: period
      label: Length
      begin: 0
      end: 3
    - entry: event
      label: star
      timeline: Row 1
      color: orange
      instant: 0.25
      marker: star
    - entry: event
      label: star-fill
      timeline: Row 1
      color: lime
      instant: 1.25
      marker: star-fill
    - entry: event
      label: galaxy
      timeline: Row 1
      color: gray
      instant: 2.25
      marker: galaxy
    - entry: event
      label: sun
      timeline: Row 2
      color: coral
      instant: 0.25
      marker: sun
    - entry: event
      label: mercury
      timeline: Row 2
      color: dodgerblue
      instant: 1.25
      marker: mercury
    - entry: event
      label: venus
      timeline: Row 2
      color: orange
      instant: 2.25
      marker: venus
    - entry: event
      label: earth
      timeline: Row 3
      color: lime
      instant: 0.25
      marker: earth
    - entry: event
      label: moon
      timeline: Row 3
      color: gray
      instant: 1.25
      marker: moon
    - entry: event
      label: mars
      timeline: Row 3
      color: coral
      instant: 2.25
      marker: mars
    - entry: event
      label: jupiter
      timeline: Row 4
      color: dodgerblue
      instant: 0.25
      marker: jupiter
    - entry: event
      label: saturn
      timeline: Row 4
      color: orange
      instant: 1.25
      marker: saturn
    - entry: event
      label: uranus
      timeline: Row 4
      color: lime
      instant: 2.25
      marker: uranus
    - entry: event
      label: neptune
      timeline: Row 5
      color: gray
      instant: 0.25
      marker: neptune
    legend: false
    axis: false
  - chart: timelines
    title: Greek markers
    entries:
    - entry: period
      label: Length
      begin: 0
      end: 3
    - entry: event
      label: alpha
      timeline: Row 1
      color: coral
      instant: 0.25
      marker: alpha
    - entry: event
      label: beta
      timeline: Row 1
      color: dodgerblue
      instant: 1.25
      marker: beta
    - entry: event
      label: gamma
      timeline: Row 1
      color: orange
      instant: 2.25
      marker: gamma
    - entry: event
      label: delta
      timeline: Row 2
      color: lime
      instant: 0.25
      marker: delta
    - entry: event
      label: epsilon
      timeline: Row 2
      color: gray
      instant: 1.25
      marker: epsilon
    - entry: event
      label: zeta
      timeline: Row 2
      color: coral
      instant: 2.25
      marker: zeta
    - entry: event
      label: eta
      timeline: Row 3
      color: dodgerblue
      instant: 0.25
      marker: eta
    - entry: event
      label: theta
      timeline: Row 3
      color: orange
      instant: 1.25
      marker: theta
    - entry: event
      label: iota
      timeline: Row 3
      color: lime
      instant: 2.25
      marker: iota
    - entry: event
      label: kappa
      timeline: Row 4
      color: gray
      instant: 0.25
      marker: kappa
    - entry: event
      label: lambda
      timeline: Row 4
      color: coral
      instant: 1.25
      marker: lambda
    - entry: event
      label: mu
      timeline: Row 4
      color: dodgerblue
      instant: 2.25
      marker: mu
    - entry: event
      label: nu
      timeline: Row 5
      color: orange
      instant: 0.25
      marker: nu
    - entry: event
      label: xi
      timeline: Row 5
      color: lime
      instant: 1.25
      marker: xi
    - entry: event
      label: omicron
      timeline: Row 5
      color: gray
      instant: 2.25
      marker: omicron
    - entry: event
      label: pi
      timeline: Row 6
      color: coral
      instant: 0.25
      marker: pi
    - entry: event
      label: rho
      timeline: Row 6
      color: dodgerblue
      instant: 1.25
      marker: rho
    - entry: event
      label: sigma
      timeline: Row 6
      color: orange
      instant: 2.25
      marker: sigma
    - entry: event
      label: sigma1
      timeline: Row 7
      color: lime
      instant: 0.25
      marker: sigma1
    - entry: event
      label: sigma2
      timeline: Row 7
      color: gray
      instant: 1.25
      marker: sigma2
    - entry: event
      label: tau
      timeline: Row 7
      color: coral
      instant: 2.25
      marker: tau
    - entry: event
      label: upsilon
      timeline: Row 8
      color: dodgerblue
      instant: 0.25
      marker: upsilon
    - entry: event
      label: phi
      timeline: Row 8
      color: orange
      instant: 1.25
      marker: phi
    - entry: event
      label: chi
      timeline: Row 8
      color: lime
      instant: 2.25
      marker: chi
    - entry: event
      label: psi
      timeline: Row 9
      color: gray
      instant: 0.25
      marker: psi
    - entry: event
      label: omega
      timeline: Row 9
      color: coral
      instant: 1.25
      marker: omega
    legend: false
    axis: false
- chart: column
  entries:
  - chart: timelines
    title: Character markers
    entries:
    - entry: period
      label: Length
      begin: 0
      end: 3
    - entry: event
      label: a
      timeline: Row 1
      color: dodgerblue
      instant: 0.25
      marker: a
    - entry: event
      label: b
      timeline: Row 1
      color: orange
      instant: 1.25
      marker: b
    - entry: event
      label: c
      timeline: Row 1
      color: lime
      instant: 2.25
      marker: c
    - entry: event
      label: d
      timeline: Row 2
      color: gray
      instant: 0.25
      marker: d
    - entry: event
      label: e
      timeline: Row 2
      color: coral
      instant: 1.25
      marker: e
    - entry: event
      label: f
      timeline: Row 2
      color: dodgerblue
      instant: 2.25
      marker: f
    - entry: event
      label: g
      timeline: Row 3
      color: orange
      instant: 0.25
      marker: g
    - entry: event
      label: h
      timeline: Row 3
      color: lime
      instant: 1.25
      marker: h
    - entry: event
      label: i
      timeline: Row 3
      color: gray
      instant: 2.25
      marker: i
    - entry: event
      label: j
      timeline: Row 4
      color: coral
      instant: 0.25
      marker: j
    - entry: event
      label: k
      timeline: Row 4
      color: dodgerblue
      instant: 1.25
      marker: k
    - entry: event
      label: l
      timeline: Row 4
      color: orange
      instant: 2.25
      marker: l
    - entry: event
      label: m
      timeline: Row 5
      color: lime
      instant: 0.25
      marker: m
    - entry: event
      label: n
      timeline: Row 5
      color: gray
      instant: 1.25
      marker: n
    - entry: event
      label: o
      timeline: Row 5
      color: coral
      instant: 2.25
      marker: o
    - entry: event
      label: p
      timeline: Row 6
      color: dodgerblue
      instant: 0.25
      marker: p
    - entry: event
      label: q
      timeline: Row 6
      color: orange
      instant: 1.25
      marker: q
    - entry: event
      label: r
      timeline: Row 6
      color: lime
      instant: 2.25
      marker: r
    - entry: event
      label: s
      timeline: Row 7
      color: gray
      instant: 0.25
      marker: s
    - entry: event
      label: t
      timeline: Row 7
      color: coral
      instant: 1.25
      marker: t
    - entry: event
      label: u
      timeline: Row 7
      color: dodgerblue
      instant: 2.25
      marker: u
    - entry: event
      label: v
      timeline: Row 8
      color: orange
      instant: 0.25
      marker: v
    - entry: event
      label: w
      timeline: Row 8
      color: lime
      instant: 1.25
      marker: w
    - entry: event
      label: x
      timeline: Row 8
      color: gray
      instant: 2.25
      marker: x
    - entry: event
      label: y
      timeline: Row 9
      color: coral
      instant: 0.25
      marker: y
    - entry: event
      label: z
      timeline: Row 9
      color: dodgerblue
      instant: 1.25
      marker: z
    - entry: event
      label: A
      timeline: Row 9
      color: orange
      instant: 2.25
      marker: A
    - entry: event
      label: B
      timeline: Row 10
      color: lime
      instant: 0.25
      marker: B
    - entry: event
      label: C
      timeline: Row 10
      color: gray
      instant: 1.25
      marker: C
    - entry: event
      label: D
      timeline: Row 10
      color: coral
      instant: 2.25
      marker: D
    - entry: event
      label: E
      timeline: Row 11
      color: dodgerblue
      instant: 0.25
      marker: E
    - entry: event
      label: F
      timeline: Row 11
      color: orange
      instant: 1.25
      marker: F
    - entry: event
      label: G
      timeline: Row 11
      color: lime
      instant: 2.25
      marker: G
    - entry: event
      label: H
      timeline: Row 12
      color: gray
      instant: 0.25
      marker: H
    - entry: event
      label: I
      timeline: Row 12
      color: coral
      instant: 1.25
      marker: I
    - entry: event
      label: J
      timeline: Row 12
      color: dodgerblue
      instant: 2.25
      marker: J
    - entry: event
      label: K
      timeline: Row 13
      color: orange
      instant: 0.25
      marker: K
    - entry: event
      label: L
      timeline: Row 13
      color: lime
      instant: 1.25
      marker: L
    - entry: event
      label: M
      timeline: Row 13
      color: gray
      instant: 2.25
      marker: M
    - entry: event
      label: N
      timeline: Row 14
      color: coral
      instant: 0.25
      marker: N
    - entry: event
      label: O
      timeline: Row 14
      color: dodgerblue
      instant: 1.25
      marker: O
    - entry: event
      label: P
      timeline: Row 14
      color: orange
      instant: 2.25
      marker: P
    - entry: event
      label: Q
      timeline: Row 15
      color: lime
      instant: 0.25
      marker: Q
    - entry: event
      label: R
      timeline: Row 15
      color: gray
      instant: 1.25
      marker: R
    - entry: event
      label: S
      timeline: Row 15
      color: coral
      instant: 2.25
      marker: S
    - entry: event
      label: T
      timeline: Row 16
      color: dodgerblue
      instant: 0.25
      marker: T
    - entry: event
      label: U
      timeline: Row 16
      color: orange
      instant: 1.25
      marker: U
    - entry: event
      label: V
      timeline: Row 16
      color: lime
      instant: 2.25
      marker: V
    - entry: event
      label: W
      timeline: Row 17
      color: gray
      instant: 0.25
      marker: W
    - entry: event
      label: X
      timeline: Row 17
      color: coral
      instant: 1.25
      marker: X
    - entry: event
      label: Y
      timeline: Row 17
      color: dodgerblue
      instant: 2.25
      marker: Y
    - entry: event
      label: Z
      timeline: Row 18
      color: orange
      instant: 0.25
      marker: Z
    - entry: event
      label: '0'
      timeline: Row 18
      color: lime
      instant: 1.25
      marker: '0'
    - entry: event
      label: '1'
      timeline: Row 18
      color: gray
      instant: 2.25
      marker: '1'
    - entry: event
      label: '2'
      timeline: Row 19
      color: coral
      instant: 0.25
      marker: '2'
    - entry: event
      label: '3'
      timeline: Row 19
      color: dodgerblue
      instant: 1.25
      marker: '3'
    - entry: event
      label: '4'
      timeline: Row 19
      color: orange
      instant: 2.25
      marker: '4'
    - entry: event
      label: '5'
      timeline: Row 20
      color: lime
      instant: 0.25
      marker: '5'
    - entry: event
      label: '6'
      timeline: Row 20
      color: gray
      instant: 1.25
      marker: '6'
    - entry: event
      label: '7'
      timeline: Row 20
      color: coral
      instant: 2.25
      marker: '7'
    - entry: event
      label: '8'
      timeline: Row 21
      color: dodgerblue
      instant: 0.25
      marker: '8'
    - entry: event
      label: '9'
      timeline: Row 21
      color: orange
      instant: 1.25
      marker: '9'
    - entry: event
      label: '!'
      timeline: Row 21
      color: lime
      instant: 2.25
      marker: '!'
    - entry: event
      label: '"'
      timeline: Row 22
      color: gray
      instant: 0.25
      marker: '"'
    - entry: event
      label: '#'
      timeline: Row 22
      color: coral
      instant: 1.25
      marker: '#'
    - entry: event
      label: $
      timeline: Row 22
      color: dodgerblue
      instant: 2.25
      marker: $
    - entry: event
      label: '%'
      timeline: Row 23
      color: orange
      instant: 0.25
      marker: '%'
    - entry: event
      label: '&'
      timeline: Row 23
      color: lime
      instant: 1.25
      marker: '&'
    - entry: event
      label: ''''
      timeline: Row 23
      color: gray
      instant: 2.25
      marker: ''''
    - entry: event
      label: (
      timeline: Row 24
      color: coral
      instant: 0.25
      marker: (
    - entry: event
      label: )
      timeline: Row 24
      color: dodgerblue
      instant: 1.25
      marker: )
    - entry: event
      label: '*'
      timeline: Row 24
      color: orange
      instant: 2.25
      marker: '*'
    - entry: event
      label: +
      timeline: Row 25
      color: lime
      instant: 0.25
      marker: +
    - entry: event
      label: ','
      timeline: Row 25
      color: gray
      instant: 1.25
      marker: ','
    - entry: event
      label: '-'
      timeline: Row 25
      color: coral
      instant: 2.25
      marker: '-'
    - entry: event
      label: .
      timeline: Row 26
      color: dodgerblue
      instant: 0.25
      marker: .
    - entry: event
      label: /
      timeline: Row 26
      color: orange
      instant: 1.25
      marker: /
    - entry: event
      label: ':'
      timeline: Row 26
      color: lime
      instant: 2.25
      marker: ':'
    - entry: event
      label: ;
      timeline: Row 27
      color: gray
      instant: 0.25
      marker: ;
    - entry: event
      label: <
      timeline: Row 27
      color: coral
      instant: 1.25
      marker: <
    - entry: event
      label: '='
      timeline: Row 27
      color: dodgerblue
      instant: 2.25
      marker: '='
    - entry: event
      label: '>'
      timeline: Row 28
      color: orange
      instant: 0.25
      marker: '>'
    - entry: event
      label: '?'
      timeline: Row 28
      color: lime
      instant: 1.25
      marker: '?'
    - entry: event
      label: '@'
      timeline: Row 28
      color: gray
      instant: 2.25
      marker: '@'
    - entry: event
      label: '['
      timeline: Row 29
      color: coral
      instant: 0.25
      marker: '['
    - entry: event
      label: \
      timeline: Row 29
      color: dodgerblue
      instant: 1.25
      marker: \
    - entry: event
      label: ']'
      timeline: Row 29
      color: orange
      instant: 2.25
      marker: ']'
    - entry: event
      label: ^
      timeline: Row 30
      color: lime
      instant: 0.25
      marker: ^
    - entry: event
      label: _
      timeline: Row 30
      color: gray
      instant: 1.25
      marker: _
    - entry: event
      label: '`'
      timeline: Row 30
      color: coral
      instant: 2.25
      marker: '`'
    - entry: event
      label: '{'
      timeline: Row 31
      color: dodgerblue
      instant: 0.25
      marker: '{'
    - entry: event
      label: '|'
      timeline: Row 31
      color: orange
      instant: 1.25
      marker: '|'
    - entry: event
      label: '}'
      timeline: Row 31
      color: lime
      instant: 2.25
      marker: '}'
    - entry: event
      label: '~'
      timeline: Row 32
      color: gray
      instant: 0.25
      marker: '~'
    legend: false
    axis: false
align: top
```
### dimensions

![dimensions SVG](dimensions.svg)

```yaml
chysl:
  version: 0.2.7
  software: Chysl (Python) 0.2.7
chart: column
title: Dimension tick ranges
entries:
- chart: timelines
  title: 1 - 1.00001
  entries:
  - entry: period
    label: Period
    begin: 1
    end: 1.00001
- chart: timelines
  title: 1 - 1.0001
  entries:
  - entry: period
    label: Period
    begin: 1
    end: 1.0001
- chart: timelines
  title: 1 - 1.0002
  entries:
  - entry: period
    label: Period
    begin: 1
    end: 1.0002
- chart: timelines
  title: 1 - 1.1
  entries:
  - entry: period
    label: Period
    begin: 1
    end: 1.1
- chart: timelines
  title: 1 - 2
  entries:
  - entry: period
    label: Period
    begin: 1
    end: 2
- chart: timelines
  title: 1 - 5
  entries:
  - entry: period
    label: Period
    begin: 1
    end: 5
- chart: timelines
  title: 1 - 10
  entries:
  - entry: period
    label: Period
    begin: 1
    end: 10
- chart: timelines
  title: 1 - 2000
  entries:
  - entry: period
    label: Period
    begin: 1
    end: 2000
- chart: timelines
  title: 1 - 10000000
  entries:
  - entry: period
    label: Period
    begin: 1
    end: 10000000
- chart: timelines
  title: 1 - 10000000000
  entries:
  - entry: period
    label: Period
    begin: 1
    end: 10000000000
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

