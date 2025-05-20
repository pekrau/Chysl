# note

- [Examples](#examples)
- [Specification](#specification)
  - [declaration](#declaration)
  - [cnotes](#cnotes)
  - [notes](#notes)
  - [cpies](#cpies)
  - [poster](#poster)

## Examples

### declaration

![declaration SVG](declaration.svg)

```yaml
chysl:
  version: 0.1.0
  software: Chysl (Python) 0.1.0
  timestamp: '2025-05-20T07:06:44+00:00'
chart: note
title:
  text: Declaration
  bold: true
body:
  text: 'This software was

    written by me.'
footer:
  text: Copyright 2025 Per Kraulis
  italic: true
```
### cnotes

![cnotes SVG](cnotes.svg)

```yaml
chysl:
  version: 0.1.0
  software: Chysl (Python) 0.1.0
  timestamp: '2025-05-20T07:06:44+00:00'
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
  version: 0.1.0
  software: Chysl (Python) 0.1.0
  timestamp: '2025-05-20T07:06:44+00:00'
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
### cpies

![cpies SVG](cpies.svg)

```yaml
chysl:
  version: 0.1.0
  software: Chysl (Python) 0.1.0
  timestamp: '2025-05-20T07:06:44+00:00'
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
### poster

![poster SVG](poster.svg)

```yaml
chysl:
  version: 0.1.0
  software: Chysl (Python) 0.1.0
  timestamp: '2025-05-20T07:06:44+00:00'
chart: board
title: Poster
entries:
- x: 250
  y: 10
  scale: 1
  component:
    chart: note
    title: By Per Kraulis
    body: Ph.D.
    footer: Stockholm University
- x: 0
  y: 100
  scale: 1
  component:
    include: universe.yaml
- x: 50
  y: 230
  scale: 1
  component:
    include: earth.yaml
```
## Specification

[JSON Schema](note.md)

Textual note with title, body and footer text.

- **chart**:
  - *required*
- **title**: Title of the note.
    - *definition*: See [here](timelines.md#specification)
- **body**: Body of the note.
    - *definition*: See [here](timelines.md#specification)
- **footer**: Footer of the note.
    - *definition*: See [here](timelines.md#specification)
- **width**: Width of chart, in pixels.
  - *type*: float
  - *exclusiveMinimum*: 0
  - *default*: 200
- **frame**: Thickness of the frame.
  - *type*: float
  - *minimum*: 0
  - *default*: 5
- **color**: Color of the note frame and lines.
  - *type*: string
  - *format*: color
  - *default*: 'gold'
- **radius**: Radius of the frame edge curvature.
  - *type*: float
  - *minimum*: 0
  - *default*: 10
- **line**: Thickness of lines between sections.
  - *type*: float
  - *minimum*: 0
  - *default*: 1
- **background**: Background color of the note.
  - *type*: string
  - *format*: color
  - *default*: 'lightyellow'

