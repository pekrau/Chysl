# Schema definitions

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
    - *type*: float
    - *exclusiveMinimum*: 0
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

## marker

Symbol for use as a marker in a chart.

- Alternative 1: Predefined symbols.
  - *one of*: 'disc', 'circle', 'oval', 'oval-vertical', 'oval-horizontal', 'ellipse', 'ellipse-vertical', 'ellipse-horizontal', 'block', 'square', 'diamond', 'diamond-fill', 'pyramid', 'triangle', 'wedge', 'trigon', 'pentagon', 'pentagon-fill', 'hexagon', 'hexagon-fill', 'heptagon', 'heptagon-fill', 'octagon', 'octagon-fill', 'bar', 'bar-vertical', 'bar-horizontal', 'cross', 'plus', 'check', 'burst', 'infinity', 'none', 'star', 'star-fill', 'galaxy', 'sun', 'mercury', 'venus', 'earth', 'moon', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'sigma1', 'sigma2', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega'
  - *default*: 'disc'
- Alternative 2: Single characters.
  - *type*: string

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
    - *one of*: 'timelines', 'piechart', 'note', 'plot', 'column', 'row', 'board'

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
      - *type*: float
    - **color**:
      - *type*: string
      - *format*: color
    - **opacity**:
      - *type*: float
      - *minimum*: 0
      - *maximum*: 1
    - **marker**:
      - *See* [marker](schema_defs.md#marker).
- Alternative 2: Data from file or web source.
  - *type*: mapping
  - **source**:
    - *required*
    - *type*: string
    - *format*: uri-reference
  - **format**: Format of data file. Inferred from file extension, if not provided.
    - *one of*: 'csv', 'tsv', 'json', 'yaml'
    - *default*: 'csv'
