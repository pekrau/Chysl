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
  - **caption**: Axis description.
    - *type*: string

## chart_or_include

Chart specification, or 'include' of a file or web resource.

- Alternative 1: Include another YAML file from the URI reference.
  - *type*: mapping
  - **include**:
    - *required*
    - *type*: string
    - *format*: uri-reference
- Alternative 2: Specification of any chart.
  - *type*: mapping
  - **chart**:
    - *required*
    - *one of*: 'timelines', 'piechart', 'note', 'column', 'row', 'board'
