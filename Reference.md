# The Reference Manual of Funix

This reference manual covers advanced features of Funix. If you are new to Funix, please read the [QuickStart Guide](QuickStart.md) first.

## Command line options

### The lazy (easy) mode

Lazy/easy mode is for when you have no  customization to individual functions. Suppose you have a Python function defined in a file `hello.py`. Then you can convert it to a web app via Funix using the command

```bash
funix -l hello.py # -l stands for lazy
```

The web app runs at `http://localhost:3000` in a browser window automatically popped. The arguments of the function are mapped to the input widgets of the web app. The return values of the function are displayed in the output widget.

### The normal mode

If you used a Funix decorator to customize a Python function, e.g.,

```py
import funix

@funix.funix(
  argument_labels={
    "x": "The number to be squared"
  }
)
def square(x: int) -> int:
    return x * x
```

then you have to use the normal mode to apply the customization. The Shell command is as simply as:

```bash
funix my_app.py
```

### The recursive mode

Funix can convert all `.py` files recursively from a local path to apps, e.g.,

```sh
funix ./demos # ./demos is a folder, funix will handle all .py files under it
```

### The Git mode

To make life more convenient, Funix can directly convert functions in a Git repo to web apps, e.g.,

```sh
funix -g http://github.com/funix/funix \    # the repo
      -r examples \                         # the folder under the repo
      ./                                    # recursively

funix -g http://github.com/funix/funix \    # the repo
      -r examples \                         # the folder under the repo
      demo.py                               # a particular file
```

### The debug mode

Starting Funix with the flag `-d` will enable the debug mode which monitors source code changes and automatically re-generate the app. Known bugs: the watchdog we used monitors all `.py` files in the current folder, which will keep your CPU high.

### The default mode

When you have multiple functions, but you want to specify which one to be the default one, so that it will be displayed when the app is loaded, you can use the flag `-D` to specify the default function, for example:

```bash
# Only for 1 file:
funix -D my_default_function my_app.py

# For multiple files:
funix -D "hello.py:hello_world" -R examples
```

But you can also use the `funix.funix` decorator to specify the default function, for example:

```python
from funix import funix


@funix(
  default=True
)
def my_default_function():
  pass
```

## Supported I/O types and widget customization

The Zen of Funix is to choose widgets for function I/Os based on their types. This can be done via themes (which is cross-app/function) or per-variable.
Only the data types supported by Funix can be properly rendered into widgets.
Funix supports certain Python's built-in data types and those from common scientific libraries, such as `Figure` of `matplotlib`.

> Funix does NOT recommend customizing the widgets per-variable. This is a major difference between Funix and other Python-based app building frameworks. Funix believes this should be done via themes, to consistently create UIs across apps. Read the [themes](#themes) section for more details. If you really want to manually pick UI components for a variable, please see [Customizing the input widgets per-variable](#customizing-the-input-widgets-per-variable).

### Input types and their widgets

Here we list the supported input data types, and the widget names (`str`) that a theme or a per-variable customization directive can use to map the type/variable to a specific UI widget.

#### Python built-in basic types

* `int` and `float`
  * allowed widget names:
    * `input` (default): a text input box where only digits and up to one dot are allowed. The UI component is [MUI's TextField type=number](https://mui.com/material-ui/react-text-field/#type-quot-number-quot).
    * `slider`: a slider. You can optionally set the arguments `start`, `end`, and `step` using a function call syntax `slider[start, end, step]` or `["slider", {"min":min, "max":max, "step":step}]` -- in the latter case, not all three parameters need to be customized. For integers, the default values are `start=0`, `end=100`, and `step=1`. For floats, the default values are `start=0`, `end=1`, and `step=0.1`. The UI component is [MUI's Slider](https://mui.com/components/slider/).
* `str`
  * allowed widget names:
    * `textarea` (default): Multiline text input with line breaks. The UI component is [MUI's TextField with multiline support](https://mui.com/material-ui/react-text-field/#multiline).
    * `input`: a text input box. Only oneline. The UI component is [MUI's TextField](https://mui.com/material-ui/react-text-field).
    * `password`: a text input box with password mask. The UI component is [MUI's TextField](https://mui.com/material-ui/react-text-field).
* `bool`
  * allowed widget names:
    * `checkbox` (default): a checkbox. The UI component is [MUI's Checkbox](https://mui.com/components/checkboxes/).
    * `switch`: a switch. The UI component is [MUI's Switch](https://mui.com/components/switches/).
* `range`
    * `slider` (default). The `start`, `end`, and `step` values for `slider` are the same as those specified when initializing a `range`-type argument. The UI component is [MUI's Slider](https://mui.com/components/slider/).
  * Examples:

    ```python
    def input_types(
        prompt: str,
        advanced_features: bool = False,
        model: typing.Literal['GPT-3.5', 'GPT-4.0', 'Llama-2', 'Falcon-7B']= 'GPT-4.0',
        max_token: range(100, 200, 20)=140,
        )  -> str:
        return "This is a dummy function. It returns nothing. "
    ```

    ![widgets for basic data types](./screenshots/input_widgets.png)

#### Python built-in compound types

* `typing.List[T]` (`typing` is Python's built-in module)
  * `T` can only be `int`, `float`, `str` or `bool`
  * Elements of `typing.List[T]` will be collectively displayed in one widget together.
  * allowed widget names:
    * `simplearray` (default): The collective UI is [RJSF ArrayField](https://rjsf-team.github.io/react-jsonschema-form/), while the UIs for elements are the default one for type `T`.
    * `[simplearray, WIDGET_OF_BASIC_TYPE]`: This option allows customizing the UI for elements.  `WIDGET_OF_BASIC_TYPE` is a widget name for a basic data type above. The collective UI is [RJSF ArrayField](https://rjsf-team.github.io/react-jsonschema-form/) while the UIs for elements are per `WIDGET_OF_BASIC_TYPE`.
    * `sheet`: All function arguments of this type will be displayed in an Excel-like sheet. The collective UI is [MUIX DataGrid](https://mui.com/x/react-data-grid/) while the UIs for elements are the default one for type `T`.
    * `[sheet, WIDGET_OF_BASIC_TYPE]`: This option allows customizing the UI for elements. Usage is similar to that of `[simplearray, WIDGET_OF_BASIC_TYPE]` above.
    * `json`: JSON string laid out with toggles, indentations, and syntax highlights. The UI is [React-Json-View](https://github.com/mac-s-g/react-json-view).
  * Examples (To add and must add)
* `typing.TypedDict` (`typing` is Python's built-in module)
  * allowed widget names:
    * `json` (default and only): Any value or key in the dict can be of type `int`, `float`, `str` or `bool` only. The UI is [React-Json-View](https://github.com/mac-s-g/react-json-view)
* `list`, `dict`, `typing.Dict` (`typing` is Python's built-in module)
  * allowed widget names:
    * `json` (default and only): The UI is [React-Json-View](https://github.com/mac-s-g/react-json-view).
* `typing.Literal` (`typing` is Python's built-in module)
  * allowed widget names:
    * `radio` (default): a radio button group. The UI is [MUI's Radio](https://mui.com/components/radio-buttons/).
    * `select`: a dropdown menu. The UI is [MUI's Select](https://mui.com/components/selects/).
* Examples
  * Example 1:

    ```python
      import funix
      from typing import List


      @funix.funix(
        widgets = {
          "a": "sheet",
          "b": ["sheet", 'slider[0, 100.0, 0.1]']
        }
      )
      def just_test(a: List[int], b: List[float]) -> dict:
        return {"a": a, "b": b}
    ```

    ![Sheet slider](./screenshots/sheet_slider.png)

#### Funix's additional MIME types

Via the module `funix.hint`, Funix adds widgets to allow users to drag-and-drop MIME files as a web app's inputs. They will be converted into Python's `bytes` type.

There are four types: `BytesImage`, `BytesVideo`, `BytesAudio`, and `BytesFile`. They are all subclasses of Python's native [`bytes` type](https://docs.python.org/3/library/stdtypes.html#bytes). The difference is that `BytesImage`, `BytesVideo`, and `BytesAudio` will be rendered into image, video, and audio players, respectively, while `BytesFile` will be rendered into a file uploader.

* Examples:
  * [ChatPaper](https://github.com/forrestbao/ChatPaper), a web app using ChatGPT API to query information in a user-uploaded PDF file.
    ![ChatPaper](https://github.com/forrestbao/ChatPaper/raw/main/screenshot.png)
  * RGB2Gray converter
    ```python
    import  io # Python's native

    import PIL # the Python Image Library
    import funix

    @funix.funix(
        title="Convert color images to grayscale images",
    )
    def gray_it(image: funix.hint.BytesImage) -> funix.hint.Image:
        img = PIL.Image.open(io.BytesIO(image))
        gray = PIL.ImageOps.grayscale(img)
        output = io.BytesIO()
        gray.save(output, format="PNG")
        return output.getvalue()
    ```
    ![RGB2Gray](./screenshots/rgb2gray.png)

#### Funix's additional types for scientific libraries

* `ipywidgets.password`: inputbox with password mask. The UI is [MUI's TextField](https://mui.com/material-ui/react-text-field).
* `ipython`
  * `ipython.display.Image`: image. Same as `BytesImage` above.
  * `ipython.display.Video`: video. Same as `BytesVideo` above.
  * `ipython.display.Audio`: audio. Same as `BytesAudio` above.
* `pandera` custom data frame schema: The UI is [MUIX DataGrid](https://mui.com/x/react-data-grid/).

#### Customizing the input widgets per-variable

Although Funix does not recommand customizing the widgets per-variable (the preferred way is via themes), it is still possible to do so via the Funix decorator attribute `widgets`. The value provided to `widgets` must be a `Dict[str, str|List]`, where a key represents a variable name (a `str`) while a value is a Funix-supported widget name mentioned above (a `str`, e.g., `"slider"`), or optionally for a parametric widget, a list of a widget name (`str`) and a `Dict[str, str|int|float|bool]` dictionary (parameters and values), e.g., `["slider", {"min":0, "max":100, "step":2}]`.

For example, the code below shows three syntaxes to associate four `int`/`float`-type variables to  sliders:

```python
import funix

@funix.funix(
  widgets={
    "x": "slider",  # default min, max and range
    "y": "slider[-10, 100, 0.25]", # one str for all parameters
    "z1": ["slider", {"min": 1, "max": 2, "step": 0.1}],
    "z2": ["slider", {"max": 2, "step": 0.1}],  # default min, custom max and step
  }
)
def square(x: int, y: float, z1: float, z2: float) -> float:
    return x + y + z1 + z2
```

### Output types and widgets

Funix supports the following output types.

#### Python built-in output types

* `int`, `float`: Displayed as `<code></code>`
* `str`: Displayed as `<span></span>`
* `bool`: Displayed as [MUI Checkbox](https://mui.com/material-ui/react-checkbox/)
* `typing.List` and `list`: Displayed in either React-JSON-Viewer or MUIX DataGrid. There will be a radio box on the front end for the user to switch between the two display options at any time, and the JSON Viewer will be used by default.
* `typing.TypedDict`, `typing.Dict`, `dict`: Displayed as ibid.

#### Output types from popular scientific libraries

* `matplotlib.figure.Figure`: For interactively displaying matplotlib plots. Currently, only 2D figures of matplotlib are supported. Rendered as [Mpld3 Plot](https://mpld3.github.io/)
* `jaxtyping`: The typing library for Numpy, PyTorch, and Tensorflow. Coming soon!
* `ipython`
  * `ipython.display.Markdown`: Markdown syntax. The UI is [React-Markdown](https://github.com/remarkjs/react-markdown) for output.
  * `ipython.display.HTML`: HTML syntax.
  * `ipython.display.Image`, `ipython.display.Video`, `ipython.display.Audio`: For displaying images, videos, and audios. The URL(s) is(are) either a local path (absolute or relative) or web URI links, e.g., at AWS S3.
* Examples
  ```python
  from typing import List
  import matplotlib.pyplot as plt
  from matplotlib.figure import Figure
  import random

  import funix

  @funix.funix(
          widgets={
            "a": "sheet",
            "b": ["sheet", "slider"]
          }
  )
  def table_plot(
          a: List[int]=list(range(20)),
          b: List[float]=[random.random() for _ in range(20)]
      ) -> Figure:
      fig = plt.figure()
      plt.plot(a, b)
      return fig
  ```
  ![slider-sheet](./screenshots/table_plot.png)

#### Additional output MIME types supported via `funix.hint`

* `funix.hint.Markdown`: For rendering strings that are in Markdown syntax. It's okay if the type is simply `str` -- but you will lose the syntax rendering. Rendered into HTML via [React-Markdown](https://github.com/remarkjs/react-markdown)
* `funix.hint.HTML`: For rendering strings that are in HTML syntax. It's okay if the type is simply `str` -- but you will lose the syntax rendering. Displayed into a `<div></div>` tag.
* `funix.hint.Image`, `funix.hint.Video`, `funix.hint.Audio`, `funix.hint.File`: For rendering URLs (either a `str` or a `typing.List[str]`) into images, vidoes, audios, and file downloaders. The URL(s) is(are) either a local path (absolute or relative) or web URI links, e.g., at AWS S3.
* `funix.hint.Code`: For rendering a string as a code block. Rendered using [Monaco Editor for React](https://github.com/suren-atoyan/monaco-react).
* Examples
  * Displaying a local still image
    ```python
    import funix

    @funix.funix()
    def display_a_image() -> funix.hint.Image:
      return "./files/test.png"
    ```
  * DallE
    ```python
    import funix

    @funix.funix()
    def dalle(Prompt: str) -> funix.hint.Image:
      response = openai.Image.create(prompt=Prompt)
      return response["data"][0]["url"]
    ```
    ![DallE](./screenshots/dalle.jpg)

## Themes

One principle of Funix is to select the widget for a variable automatically based on its type without manual intervention, which is tedious, redundant, and inconsistent across multiple apps/pages.
The mapping from a type to a widget is defined in a theme.

Besides controlling the type-to-widget mapping, a theme also controls other appearances of widgets, such as color, size, font, etc. In particular, Funix renders widgets using [Material UI, also called MUI](https://mui.com/). Thus a Funix theme gives users the direct access to MUI components and their properties (`props`).

### Defining a theme

A theme definition is a JSON dictionary of four parts: `name`, `widgets`, `props`, `typography`, and `palette`, like the example below:

```jsonc
{
  "name": "test_theme",
  "widgets": {    // dict, map types to widgets
    "str": "inputbox",
    "int": "slider[0,100,2]",
    "float": ["slider", { "min": 0, "max": 100, "step": 2 }],
    "Literal": "radio"
  },
  "props": {
    "slider": {
      "color": "#99ff00"
    },
    "radio": {
      "size": "medium"
    }
  },
  "typograhpy": {
    "fontSize": 16,   // font size, px
    "fontWeight[Light|Regular|Medium|Bold]": 500, // Font weight in light, regular, medium or bold
    "h1": {
      "fontFamily": "Droid Sans",
      "letterSpacing": "0.2rem"   // Word spacing
    }
  },
  "palette": {
    "background": {
      "default": "#112233",   // Default background color
      "paper": "#112233"    // In <Paper /> color
    },
    "primary": {
      "main": "#ddcc11",
      "contrastText": "#d01234"
    }
  }
}
```

A theme definition dictionary contains five fields, `name`, `widgets`, `props` `typography`, and `palette` that are all **optional**:

* The value of the `name` field must be a string, defining the name of the theme.
* The value of the `widgets` field is the same as the one for [the `widgets` attribute in a Funix decorator](#input-types-and-their-widgets) which is a `Dict[str|List[str], str|List]`, where a key represents a type (a `str`, e.g., `"str"`) while a value is a string (e.g., `"inputbox"`), or optionally for a parametric widget, a list of a string (widget name) and a dictionary (parameters and values), e.g., `["slider", {"max":10, "step":2}]`.
* As a dictionary, the `props` field maps Funix widgets (a `str`) to their Material-UI props (a `dict`). It gives a user direct access to `props` of an MUI component. In the example above, we set [the `color` prop of MUI's `slider`](https://mui.com/material-ui/api/slider/#Slider-prop-color) and [the `size` prop of MUI's `radio`](https://mui.com/material-ui/api/radio/#Radio-prop-size).
* The `typograph` field is a subset of the `typograph` field in a [MUI theme object](https://mui.com/material-ui/customization/default-theme/?expand-path=$.typography), expressed as a nested dictionary.
* Similar to the `typograph` field, the `palette` field is a subset of the `palette` field in a [MUI theme object](https://mui.com/material-ui/customization/default-theme/?expand-path=$.typography), expressed as a nested dictionary.

### (Optional) Importing a theme or defining a theme on-the-fly

You can import a theme from

* a local file path
* a web URL, or
* a JSON string defined on-the-fly.

You can then use the name (provided in the theme definition) or the alias to refer to the theme later.

The example below renames two themes imported by the `alias` argument.

```python
import funix


# Importing from web URL
funix.import_theme(
  "http://example.com/my_themes.json",
  alias = "my_favorite_theme"
) # optional


# Importing from local file

funix.import_theme(
  "../my_themes.json",
  alias = "my_favorite_theme"
) # optional
```

The example below defines a theme on-the-fly and imports it (without aliasing it) for later use.

```python
import funix

theme_json = {
  # theme definition
  "name": "grandma's secret theme"
  "widgets" : {
    "range" : "inputbox"
  }
}

funix.import_theme(theme_dict = theme_json)
```

### Using a theme

A theme can be applied to all functions in one `.py` Python script from

* a web URL
* a local file path
* a theme name imported earlier

using the `set_default_theme()` function.
If you have multiple `set_default_theme()` calls, then the last one will overwrite all above ones.

```python
import funix

funix.set_default_theme("https://raw.githubusercontent.com/TexteaInc/funix-doc/main/examples/sunset_v2.json") # from web URL

funix.set_default_theme("../..//sunset_v2.json") # from local file

funix.set_default_theme("my_favorite_theme") # from alias or name
```

Alternatively, a theme can be applied to a particular function, again, from a web URL, a local file path, or a theme name/alias:

```python
import funix

@funix.funix(theme = "https://raw.githubusercontent.com/TexteaInc/funix-doc/main/examples/sunset.json")
def foo():
  pass

@funix.funix(theme = "../../themes/sunset.json")
def foo():
  pass

@funix.funix(theme = "grandma's secret theme") # "sunset" is a theme alias
def foo():
  pass
```



## Setting the default and example values in widgets

Quite often, a web app has default or example values prefilled at widgets for convenience. Funix provides handy solutions to support them.

Default values can be set using Python's built-in default value for keyword arguments.
Then the default value will be pre-populated in the web interface automatically.


<!-- add example -->

There is no Python's built-in way to set example values. Funix provides a decorator attribute `examples` to support it. The value to be provided to `examples` attribute is a `Dict[str, typing.List[Any]]` where the key is an argument name and the value is a list of example values.

Example 1:

```python
@funix.funix(
    examples={"arg3": [1, 5, 7]}
)
def argument_selection(
    arg1: str = "prime",
    arg2: typing.Literal["is", "is not"]="is",
    arg3: int = 3,
) -> str:
    return f"The number {arg3} {arg2} {arg1}."

```

![literal](./screenshots/default_example_literal.png)

Example 2:

```python
import os
import funix
import typing
import openai
openai.api_key = os.environ.get("OPENAI_KEY")

@funix.funix(
  examples = {"prompt": ["Who is Einstein?", "Tell me a joke. "]}
)
def ChatGPT_single_turn(
  prompt: str,
  model : typing.Literal['gpt-3.5-turbo', 'gpt-3.5-turbo-0301'] = 'gpt-3.5-turbo'
) -> str:
  completion = openai.ChatCompletion.create(
    messages=[{"role": "user", "content": prompt}],
    model=model
  )
  return f'ChatGPT says:  {completion["choices"][0]["message"]["content"]}'
```

<!-- Add screenshot -->

## Naming your app or widgets

To help users understand your app or widgets, you can explain them using the decorator attributes `title`, `description` and `argument_labels` respectively. The value provided to `title` or `description` is a Markdown-syntax string. The `title` will appear in the top banner as well as the right navigation bar. The value provided to `argument_labels` is of the type `Dict[str, str]` where the key is an argument name and the value is a Markdown-syntax string.

Example 1:

```python
import funix

@funix.funix(
  title="BMI Calculator",
  description = "**Calculate** _your_ BMI",
  argument_labels = {
    "weight": "Weight (kg)",
    "height": "Height (m)"
  }
)
def BMI(weight: float, height: float) -> str:
    bmi = weight / (height**2)
    return f"Your BMI is: {bmi:.2f}"
```

![BMI example demonstrating ](screenshots/bmi_description_labels.png)

## Customizing layouts

By default, Funix puts the input and output widgets in two panels that are put side-by-side, respectively.
In either panel, widgets are laid out in the order they appear in the function's signature, one-widget per line and top-down.

### Customizing the panel arrangement

The input and output panel are by default placed left to right. You can change their order and orientation using the `direction` attribute in a Funix decorator. The example below shall be self-explaining:

```python
import funix

@funix.funix()
def foo_default(x:int) -> str:
    return f"{x} appears to the row, default"

@funix.funix(
    direction="column"
)
def foo_bottom(x:int) -> str:
    return f"{x} appears at the bottom"

@funix.funix(
    direction="column-reverse"
)
def foo_top(x:int) -> str:
    return f"{x} appears at the top"

@funix.funix(
    direction="row-reverse"
)
def foo_left(x:int) -> str:
    return f"{x} appears to the left"
```

A more advanced example is our ChatGPT multiturn app where `direction = "column-reverse"` so the message you type stays at the bottom. The source code can be found in `$FUNIX_ROOT/examples/AI/chatGPT_multi_turn.py`. Here is the screenshot:

![ChatGPT multiturn](./screenshots/chatGPT_multiturn.png)

### Customizing the widget layout

The input and output layout can be customized via the attribute `input_layout` and `output_layout` that use a row-based layout system where each row is a list of cells. Each cell is a dictionary that specifies the widget type & name and the number of columns it occupies.
The type of `input_layout` and `output_layout` is:

```python
typing.List[  # each row
  typing.List[ # each cell in the same row
    typing.Dict[str, str|int]  # see below
  ]
]
```

The per-cell dictionary must have one entry, whose

* **key** specifies the widget type, which is a string "argument" (if the widget is an input/argument), "return_index" (if the widget is an output/return), "markdown", "html", or "divider".
* **value** is the content of the widget
  * If the widget type is "argument", then the value is the argument name as a `str`.
  * If the widget type is "return_index", then the value is the index of the return value as an `int`.
  * If the widget type is "markdown" or "html", then the value is a Markdown- or HTML-syntax string.
  * If the widget type is "divider", then the value is the text to be displayed on the divider. When the text is an empty string, then nothing is displayed.

Optionally, the per-cell dictionary can contain an entry of the string key `width` and the value being a `float`. The value specifies the number of columns, as defined in [MUI's Grid](https://mui.com/material-ui/react-grid/), the cell occupies. The default value is 1.

Note that widgets not covered in `input_layout` or `output_layout` will be displayed in the default order and after those covered in `input_layout` and `output_layout`.

**Example 1**: Source code: `examples/layout_simple.py`

```python
import funix


@funix.funix(
    input_layout=[
        [{"markdown": "### Sender information"}],  # row 1
        [
            {"argument": "first_name", "width": 3},
            {"argument": "last_name", "width": 3},
        ],  # row 2
        [{"argument": "address", "width": 6}],  # row 3
        [  # row 4
            {"argument": "city", "width": 2.5},
            {"argument": "state", "width": 2},
            {"argument": "zip_code", "width": 2},
        ],
        [{"html": "<a href='http://funix.io'>We love Funix</a>"}],  # row 5
    ],
    output_layout=[
        [{"divider": "zip code is "}],
        [{"return_index": 2}],
        [{"divider": "from the town"}],
        [{"return_index": [0, 1]}],
    ],
)
def layout_shipping(
    first_name: str, last_name: str, address: str, city: str, state: str, zip_code: str
) -> (str, str, str):
    return city, state, zip_code
```

![Layout sender](screenshot/../screenshots/layout_sender.png)

**Example 2: Using EasyPost API**: Source code: `$FUNIX_ROOT/examples/layout_easypost_shipping.py`

![Layout shipping](./screenshots/easypost_shipping.png)

## Conditional input widget display

Funix allows controlling the appearance of input widgets based on the values of other widgets via the attribute `conditional_visible` which is of the type:

```python
typing.List[ # a series of rules
  typing.TypedDict( # each rule
    "show": typing.List[str] # arguments visible only
    "when": typing.List[     # when conjuction of conditions holds
        typing.Dict[str, Any]  # each condition
    ]
  )
]
```

`show`'s value is a list of argument name strings.
`when`'s value is a list of dictionaries, representing a series of conditions whose conjunction must be True for arguments in corresponding `show` list to appear.

If `when`'s value is

`{"argument1": value1, "argument2": value2}`,

then it means the condition

`argument1 == value1 && argument2 == value2`

**Example** (Source code `examples/conditional_simple.py`):

```python
import typing
import openai
import funix

openai.api_key = os.environ.get("OPENAI_KEY")

@funix.funix(
  widgets={"prompt":"textarea", "model": "radio"},
  conditional_visible=[
    {
      "when": {"show_advanced": True,},
      "show": ["max_tokens", "model", "openai_key"]
    }
  ]
)
def ChatGPT_advanced(
  prompt: str,
  show_advanced: bool = False,
  model : typing.Literal['gpt-3.5-turbo', 'gpt-3.5-turbo-0301']= 'gpt-3.5-turbo',
  max_tokens: range(100, 200, 20)=140,
  openai_key: str = ""
) -> str:
  completion = openai.ChatCompletion.create(
    messages=[{"role": "user", "content": prompt}],
    model=model,
    max_tokens=max_tokens,
  )
  return completion["choices"][0]["message"]["content"]
```

![conditional visible](./screenshots/conditional_visible.gif)

## Per-argument configuration via `argument_config`

In all examples above, we provide values for each attribute (such as `widgets`, `examples`, or `argument_labels`) in a Funix decorator like this:

```python
import funix


@funix.funix(
  attribute_name_1 = {
    argument_1: ...
    argument_2: ...
  },
  attribute_name_2 = {
    argument_1: ...
    argument_2: ...
  },
)
```

When there are many arguments, this may be inconvenient because different attributes of the same argument are scattered.

Hence, Funix introduces a new attribute `argument_config` to support grouping all attributes of the same argument together. The example above can be rewritten as below:

```python
import funix


@funix.funix(
  argument_config = {
    argument_1: {
      attribute_name_1: ...
      attribute_name_2: ...
    },
    argument_2: {
      attribute_name_1: ...
      attribute_name_2: ...
    }
  }
)
```

## Call history

Funix automatically logs the calls of an app in your browser for you to review the history later. This can be particularly useful when you want to compare the outputs of an app given different inputs, e.g., different conversations with ChatGPT. Funix offers two ways to view the history: the rightbar and the comprehensive log.

The history rightbar can be toggled like in GIF below. All calls are timestamps. Clicking on one history call will popular the input and output of the call to the input and output widgets. You can further (re)name, delete and export (to JSON) each call.

![history sidebar](./screenshots/history_sidebar.gif)

A comprehensive log can be toggled by clicking the clock icon at the top right corner of a Funix-converted app. The inputs and outputs of each call are presented in JSON trees. You can jump from the JSON tree to the UI with the inputs and outputs populated by clicking the "View" button under a call. Note that the comprehensive log presents calls for all Funix-converted apps in your browser, unlike the history rightbar which displays history per-app.

![history comprehensive log](./screenshots/history_comprehensive_log.gif)

## Multipage apps and sessions/states

Building a multipage app in Funix is easy: one function becomes one page and you can switch between pages using the function selector. Passing data between pages are done via global variables. Simply use the `global` keyword of Python.

Examples:
* A simple global variable-based state management
  ```python
  import funix

  y = "The default value of y."

  @funix.funix(  )
  def set_y(x: str="123") -> str:
      global y
      y = x
      return "Y has been changed. Now check it in the get_y() page."


  @funix.funix( )
  def get_y() -> str:
      return y
  ```

  ![multipage app via global variables](./screenshots/multipage_global.gif)

### Sessions

We have seen how to use a global variable to pass values between pages. However, the value of a global variable is shared among all users. This can be dangerous. For example, an API token key is a global variable set in one page and used in the other. Then once a user sets the API token key in the former page, all other users can it freely in the latter page though they may not be able to see the token value.

To avoid this situation, we need to sessionize each browser's connection to a Funix app. To do so, add the `-t` option when launching the `funix` command, e.g.,

```bash
funix session_simple.py -t
```

The video/GIF below shows that in the private and non-private modes of a browser (thus two separate sessions), the global variable `y` in the code above has different values. Changing the value of `y` in one window won't change its value in another window.

![sessioned global y](./screenshots/session.gif)

A more practical example is in `$FUNIX_ROOT/examples/AI/openAI_minimal.py` where openAI key is sessionized for users to talk to OpenAI endpoints using their individual API keys.


**Known bugs**: However, there are many cases that our simple AST-based solution does not cover. If sessions are not properly maintained, you can use two Funix functions to manually set and get a session-level global variable.

```python
from funix import funix
from funix.session import get_global_variable, set_global_variable, set_default_global_variable


set_default_global_variable("user_word", "Whereof one cannot speak, thereof one must be silent")


@funix()
def set_word(word: str) -> str:
    set_global_variable("user_word", word)
    return "Success"


@funix()
def get_word() -> str:
    return get_global_variable("user_word")
```


### Linking pages together via `prefilling`

A special case of passing data across pages is to pass (part of) the output of a function to an input of another.
Funix supports this via the `prefill` attribute of a Funix decorator. For example,

```py
import funix

def first_action(x: int) -> int:
  return x - 1

def second_action(message: str) -> list[str]:
  return message.split(" ")

def third_action(x: int, y: int) -> dict:
  return {"x": x, "y": y}

@funix.funix(
  pre_fill={
    "a": first_action,
    "b": (second_action, -1),
    "c": (third_action, "x")
  }
)
def final_action(a: int, b: str, c: int) -> str:
    return f"{a} {b} {c}"
```

This multi-page app has 4 pages/functions/steps. The results from  `{first, second, third}_action` are used collectively in the final one `final_action`.

The `prefill` attribute takes in a dictionary of type

```python
Dict[
  str,  # string of a function argument
    Callable |  # callable returns an int, float, str, or bool
    Tuple(Callable, int) |  # callable returns a sequence, int is the index
    Tuple (Callable, int|str) # callable returns a dict, int|str is the key
]
```

The key is a `str`, corresponding to an argument of the function being prefilled.
The value can be of three cases:

1. a callable, if the callable has a non-compound return value -- in this case, the return of the callable is sent to the corresponding argument of the function being prefilled.
2. a tuple of a callable and an index, if the callable returns a sequence -- in this case, the return of the callable that match the index is sent to the corresponding argument of the function being prefilled.
3. a tuple of a callable and a `str`, if the callable returns a dictionary -- in this case, the return of the callable and of the key is sent to the corresponding argument of the function being prefilled.

## Rate Limit

Some APIs may be expensive (e.g. ChatGPT), and if they are not rate-limited, you may have a large deficit on your credit card.

Funix provides an easy way to apply the rate limit.

![Rate limit exceeded](./screenshots/rate-limit.png)

```python
# For easy configuration, you can pass a dict

# 10 requests per browser per minute
@funix(rate_limit={"per_browser":10})
def per_browser():
  pass

# Or limit based on IP:
@funix(rate_limit={"per_ip":100})
def per_ip():
  pass

# based on both IP and browser:
@funix(
  rate_limit={
    "per_ip": 100,
    "per_browser": 10
  }
)
def per_browser_and_ip():
  pass

# If you want to set a custom period, pass a list of dict
@funix(
    rate_limit=[
        # 1 request per day per browser
        {"per_browser": 1, "period": 60 * 60 * 24},
        {"per_ip": 20},
    ],
)
def custom_period():
  pass
```

## Stream mode

Some functions may take a long time to run, and you may want to see the intermediate results as they are generated. Funix provides a stream mode to support this. You can use `yield` to return intermediate results. The return value of the function is the final result.

Or you want to implement some functions that can be refreshed in time, such as chat or real-time text generation, here is an example of ChatGPT:

```python
from funix import funix
from funix.hint import Markdown

from openai import OpenAI


@funix()
def chatGPT(prompt: str) -> Markdown:
    client = OpenAI(api_key="xxx")
    stream = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-3.5-turbo",
        stream=True,
    )
    message = []
    for part in stream:
        message.append(part.choices[0].delta.content or "")
        yield "".join(message)
```

You don't need turn on the stream mode manually, Funix will detect the `yield` statement and turn on the stream mode automatically.

### Print to web

It's okay to use `print` for just printing something to the web. Funix will capture the stdout and display it in the output panel. But you need turn on the `print_to_web` mode in decorator manually.

```python
from funix import funix

@funix(print_to_web=True)
def print_to_web():
    print("Hello world!")
```

It will force the function to run in the stream mode, and **don't care about your return annotations**. Funix will force the return type to `Markdown`, and the return value will be the appended to the output panel.

## Class

> [!IMPORTANT]
> Funix may not be able to read your class source code correctly. Please ensure that your class code is indented normally. It is best not to have multi-line text without indentation that "destroys" the indentation function. It would break the current simple class code getter, which only gets the source code based on indentation.

We can also use class to define a Funix app. It's good for stateful apps and some people don't like global variables. Just use the `funix.funix_class` decorator.

```python
from funix import funix_class


class A:
  def __init__(self, value: int = 0):
    self.value = value

  def add(self, x: int) -> int:
    self.value += x
    return self.value


@funix_class()
A(1)
```

If you want user can construct the class by themselves, you can do like this:

```python
from funix import funix_class


@funix_class()
class A:
  def __init__(self, value: int = 0):
    self.value = value

  def add(self, x: int) -> int:
    self.value += x
    return self.value
```

For classes that have been built, funix will treat them as classes shared by all users. For classes that need to be built manually, funix will record a separate class for each user.

### Method with config

You can use `funix.funix_method` decorator like `funix` to configure methods in a class. Funix will read the config from the `funix_method` decorator and apply it to the method.

```python
from funix import funix_class, funix_method


@funix_class()
class A:
  @funix_method(title="Create a new A instance")
  def __init__(self, value: int = 0):
    self.value = value

  def add(self, x: int) -> int:
    self.value += x
    return self.value
```

### Disable some methods

Although you can add `__` prefix to the method name to "hide" it, it's not a good way to disable a method in funix. Funix provides a better way to do this. Just use `disable` argument in `funix_method` decorator.

```python
from funix import funix_class, funix_method


@funix_class()
class A:
  @funix_method(title="Create a new A instance")
  def __init__(self, value: int = 0):
    self.value = value

  def add(self, x: int) -> int:
    self.value += x
    return self.value

  @funix_method(disable=True)
  def need_private_but_i_do_not_want_to_add_underscore(self):
    pass
```

Funix will skip the method with `disable=True` in the class.

## Secret

Very often you wanna protect the access to your app. Funix offers a simple way to do that: generating a random token that needs to be attached to the URL in order to open the app in a browser.

To do so, just toggle the command line option `secret` when launching a Funix app. You can provide a token or let Funix generate one for you.

```bash
funix  my_app.py --secret  my_secret_token # use a token provided by you
or
funix  my_app.py --secret  True # randomly generate a token
```

The token, denoted as `TOKEN` in the rest of this seciton,  will be printed on the Terminal. For example,

```bash
$ funix hello.py --secret True
Secrets:
---------------
Name: hello
Secret: 8c9f55d0eb74adbb3c87a445ea0ae92f
Link: http://127.0.0.1:3000/hello?secret=8c9f55d0eb74adbb3c87a445ea0ae92f
```

To access the app, you just append `?secret=TOKEN` in the app URL. In the example above, the URL to properly open the app is `http://127.0.0.1:3000/hello?secret=8c9f55d0eb74adbb3c87a445ea0ae92f`. Bad guys trying to access your app via `http://127.0.0.1:3000/hello` (no secret in the URL) will not be able to run your app.

However, if you are not a bad guy but just a forgetful person, you can still access your app without the token in the URL. Just click the "secret" button on the top right corner of the app, and enter the secret in a pop-up window, then you can use the app.

![enter secret](./screenshots/secret.gif)

> Note: This is not a strong way to protect your app.

## Backend APIs

TBD.
