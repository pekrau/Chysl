# column

- [Examples](#examples)
  - [universe_earth](#universe_earth)
  - [pies_column](#pies_column)
  - [notes_column](#notes_column)
  - [notes](#notes)
  - [markers](#markers)
  - [dimensions](#dimensions)
  - [scatter_iris](#scatter_iris)

- [Specification](#specification)

## Examples

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
### pies_column

![pies_column SVG](pies_column.svg)

```yaml
chysl: 0.3.7
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
    href: https://en.wikipedia.org/wiki/Strawberry
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
    href: https://en.wikipedia.org/wiki/Rhubarb
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
chysl: 0.3.7
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
### scatter_iris

[CSV data file](scatter_iris.csv)

![scatter_iris SVG](scatter_iris.svg)

```yaml
chysl: 0.3.7
chart: column
title:
  text: Iris flower measurements
  size: 30
subcharts:
- chart: row
  subcharts:
  - chart: scatter2d
    width: 300
    xaxis:
      min: 4
      max: 8
      labels: false
    yaxis:
      min: 4
      max: 8
      labels: true
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: sepal length
        y: sepal length
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  - chart: scatter2d
    width: 300
    xaxis:
      min: 2
      max: 4.5
      labels: false
    yaxis:
      min: 4
      max: 8
      labels: false
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: sepal width
        y: sepal length
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  - chart: scatter2d
    width: 300
    xaxis:
      min: 0.5
      max: 7.5
      labels: false
    yaxis:
      min: 4
      max: 8
      labels: false
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: petal length
        y: sepal length
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  - chart: scatter2d
    width: 300
    xaxis:
      min: 0
      max: 3
      labels: false
    yaxis:
      min: 4
      max: 8
      labels: false
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: petal width
        y: sepal length
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  padding: 4
- chart: row
  subcharts:
  - chart: scatter2d
    width: 300
    xaxis:
      min: 4
      max: 8
      labels: false
    yaxis:
      min: 2
      max: 4.5
      labels: true
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: sepal length
        y: sepal width
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  - chart: scatter2d
    width: 300
    xaxis:
      min: 2
      max: 4.5
      labels: false
    yaxis:
      min: 2
      max: 4.5
      labels: false
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: sepal width
        y: sepal width
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  - chart: scatter2d
    width: 300
    xaxis:
      min: 0.5
      max: 7.5
      labels: false
    yaxis:
      min: 2
      max: 4.5
      labels: false
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: petal length
        y: sepal width
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  - chart: scatter2d
    width: 300
    xaxis:
      min: 0
      max: 3
      labels: false
    yaxis:
      min: 2
      max: 4.5
      labels: false
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: petal width
        y: sepal width
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  padding: 4
- chart: row
  subcharts:
  - chart: scatter2d
    width: 300
    xaxis:
      min: 4
      max: 8
      labels: false
    yaxis:
      min: 0.5
      max: 7.5
      labels: true
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: sepal length
        y: petal length
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  - chart: scatter2d
    width: 300
    xaxis:
      min: 2
      max: 4.5
      labels: false
    yaxis:
      min: 0.5
      max: 7.5
      labels: false
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: sepal width
        y: petal length
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  - chart: scatter2d
    width: 300
    xaxis:
      min: 0.5
      max: 7.5
      labels: false
    yaxis:
      min: 0.5
      max: 7.5
      labels: false
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: petal length
        y: petal length
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  - chart: scatter2d
    width: 300
    xaxis:
      min: 0
      max: 3
      labels: false
    yaxis:
      min: 0.5
      max: 7.5
      labels: false
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: petal width
        y: petal length
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  padding: 4
- chart: row
  subcharts:
  - chart: scatter2d
    width: 300
    xaxis:
      min: 4
      max: 8
      caption: Sepal length
      labels: true
    yaxis:
      min: 0
      max: 3
      labels: true
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: sepal length
        y: petal width
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  - chart: scatter2d
    width: 300
    xaxis:
      min: 2
      max: 4.5
      caption: Sepal width
      labels: true
    yaxis:
      min: 0
      max: 3
      labels: false
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: sepal width
        y: petal width
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  - chart: scatter2d
    width: 300
    xaxis:
      min: 0.5
      max: 7.5
      caption: Petal length
      labels: true
    yaxis:
      min: 0
      max: 3
      labels: false
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: petal length
        y: petal width
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  - chart: scatter2d
    width: 300
    xaxis:
      min: 0
      max: 3
      caption: Petal width
      labels: true
    yaxis:
      min: 0
      max: 3
      labels: false
      width: 24
    size: 6
    points:
      source: scatter_iris.csv
      parameters:
        x: petal width
        y: petal width
        color:
          field: class
          map:
            Iris-setosa: red
            Iris-versicolor: green
            Iris-virginica: blue
        marker:
          field: class
          map:
            Iris-setosa: circle
            Iris-versicolor: triangle
            Iris-virginica: square
  padding: 4
- chart: column
  subcharts:
  - chart: note
    body:
      text: 'Iris setosa: red circles'
      size: 24
      color: red
    frame: 0
    background: white
  - chart: note
    body:
      text: 'Iris versicolor: green triangles'
      size: 24
      color: green
    frame: 0
    background: white
  - chart: note
    body:
      text: 'Iris virginica: blue squares'
      size: 24
      color: blue
    frame: 0
    background: white
  padding: 0
padding: 4
```
## Specification

[JSON Schema](column.md)

Charts stacked in a column.

- **chart**:
  - *required*
  - *const* 'column'
- **title**:
  - *See* [title](schema_defs.md#title).
- **description**:
  - *See* [description](schema_defs.md#description).
- **align**: Align charts horizontally within the column.
  - *one of*: 'left', 'center', 'right'
  - *default*: 'center'
- **padding**: Padding between the subcharts.
  - *type*: float
  - *minimum*: 0
  - *default*: 2
- **subcharts**: Charts in the column.
  - *required*
  - *type*: sequence
  - *items*:
    - *See* [chart_or_include](schema_defs.md#chart_or_include).

