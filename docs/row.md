# row

- [Examples](#examples)
  - [pies_row](#pies_row)
  - [scatter_iris](#scatter_iris)

- [Specification](#specification)

## Examples

### pies_row

![pies_row SVG](pies_row.svg)

```yaml
chysl:
  version: 0.2.11
  software: Chysl (Python) 0.2.11
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
### scatter_iris

[CSV data file](scatter_iris.csv)

![scatter_iris SVG](scatter_iris.svg)

```yaml
chysl:
  version: 0.2.11
  software: Chysl (Python) 0.2.11
chart: column
title:
  text: Iris flower measurements
  size: 30
entries:
- chart: row
  entries:
  - chart: note
    body:
      text: Sepal length
      size: 24
    frame: 0
    background: white
  - chart: plot2d
    entries:
    - entry: scatter2d
      data:
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
    width: 300
  - chart: plot2d
    entries:
    - entry: scatter2d
      data:
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
    width: 300
  - chart: plot2d
    entries:
    - entry: scatter2d
      data:
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
    width: 300
- chart: row
  entries:
  - chart: plot2d
    entries:
    - entry: scatter2d
      data:
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
    width: 300
  - chart: note
    body:
      text: Sepal width
      size: 24
    frame: 0
    background: white
  - chart: plot2d
    entries:
    - entry: scatter2d
      data:
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
    width: 300
  - chart: plot2d
    entries:
    - entry: scatter2d
      data:
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
    width: 300
- chart: row
  entries:
  - chart: plot2d
    entries:
    - entry: scatter2d
      data:
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
    width: 300
  - chart: plot2d
    entries:
    - entry: scatter2d
      data:
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
    width: 300
  - chart: note
    body:
      text: Petal length
      size: 24
    frame: 0
    background: white
  - chart: plot2d
    entries:
    - entry: scatter2d
      data:
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
    width: 300
- chart: row
  entries:
  - chart: plot2d
    entries:
    - entry: scatter2d
      data:
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
    width: 300
  - chart: plot2d
    entries:
    - entry: scatter2d
      data:
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
    width: 300
  - chart: plot2d
    entries:
    - entry: scatter2d
      data:
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
    width: 300
  - chart: note
    body:
      text: Petal width
      size: 24
    frame: 0
    background: white
- chart: column
  entries:
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
```
## Specification

[JSON Schema](row.md)

Charts arranged in a row.

- **chart**:
  - *required*
  - *const* 'row'
- **title**: Title of the column chart.
  - *See* [text](schema_defs.md#text).
- **align**: Align charts vertically within the row.
  - *one of*: 'bottom', 'middle', 'top'
  - *default*: 'middle'
- **entries**: Component charts in the row.
  - *required*
  - *type*: sequence
  - *items*:
    - *See* [chart_or_include](schema_defs.md#chart_or_include).

