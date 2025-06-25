# Schema definitions
- [marker](#marker): Symbol to use as data point marker.
- [text](#text): Text, with or without explicit styling.
- [fuzzy_number](#fuzzy_number): Number value, exact, or fuzzy with either low/high or error.
- [frame](#frame): Specification of the chart area frame.
- [axis](#axis): Coordinate axis specification.
- [grid](#grid): Coordinate grid, with optional styling.
- [chart_or_include](#chart_or_include): Inline chart specification, or location (file of web resource) to read the chart specification from.
- [datasource](#datasource): Data from a file, web resource or database.
- [field](#field): For a chart parameter, give the source data field to use.

## marker

Symbol to use as data point marker.

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
  - **font**: Name of the font.
    - *type*: string
    - *default*: 'sans-serif'
  - **size**: Size of font (pixels). Default depends on context.
    - *type*: float
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

## frame

Specification of the chart area frame.

- Alternative 1: Default chart area frame, or no frame.
  - *type*: boolean
  - *default*: true
- Alternative 2: Specification of the chart area frame.
  - *type*: mapping
  - **thickness**: Thickness of the frame (pixels). Default depends on the chart.
    - *type*: float
  - **color**: Color of the frame. Default depends on the chart.
    - *type*: string
    - *format*: color
  - **radius**: Radius of the frame corner curvature (pixels). Default depends on the chart.
    - *type*: float
    - *minimum*: 0

## axis

Coordinate axis specification.

- Alternative 1: Display default axis, or no display.
  - *type*: boolean
  - *default*: true
- Alternative 2: Coordinate axis specification.
  - *type*: mapping
  - **min**: Explicit minimum for the axis.
    - *type*: float
  - **max**: Explicit maximum for the axis.
    - *type*: float
  - **ticks**: Explicit positions for axis ticks.
    - *type*: sequence
    - *items*:
      - *type*: float
  - **labels**: Display tick labels, or not.
    - *type*: boolean
    - *default*: true
  - **factor**: Factor to divide tick value by for label display. Default depends on context.
    - *type*: float
  - **absolute**: Display absolute values for tick labels.
    - *type*: boolean
    - *default*: false
  - **caption**: Axis description.
    - *type*: string

## grid

Coordinate grid, with optional styling.

- Alternative 1: Display default grid or not.
  - *type*: boolean
  - *default*: true
- Alternative 2: Grid with styling.
  - *type*: mapping
  - **color**: Color of grid lines.
    - *type*: string
    - *format*: color
    - *default*: 'lightgray'

## chart_or_include

Inline chart specification, or location (file of web resource) to read the chart specification from.

- Alternative 1: Specification of a chart.
  - *type*: mapping
  - **chart**:
    - *required*
    - *one of*: 'timelines', 'piechart', 'scatter2d', 'lines2d', 'note', 'column', 'row', 'overlay', 'board'
- Alternative 2: Read the chart specification (YAML) referenced by the URL.
  - *type*: mapping
  - **include**:
    - *required*
    - *type*: string
    - *format*: uri-reference

## datasource

Data from a file, web resource or database.

- Alternative 1: File path or web resource URL, with optional explicit file format and parameter map.
  - *type*: mapping
  - **source**: File path or web resource URL.
    - *required*
    - *type*: string
    - *format*: uri-reference
  - **format**: File format.
    - *one of*: 'csv', 'tsv', 'json', 'yaml'
  - **map**: For a chart parameter, specify the source data field to use.
    - *type*: mapping
- Alternative 2: Sqlite database.
  - *type*: mapping
  - **database**:
    - *required*
    - *const* 'sqlite'
  - **source**: File path or URL for the Sqlite database file.
    - *required*
    - *type*: string
    - *format*: uri-reference
  - **select**: SQL 'select' statement retrieving the data from the database.
    - *required*
    - *type*: string

## field

For a chart parameter, give the source data field to use.

- Alternative 1: Name of the field in the source data; e.g. CSV column header.
  - *type*: string
- Alternative 2: Number of the field in the source data; e.g. CSV column number, starting with 1.
  - *type*: integer
  - *minimum*: 1
- Alternative 3: Mapping of values in a field of source data to values in a chart parameter.
  - *type*: mapping
  - **field**: Name of the field in the source data; e.g. CSV column header.
    - *required*
    - *type*: string
  - **map**: Convert a string value in the source data to a value for the chart parameter.
    - *required*
    - *type*: mapping
