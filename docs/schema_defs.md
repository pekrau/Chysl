# Schema definitions
- [size](#size): Size of graphical item, in approximate display pixel units.
- [color](#color): Color specification; hex code '#rrggbb' or CSS3 color name.
- [opacity](#opacity): Opacity in range [0.0, 1.0].
- [marker](#marker): Symbol for use as a marker in a chart.
- [text](#text): Text, with or without explicit styling.
- [title](#title): Title of the chart, with or without styling. Displayed at the top.
- [description](#description): Description of the chart. Rendered as <desc> in SVG.
- [fuzzy_number](#fuzzy_number): Number value, exact, or fuzzy with either low/high or error.
- [uri](#uri): A URI, absolute or relative.
- [axis](#axis): Coordinate axis specification.
- [grid](#grid): Coordinate grid specification.
- [chart_or_include](#chart_or_include): Inline chart specification, or location (file of web resource) to read the chart specification from.
- [datapoints](#datapoints): Data provided inline, or from a file, web resource or database.
- [field](#field): Mapping of a plot parameter to a field in source data.

## size

Size of graphical item, in approximate display pixel units.

- *type*: float

## color

Color specification; hex code '#rrggbb' or CSS3 color name.

- *type*: string
- *format*: color

## opacity

Opacity in range [0.0, 1.0].

- *type*: float
- *minimum*: 0
- *maximum*: 1
- *default*: 1

## marker

Symbol for use as a marker in a chart.

- Alternative 1: Predefined symbols denoted by names.
  - *one of*: 'disc', 'circle', 'oval', 'oval-vertical', 'oval-horizontal', 'ellipse', 'ellipse-vertical', 'ellipse-horizontal', 'block', 'square', 'square-cross', 'diamond', 'diamond-cross', 'diamond-fill', 'pyramid', 'triangle', 'wedge', 'trigon', 'pentagon', 'pentagon-fill', 'hexagon', 'hexagon-fill', 'heptagon', 'heptagon-fill', 'octagon', 'octagon-fill', 'cross', 'plus', 'minus', 'bar', 'check', 'burst', 'infinity', 'none', 'star', 'star-fill', 'galaxy', 'sun', 'mercury', 'venus', 'earth', 'moon', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'sigma1', 'sigma2', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega'
- Alternative 2: A single character as marker.
  - *type*: string

## text

Text, with or without explicit styling.

- Alternative 1: Text with default styling.
  - *type*: string
- Alternative 2: Text with styling options.
  - *type*: mapping
  - **text**: The text to display.
    - *required*
    - *type*: string
  - **size**: Size of font. Default depends on context.
    - *See* [size](schema_defs.md#size).
  - **bold**: Bold font.
    - *type*: boolean
    - *default*: false
  - **italic**: Italics font.
    - *type*: boolean
    - *default*: false
  - **color**: Color of text.
    - *type*: string
    - *format*: color
    - *default*: 'black'
  - **placement**: Placement of text. Ignored in some contexts.
    - *one of*: 'left', 'center', 'right'
    - *default*: 'center'
  - **anchor**: Text anchor position. Ignored in some contexts.
    - *one of*: 'start', 'middle', 'end'
    - *default*: 'middle'

## title

Title of the chart, with or without styling. Displayed at the top.

- *See* [text](schema_defs.md#text).

## description

Description of the chart. Rendered as <desc> in SVG.

- *type*: string

## fuzzy_number

Number value, exact, or fuzzy with either low/high or error.

- Alternative 1: Exact number value.
  - *type*: float
- Alternative 2: Fuzzy number value,  with either low/high or error
  - *type*: mapping
  - **value**: Central value for the fuzzy number.
    - *required*
    - *type*: float
  - **low**: Low value for the fuzzy number.
    - *type*: float
  - **high**: High value for the fuzzy number.
    - *type*: float
  - **error**: Symmetrical error around the central value.
    - *type*: float
    - *exclusiveMinimum*: 0

## uri

A URI, absolute or relative.

- *type*: string
- *format*: uri-reference

## axis

Coordinate axis specification.

- Alternative 1: Display default axis, or no display.
  - *type*: boolean
  - *default*: true
- Alternative 2: Coordinate axis specification.
  - *type*: mapping
  - **min**: Explicit minimum of span for axis.
    - *type*: float
  - **max**: Explicit maximum of span for axis.
    - *type*: float
  - **ticks**: Explicit positions for axis ticks.
    - *type*: sequence
    - *items*:
      - *type*: float
  - **labels**: Display labels, or not.
    - *type*: boolean
    - *default*: true
  - **factor**: Factor to divide tick value by for label display. Default depends on context.
    - *type*: float
  - **absolute**: Display absolute values for ticks.
    - *type*: boolean
    - *default*: false
  - **caption**: Axis description.
    - *type*: string
  - **width**: Space for labels and caption. Default is enough for display of specified labels and caption.
    - *type*: float

## grid

Coordinate grid specification.

- Alternative 1: Display default grid.
  - *type*: boolean
  - *default*: true
- Alternative 2: Grid styling.
  - *type*: mapping
  - **color**: Color of grid lines.
    - *type*: string
    - *format*: color
    - *default*: 'lightgray'

## chart_or_include

Inline chart specification, or location (file of web resource) to read the chart specification from.

- Alternative 1: Read the chart specification (YAML) from the URI reference.
  - *type*: mapping
  - **include**:
    - *required*
    - *type*: string
    - *format*: uri-reference
- Alternative 2: Specification of a chart.
  - *type*: mapping
  - **chart**:
    - *required*
    - *one of*: 'timelines', 'piechart', 'scatter2d', 'lines2d', 'note', 'column', 'row', 'overlay', 'board'

## datapoints

Data provided inline, or from a file, web resource or database.

- Alternative 1: Inline data points.
  - *type*: sequence
  - *items*:
    - *type*: mapping
    - **x**:
      - *type*: float
    - **y**:
      - *type*: float
    - **size**:
      - *See* [size](schema_defs.md#size).
    - **color**:
      - *See* [color](schema_defs.md#color).
    - **opacity**:
      - *See* [opacity](schema_defs.md#opacity).
    - **marker**:
      - *See* [marker](schema_defs.md#marker).
- Alternative 2: Data from file, web resource or database.
  - *type*: mapping
  - **source**:
    - *required*
    - Alternative 1: File path or href. File format is deduced from the extension, or 'csv' if not recognized.
      - *type*: string
      - *format*: uri-reference
    - Alternative 2: File path or href, with explicit file format.
      - *type*: mapping
      - **location**: File path or href.
        - *required*
        - *type*: string
        - *format*: uri-reference
      - **format**: File format.
        - *required*
        - *one of*: 'csv', 'tsv', 'json', 'yaml'
    - Alternative 3: Sqlite database.
      - *type*: mapping
      - **database**:
        - *required*
        - *const* 'sqlite'
      - **location**: File path or href.
        - *required*
        - *type*: string
        - *format*: uri-reference
      - **select**: SQL 'select' statement retrieving the data from the database.
        - *required*
        - *type*: string
  - **parameters**: Mapping of plot parameters to the fields in the source data.
    - *type*: mapping
    - **x**:
      - *See* [field](schema_defs.md#field).
    - **y**:
      - *See* [field](schema_defs.md#field).
    - **size**:
      - *See* [field](schema_defs.md#field).
    - **color**:
      - *See* [field](schema_defs.md#field).
    - **opacity**:
      - *See* [field](schema_defs.md#field).
    - **marker**:
      - *See* [field](schema_defs.md#field).

## field

Mapping of a plot parameter to a field in source data.

- Alternative 1: Name of the field in the source data; CSV column header. The values are used directly.
  - *type*: string
- Alternative 2: Number of the field in the source data; CSV column number, starting with 1. The values are used directly.
  - *type*: integer
  - *minimum*: 1
- Alternative 3: Mapping of values in source data to a plot parameter.
  - *type*: mapping
  - **field**: Name of the field in the source data; CSV column header.
    - *required*
    - *type*: string
  - **map**: Map a string value in the source data to a value for the plot parameter.
    - *type*: mapping
