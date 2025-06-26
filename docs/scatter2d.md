# scatter2d

- [Examples](#examples)
  - [scatter_points](#scatter_points)
  - [scatter_iris](#scatter_iris)
  - [markers](#markers)
  - [points_marks](#points_marks)

- [Specification](#specification)

## Examples

### scatter_points

![scatter_points SVG](scatter_points.svg)

```yaml
chysl: 0.5.1
chart: scatter2d
title: Scattered points inline
xaxis:
  caption: X dimension
yaxis:
  caption: Y dimension
points:
- x: 41.66198725453412
  y: 1.016916945706836
  marker: disc
  size: 89.51239055522458
  color: blue
  opacity: 0.4493199275997964
- x: 36.84116894884757
  y: 19.366134904507426
  marker: alpha
  size: 73.96049012373167
  color: red
  opacity: 0.3808439119646841
- x: 12.426688428353017
  y: 43.29362680099159
  marker: mars
  size: 73.72470928455058
  color: green
  opacity: 0.3871717803618659
- x: 55.32210855693298
  y: 35.490138633659875
  marker: disc
  size: 97.48388710597291
  color: purple
  opacity: 0.34564704943836755
- x: 97.863999557041
  y: 41.2119392939301
  marker: alpha
  size: 70.23612208660225
  color: cyan
  opacity: 0.3740730844650946
- x: 71.8967140300885
  y: 18.997137872182034
  marker: mars
  size: 60.49362554641313
  color: orange
  opacity: 0.31176060907110026
- x: 33.95177723979207
  y: 96.74824588798714
  marker: disc
  size: 98.72790725113941
  color: lime
  opacity: 0.6722650200705174
- x: 0.3454610755095566
  y: 94.02385030977428
  marker: alpha
  size: 92.24601812532859
  color: black
  opacity: 0.6854171692584055
- x: 17.88737646235151
  y: 9.94996328096114
  marker: mars
  size: 64.87194811071146
  color: blue
  opacity: 0.7427682335727397
- x: 57.80860273663232
  y: 73.65822149440822
  marker: disc
  size: 53.95726619370446
  color: red
  opacity: 0.5617987900823291
- x: 70.93864374841317
  y: 82.48339468977807
  marker: alpha
  size: 88.42747198354498
  color: green
  opacity: 0.41615405648873105
- x: 87.31899671198792
  y: 21.63804302900447
  marker: mars
  size: 88.11395425619887
  color: purple
  opacity: 0.5775426494691887
- x: 18.582835985521594
  y: 58.8608618331516
  marker: disc
  size: 71.09436314524501
  color: cyan
  opacity: 0.7793312517176161
- x: 4.153922185136183
  y: 16.413828210031
  marker: alpha
  size: 98.99755918885067
  color: orange
  opacity: 0.7161024429252615
- x: 15.027246598161915
  y: 22.911297045444933
  marker: mars
  size: 72.34829649715135
  color: lime
  opacity: 0.3784904151633868
- x: 32.37607256534856
  y: 4.931922302313108
  marker: disc
  size: 82.70063762893398
  color: black
  opacity: 0.3392813734266923
- x: 99.46042507818163
  y: 92.05698384306194
  marker: alpha
  size: 87.32973233388773
  color: blue
  opacity: 0.686202945233638
- x: 36.77523003172184
  y: 67.87061729470147
  marker: mars
  size: 85.67552601762335
  color: red
  opacity: 0.5403881274977664
- x: 6.1525046928359135
  y: 62.61039487405924
  marker: disc
  size: 59.54564993321353
  color: green
  opacity: 0.6050445354210666
- x: 42.082846107038975
  y: 95.25307830408943
  marker: alpha
  size: 52.095676972398344
  color: purple
  opacity: 0.6844281832234802
- x: 69.85618555499734
  y: 55.65629985158106
  marker: mars
  size: 44.80277664731132
  color: cyan
  opacity: 0.3824758555460905
- x: 96.72819773521698
  y: 23.064252885618973
  marker: disc
  size: 49.812581909934636
  color: orange
  opacity: 0.44414783623123366
- x: 53.71205291941445
  y: 51.961333822995634
  marker: alpha
  size: 40.199908679667814
  color: lime
  opacity: 0.3015924820962709
- x: 49.60664874757757
  y: 18.48544913177429
  marker: mars
  size: 76.45005014560031
  color: black
  opacity: 0.6992315152682786
- x: 9.587326842754095
  y: 50.51671769471715
  marker: disc
  size: 64.36828735446176
  color: blue
  opacity: 0.6952266415635342
```
### scatter_iris

[CSV data file](scatter_iris.csv)

![scatter_iris SVG](scatter_iris.svg)

```yaml
chysl: 0.5.1
chart: column
title:
  size: 30
  text: Iris flower measurements
subcharts:
- chart: row
  subcharts:
  - chart: column
    subcharts:
    - chart: scatter2d
      width: 300
      height: 300
      xaxis:
        labels: false
      yaxis:
        caption: Sepal length
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
      height: 300
      xaxis:
        labels: false
      yaxis:
        caption: Sepal width
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
      height: 300
      xaxis:
        labels: false
      yaxis:
        caption: Petal length
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
      height: 300
      xaxis:
        caption: Sepal length
      yaxis:
        caption: Petal width
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
    align: right
    padding: 4
  - chart: column
    subcharts:
    - chart: scatter2d
      width: 300
      height: 300
      xaxis:
        labels: false
      yaxis:
        labels: false
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
      height: 300
      xaxis:
        labels: false
      yaxis:
        labels: false
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
      height: 300
      xaxis:
        labels: false
      yaxis:
        labels: false
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
      height: 300
      xaxis:
        caption: Sepal width
      yaxis:
        labels: false
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
    align: right
    padding: 4
  - chart: column
    subcharts:
    - chart: scatter2d
      width: 300
      height: 300
      xaxis:
        labels: false
      yaxis:
        labels: false
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
      height: 300
      xaxis:
        labels: false
      yaxis:
        labels: false
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
      height: 300
      xaxis:
        labels: false
      yaxis:
        labels: false
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
      height: 300
      xaxis:
        caption: Petal length
      yaxis:
        labels: false
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
    align: right
    padding: 4
  - chart: column
    subcharts:
    - chart: scatter2d
      width: 300
      height: 300
      xaxis:
        labels: false
      yaxis:
        labels: false
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
    - chart: scatter2d
      width: 300
      height: 300
      xaxis:
        labels: false
      yaxis:
        labels: false
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
    - chart: scatter2d
      width: 300
      height: 300
      xaxis:
        labels: false
      yaxis:
        labels: false
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
    - chart: scatter2d
      width: 300
      height: 300
      xaxis:
        caption: Petal width
      yaxis:
        labels: false
      size: 6
      points:
        source: scatter_iris.csv
        map:
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
    align: right
    padding: 4
  padding: 4
- chart: column
  subcharts:
  - chart: note
    body:
      size: 24
      color: red
      text: 'Iris setosa: red circles'
    frame: false
    background: white
  - chart: note
    body:
      size: 24
      color: green
      text: 'Iris versicolor: green triangles'
    frame: false
    background: white
  - chart: note
    body:
      size: 24
      color: blue
      text: 'Iris virginica: blue squares'
    frame: false
    background: white
padding: 4
```
### markers

![markers SVG](markers.svg)

```yaml
chysl: 0.5.1
chart: column
subcharts:
- chart: scatter2d
  title: Geometry markers
  width: 400
  height: 225
  xaxis:
    max: 3.0
    labels: false
  yaxis: false
  xgrid: false
  ygrid: false
  points:
  - x: 0.2
    y: 1
    marker: disc
    color: gray
    label: disc
  - x: 1.2
    y: 1
    marker: circle
    color: coral
    label: circle
  - x: 2.2
    y: 1
    marker: oval
    color: dodgerblue
    label: oval
  - x: 0.2
    y: 2
    marker: oval-vertical
    color: orange
    label: oval-vertical
  - x: 1.2
    y: 2
    marker: oval-horizontal
    color: lime
    label: oval-horizontal
  - x: 2.2
    y: 2
    marker: ellipse
    color: gray
    label: ellipse
  - x: 0.2
    y: 3
    marker: ellipse-vertical
    color: coral
    label: ellipse-vertical
  - x: 1.2
    y: 3
    marker: ellipse-horizontal
    color: dodgerblue
    label: ellipse-horizontal
  - x: 2.2
    y: 3
    marker: block
    color: orange
    label: block
  - x: 0.2
    y: 4
    marker: square
    color: lime
    label: square
  - x: 1.2
    y: 4
    marker: square-cross
    color: gray
    label: square-cross
  - x: 2.2
    y: 4
    marker: diamond
    color: coral
    label: diamond
  - x: 0.2
    y: 5
    marker: diamond-cross
    color: dodgerblue
    label: diamond-cross
  - x: 1.2
    y: 5
    marker: diamond-fill
    color: orange
    label: diamond-fill
  - x: 2.2
    y: 5
    marker: pyramid
    color: lime
    label: pyramid
  - x: 0.2
    y: 6
    marker: triangle
    color: gray
    label: triangle
  - x: 1.2
    y: 6
    marker: wedge
    color: coral
    label: wedge
  - x: 2.2
    y: 6
    marker: trigon
    color: dodgerblue
    label: trigon
  - x: 0.2
    y: 7
    marker: pentagon
    color: orange
    label: pentagon
  - x: 1.2
    y: 7
    marker: pentagon-fill
    color: lime
    label: pentagon-fill
  - x: 2.2
    y: 7
    marker: hexagon
    color: gray
    label: hexagon
  - x: 0.2
    y: 8
    marker: hexagon-fill
    color: coral
    label: hexagon-fill
  - x: 1.2
    y: 8
    marker: heptagon
    color: dodgerblue
    label: heptagon
  - x: 2.2
    y: 8
    marker: heptagon-fill
    color: orange
    label: heptagon-fill
  - x: 0.2
    y: 9
    marker: octagon
    color: lime
    label: octagon
  - x: 1.2
    y: 9
    marker: octagon-fill
    color: gray
    label: octagon-fill
- chart: scatter2d
  title: Symbol markers
  width: 400
  height: 75
  xaxis:
    max: 3.0
    labels: false
  yaxis: false
  xgrid: false
  ygrid: false
  points:
  - x: 0.2
    y: 1
    marker: cross
    color: coral
    label: cross
  - x: 1.2
    y: 1
    marker: plus
    color: dodgerblue
    label: plus
  - x: 2.2
    y: 1
    marker: minus
    color: orange
    label: minus
  - x: 0.2
    y: 2
    marker: bar
    color: lime
    label: bar
  - x: 1.2
    y: 2
    marker: check
    color: gray
    label: check
  - x: 2.2
    y: 2
    marker: burst
    color: coral
    label: burst
  - x: 0.2
    y: 3
    marker: infinity
    color: dodgerblue
    label: infinity
  - x: 1.2
    y: 3
    marker: none
    color: orange
    label: none
- chart: scatter2d
  title: Astronomy markers
  width: 400
  height: 125
  xaxis:
    max: 3.0
    labels: false
  yaxis: false
  xgrid: false
  ygrid: false
  points:
  - x: 0.2
    y: 1
    marker: star
    color: lime
    label: star
  - x: 1.2
    y: 1
    marker: star-fill
    color: gray
    label: star-fill
  - x: 2.2
    y: 1
    marker: galaxy
    color: coral
    label: galaxy
  - x: 0.2
    y: 2
    marker: sun
    color: dodgerblue
    label: sun
  - x: 1.2
    y: 2
    marker: mercury
    color: orange
    label: mercury
  - x: 2.2
    y: 2
    marker: venus
    color: lime
    label: venus
  - x: 0.2
    y: 3
    marker: earth
    color: gray
    label: earth
  - x: 1.2
    y: 3
    marker: moon
    color: coral
    label: moon
  - x: 2.2
    y: 3
    marker: mars
    color: dodgerblue
    label: mars
  - x: 0.2
    y: 4
    marker: jupiter
    color: orange
    label: jupiter
  - x: 1.2
    y: 4
    marker: saturn
    color: lime
    label: saturn
  - x: 2.2
    y: 4
    marker: uranus
    color: gray
    label: uranus
  - x: 0.2
    y: 5
    marker: neptune
    color: coral
    label: neptune
- chart: scatter2d
  title: Greek markers
  width: 400
  height: 225
  xaxis:
    max: 3.0
    labels: false
  yaxis: false
  xgrid: false
  ygrid: false
  points:
  - x: 0.2
    y: 1
    marker: alpha
    color: dodgerblue
    label: alpha
  - x: 1.2
    y: 1
    marker: beta
    color: orange
    label: beta
  - x: 2.2
    y: 1
    marker: gamma
    color: lime
    label: gamma
  - x: 0.2
    y: 2
    marker: delta
    color: gray
    label: delta
  - x: 1.2
    y: 2
    marker: epsilon
    color: coral
    label: epsilon
  - x: 2.2
    y: 2
    marker: zeta
    color: dodgerblue
    label: zeta
  - x: 0.2
    y: 3
    marker: eta
    color: orange
    label: eta
  - x: 1.2
    y: 3
    marker: theta
    color: lime
    label: theta
  - x: 2.2
    y: 3
    marker: iota
    color: gray
    label: iota
  - x: 0.2
    y: 4
    marker: kappa
    color: coral
    label: kappa
  - x: 1.2
    y: 4
    marker: lambda
    color: dodgerblue
    label: lambda
  - x: 2.2
    y: 4
    marker: mu
    color: orange
    label: mu
  - x: 0.2
    y: 5
    marker: nu
    color: lime
    label: nu
  - x: 1.2
    y: 5
    marker: xi
    color: gray
    label: xi
  - x: 2.2
    y: 5
    marker: omicron
    color: coral
    label: omicron
  - x: 0.2
    y: 6
    marker: pi
    color: dodgerblue
    label: pi
  - x: 1.2
    y: 6
    marker: rho
    color: orange
    label: rho
  - x: 2.2
    y: 6
    marker: sigma
    color: lime
    label: sigma
  - x: 0.2
    y: 7
    marker: sigma1
    color: gray
    label: sigma1
  - x: 1.2
    y: 7
    marker: sigma2
    color: coral
    label: sigma2
  - x: 2.2
    y: 7
    marker: tau
    color: dodgerblue
    label: tau
  - x: 0.2
    y: 8
    marker: upsilon
    color: orange
    label: upsilon
  - x: 1.2
    y: 8
    marker: phi
    color: lime
    label: phi
  - x: 2.2
    y: 8
    marker: chi
    color: gray
    label: chi
  - x: 0.2
    y: 9
    marker: psi
    color: coral
    label: psi
  - x: 1.2
    y: 9
    marker: omega
    color: dodgerblue
    label: omega
padding: 10
```
### points_marks

![points_marks SVG](points_marks.svg)

```yaml
chysl: 0.5.1
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
      marker: beta
      color: white
    - x: 3
      y: 3
      marker: gamma
```
## Specification

[JSON Schema](scatter2d.md)

2D scatter chart.

- **chart**:
  - *required*
  - *const* 'scatter2d'
- **title**: Title of the chart.
  - *See* [text](schema_defs.md#text).
- **description**: Description of the chart. Rendered as <desc> in SVG.
  - *type*: string
- **points**:
  - *required*
  - Alternative 1: Inline list of 2D points.
    - *type*: sequence
    - *items*:
      - *type*: mapping
      - **x**:
        - *type*: float
      - **y**:
        - *type*: float
      - **marker**:
        - *See* [marker](schema_defs.md#marker).
      - **size**: Size of the marker (pixels).
        - *type*: float
      - **color**: Color specified by hex code '#rrggbb' or CSS3 color name.
        - *type*: string
        - *format*: color
      - **opacity**: Opacity of the marker.
        - *type*: float
        - *minimum*: 0
        - *maximum*: 1
        - *default*: 1
      - **label**: Description of the point.
        - *type*: string
      - **href**: A link URL, absolute or relative.
        - *type*: string
        - *format*: uri-reference
  - Alternative 2: External source of 2D points data.
    - *See* [datasource](schema_defs.md#datasource).
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
- **marker**: Default marker.
  - *See* [marker](schema_defs.md#marker).
  - *default*: 'disc'
- **size**: Default size of the markers (pixels).
  - *type*: float
  - *default*: 10
- **color**: Default marker color.
  - *type*: string
  - *format*: color
  - *default*: 'black'
- **opacity**: Default marker opacity.
  - *type*: float
  - *minimum*: 0
  - *maximum*: 1
  - *default*: 1

