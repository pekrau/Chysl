# note

- [Examples](#examples)
  - [declaration](#declaration)
  - [notes_column](#notes_column)
  - [notes](#notes)
  - [pies_column](#pies_column)
  - [poster](#poster)

- [Specification](#specification)

## Examples

### declaration

![declaration SVG](declaration.svg)

```yaml
chysl: 0.4.0
chart: note
title:
  bold: true
  placement: left
  text: Declaration
body:
  placement: right
  text: 'This software was

    written by me.'
footer:
  italic: true
  text: Copyright 2025 Per Kraulis
width: 200
```
### notes_column

![notes_column SVG](notes_column.svg)

```yaml
chysl: 0.4.0
chart: column
title: Notes in a column
subcharts:
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
  width: 200
- chart: note
  footer: Footer
  width: 200
- chart: note
  title: Header
  body: Body (no lines)
  footer: Footer
  line: 0
  width: 200
- include: declaration.yaml
padding: 4
```
### notes

![notes SVG](notes.svg)

```yaml
chysl: 0.4.0
chart: board
items:
- x: 0
  y: 0
  subchart:
    chart: column
    title: Notes in a column
    subcharts:
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
      width: 200
    - chart: note
      footer: Footer
      width: 200
    - chart: note
      title: Header
      body: Body (no lines)
      footer: Footer
      line: 0
      width: 200
    - include: declaration.yaml
    padding: 4
  scale: 1.5
```
### pies_column

![pies_column SVG](pies_column.svg)

```yaml
chysl: 0.4.0
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
```
### poster

![poster SVG](poster.svg)

```yaml
chysl: 0.4.0
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
- x: 0
  y: 150
  subchart:
    include: universe.yaml
- x: 50
  y: 290
  subchart:
    include: earth.yaml
```
## Specification

[JSON Schema](note.md)

Textual note with title, body and footer text.

- **chart**:
  - *required*
  - *const* 'note'
- **title**: Title of the note.
  - *See* [text](schema_defs.md#text).
- **body**: Body of the note.
  - *See* [text](schema_defs.md#text).
- **footer**: Footer of the note.
  - *See* [text](schema_defs.md#text).
- **description**: Description of the chart. Rendered as <desc> in SVG.
  - *type*: string
- **frame**: Specification of the note frame. Default is 5 pixels gold with radius 10.
  - *See* [frame](schema_defs.md#frame).
- **line**: Thickness of lines between sections (pixels). Same color as frame.
  - *type*: float
  - *minimum*: 0
  - *default*: 1
- **background**: Background color of the note.
  - *type*: string
  - *format*: color
  - *default*: 'lightyellow'
- **width**: Explicit width of note (pixels).
  - *type*: float

