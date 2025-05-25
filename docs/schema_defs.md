# Schema definitions

## size

Size of graphical item, in approximate pixel units.

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

## marker

Symbol for use as a marker in a chart.

- Alternative 1: Predefined symbols denoted by names.
  - *one of*: 'disc', 'circle', 'oval', 'oval-vertical', 'oval-horizontal', 'ellipse', 'ellipse-vertical', 'ellipse-horizontal', 'block', 'square', 'square-cross', 'diamond', 'diamond-cross', 'diamond-fill', 'pyramid', 'triangle', 'wedge', 'trigon', 'pentagon', 'pentagon-fill', 'hexagon', 'hexagon-fill', 'heptagon', 'heptagon-fill', 'octagon', 'octagon-fill', 'cross', 'plus', 'minus', 'bar', 'check', 'burst', 'infinity', 'none', 'star', 'star-fill', 'galaxy', 'sun', 'mercury', 'venus', 'earth', 'moon', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'sigma1', 'sigma2', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega'
  - *default*: 'disc'
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

## axis

Coordinate axis specification.

- Alternative 1: Display default axis.
  - *type*: boolean
  - *default*: true
- Alternative 2: Axis details.
  - *type*: mapping
  - **color**: Color of grid lines.
    - *type*: string
    - *format*: color
    - *default*: 'gray'
  - **absolute**: Display absolute values for ticks.
    - *type*: boolean
    - *default*: false
  - **caption**: Axis description.
    - *type*: string

## chart_or_include

In-line chart specification, or location (file of web resource) to read the chart specification from.

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
    - *one of*: 'timelines', 'piechart', 'note', 'plot2d', 'column', 'row', 'board'

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

## data_or_source

Data provided in-line, or from a file or web source.

- Alternative 1: In-line data points.
  - *type*: sequence
  - *items*:
    - *type*: mapping
    - **x**:
      - *See* [fuzzy_number](schema_defs.md#fuzzy_number).
      - *required*
    - **y**:
      - *See* [fuzzy_number](schema_defs.md#fuzzy_number).
      - *required*
    - **size**:
      - *See* [size](schema_defs.md#size).
    - **color**:
      - *See* [color](schema_defs.md#color).
    - **opacity**:
      - *See* [opacity](schema_defs.md#opacity).
    - **marker**:
      - *See* [marker](schema_defs.md#marker).
- Alternative 2: Data from file or web source.
  - *type*: mapping
  - **source**: File path or href for the source.
    - *required*
    - *type*: string
    - *format*: uri-reference
  - **format**: Format of data file. Inferred from file extension, if not provided.
    - *one of*: 'csv', 'tsv', 'json', 'yaml'
    - *default*: 'csv'
  - **parameters**: Mapping of plot parameters to the fields in the source data.
