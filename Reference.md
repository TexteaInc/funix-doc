# The Reference Manual of Funix 

*Who should read it*: This reference manual is for those who want to customize their apps under the Funix framework. If you are new to Funix, please read the [QuickStart Guide](QuickStart.md) first.  

## The lazy mode

The lazy mode converts a type-hinted Python function into a web app with default settings. It is the simplest way to build a web app in Funix. 

Suppose you have a Python function defined in a file `hello.py`. Then you can convert it to a web app using the command 

```bash
funix -l hello.py
```

The web app runs at `http://localhost:80` in a browser window automatically popped. The arguments of the function are mapped to the input widgets of the web app. The return values of the function are displayed in the output widget.

## The Funix decorators
The appearance and behavior of a web app can be customized using Funix decorators.  For example, the code below changes the widget for an integer input from the default input box to a slider:

```python
import funix
@funix.funix(
    widgets={
        "x": "slider"
        }
    )
def square(x: int) -> int:
    return x * x
```

Funix supports decorating a function with three decorators: `@funix`, `@funix_yaml`, and `@funix_json5`, which are based on the syntaxes of Python, YAML, and JSON5, respectively. The example above can be expressed in YAML and JSON5 as below. 

```python
import funix
@funix.funix_json5("""
{
    widgets: {
        x: slider
    }
}
""")
def square(x: int) -> int:
    return x * x
```

```python
import funix
@funix.funix_yaml("""
widgets:
  x: slider
""")
def square(x: int) -> int:
    return x * x
```

We will use whatever decorator the easiest to get the job done in this document.

## Supported I/O types and widget customization

To customize the widget of a Funix-decorated function, use the Funix decorator attribute `widget`. 
The value provided to `widget` must be a `Dict[str|List[str], str]` where the key is an argument name or a list of argument names and value is a widget name.

### Input types and their widgets

#### Atomic types: 

* `int` and `float`
  * allowed widget names:
    * `input` (default): a text input box where only digits and up to one dot are allowed. The UI is [MUI's TextField type=number](https://mui.com/material-ui/react-text-field/#type-quot-number-quot). 
    * `slider`: a slider. You can optionally set the arguments `start`, `end`, and `step` using a function call syntax `slider(start, end, step)`. For integers, the default values are `start=0`, `end=100`, and `step=1`. For floats, the default values are `start=0`, `end=1`, and `step=0.1`.  The UI is [MUI's Slider](https://mui.com/components/slider/).
  * Examples: 
    * ```python
      import funix 
      @funix.funix(
          widgets={"x": "slider(-1, 1, 0.25)"}) 
      def square(x: int) -> int:
          return x * x
      ```
* `str`
  * allowed widget names: 
    * `input` (default): a text input box. Only oneline. The UI is [MUI's TextField](https://mui.com/material-ui/react-text-field).  
    * `textarea`: Multiline text input with line breaks. The UI is [MUI's TextField with multiline support](https://mui.com/material-ui/react-text-field/#multiline).
* `bool`
  * allowed widget names: 
    * `checkbox` (default): a checkbox. The UI is [MUI's Checkbox](https://mui.com/components/checkboxes/).
    * `switch`: a switch. The UI is [MUI's Switch](https://mui.com/components/switches/).
* `range`
  * `range` type is a special type of Python, which is essentially a sequence of integers. 
  * allowed widget names:
    * `slider` (default). The `start`, `end`, and `step` values for `slider` are the same as those specified when initializing a `range`-type argument. The UI is [MUI's Slider](https://mui.com/components/slider/).
  * Examples: 
    * ```python
      def square(x: range(0, 100, 10)) -> int:
          return x * x
      ```

#### Compound types: 
* `typing.List[T]` (`typing` is Python's built-in module)
  * `T` can only be `int`, `float`, `str` or `bool`
  * Elements of `typing.List[T]` will be collectively displayed in one widget together.
  * allowed widget names:
    * `simplearray` (default): The collective UI is [RJSF ArrayField](https://rjsf-team.github.io/react-jsonschema-form/), while the UIs for elements are the default one for type `T`. 
    * `[simplearray, WIDGET_OF_ATOMIC_TYPE]`: This option allows customizing the UI for elements.  `WIDGET_OF_ATOMIC_TYPE` is a widget name for an atomic type above. The collective UI is [RJSF ArrayField](https://rjsf-team.github.io/react-jsonschema-form/) while the UIs for elements are per `WIDGET_OF_ATOMIC_TYPE`. 
    * `sheet`: All function arguments of this type will be displayed in an Excel-like sheet. The collective UI is [MUIX DataGrid](https://mui.com/x/react-data-grid/) while the UIs for elements are the default one for type `T`. 
    * `[sheet, WIDGET_OF_ATOMIC_TYPE]`: This option allows customizing the UI for elements. Usage is similar to that of `[simplearray, WIDGET_OF_ATOMIC_TYPE]` above. 
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
    * ```python
        import funix 
        import typing

        @funix.funix_yaml("""
        widgets:
        a:
            - sheet
        b:
            - sheet
            - 'slider[0, 100.0, 0.1]'
        """)
        def just_test(a: typing.List[int], b: typing.List[float]) -> dict:
            return {"a": a, "b": b}
      ```
      ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e354e547-4f57-4ba2-a907-387d6aed8471/Untitled.png)

#### Funix's additional types
Via the module `funix.widget.builtin`, Funix adds widgets to allow users to drag-and-drop MIME files as a web app's inputs. They will be converted into Python's `bytes` type. 

* `funix.widget.builtin.BytesFile`
  * Examples: 
    * [ChatPDF](https://github.com/forrestbao/ChatPaper), a web app using ChatGPT API to query information in a user-uploaded PDF file. 


### Output types and widgets
Funix supports the following output types. 

#### Python native ones 
* `int`, `float`: Displayed as `<code></code>`
* `str`: Displayed as `<span></span>`
* `bool`: Displayed as [MUI Checkbox](https://mui.com/material-ui/react-checkbox/)
* `typing.List` and `list`: Displayed in either React-JSON-Viewer or MUIX DataGrid. There will be a radio box on the front end for the user to switch between the two display options at any time, and the JSON Viewer will be used by default.
* `typing.TypedDict`, `typing.Dict`, `dict`: Displayed as ibid. 

#### Additional MIME types
To facilitate the rendering of MIME types, we introduce a module `funix.hint`. 
* `funix.hint.Figure`: For interactively displaying matplotlib plots. Currently, only 2D figures of matplotlib are supported. Rendered as [Mpld3 Plot](https://mpld3.github.io/)
* `funix.hint.Markdown`: For rendering strings that are in Markdown syntax. It's okay if the type is simply `str` -- but you will lose the syntax rendering. Rendered into HTML via [Markdown-it](https://markdown-it.github.io/) 
* `funix.hint.HTML`: For rendering strings that are in HTML syntax. It's okay if the type is simply `str` -- but you will lose the syntax rendering. Displayed into a `<div></div>` tag. 
* `funix.hint.Images`, `funix.hint.Videos`, `funix.hint.Audios`, `Funix.hint.Files`: For rendering URLs (either a `str` or a `typing.List[str]`) into images, vidoes, audios, and file downloaders. The URL(s) is(are) either a local path (absolute or relative) or web URI links, e.g., at AWS S3.
  * Examples 
<!-- FIXME: plural or singular?  -->
* `Code`: For rendering a string as a code block. Rendered using [React Syntax Highlighter Prism]

## Setting the default and example values in widgets
Quite often, a web app has default or example values prefilled at widgets for convenience. Funix provides handy solutions to support them. 

Default values can be set using Python's built-in default value for keyword arguments. 

<!-- add example -->

There is no Python's built-in way to set example values. Funix provides a decorator attribute `examples` to support it. The value to be provided to `examples` attribute is a `Dict[str, typing.List[Any]]` where the key is an argument name and the value is a list of example values.

Example 1: 
```python
import typing

from funix import funix

@funix(
        examples={"arg2": [1, 5, 7]}, 
        widgets={"arg1": "radio"}
)
def argument_selection(
        arg1: typing.Literal["is", "is not"]="is not", 
        arg2: str="prime",
        ) -> str:
    return f"The number {arg1} {arg2} {arg3}."

```

![](./screenshots/default_example_literal.png)

Example 2: 

```python
import funix
import typing
import openai 
openai.api_key = os.environ.get("OPENAI_KEY")

@funix.funix(
    prompt = ["Who is Einstein?", "Tell me a joke. "]
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
To help users understand your app or widgets, you can explain them using the decorator attributes `description` and `argument_labels` respectively. The value provided to `description` is a Markdown-syntax string. The value provided to `argument_labels` is of the type `Dict[str, str]` where the key is an argument name and the value is a Markdown-syntax string.

Example 1: 
```python
import funix

@funix.funix(
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

TBD. 

### Customizing the widget layout

The input and output layout can be customized via the attribute `input_layout` and `output_layout` that use a row-based layout system where each row is a list of cells. Each cell is a dictionary that specifies the widget type & name and the number of columns it occupies. 
The type of `input_layout` and `output_layout` is : 
```python 
typing.List[  # each row 
  typing.List[ # each cell in the same row
    typing.Dict[str, str|int]  # see below 
  ]
]
``` 

The per-cell dictionary must have one entry, whose 
* **key** specifies the widget type, which is a string "argument" (if the widget is an input/argument), "return" (if the widget is an output/return), "markdown", "html", or "divider". 
* **value** is the content of the widget
  * If the widget type is "argument", then the value is the argument name as a `str`. 
  * If the widget type is "return", then the value is the index of the return value as an `int`. 
  * If the widget type is "markdown" or "html", then the value is a Markdown- or HTML-syntax string. 
  * If the widget type is "divider", then the value is the text to be displayed on the divider. When the text is an empty string, then nothing is displayed.

Optionally, the per-cell dictionary can contain an entry of the string key `width` and the value being an integer. The value specifies the number of columns, as defined in [MUI's Grid](https://mui.com/material-ui/react-grid/), the cell occupies. The default value is 1.

Note that widgets not covered in `input_layout` or `output_layout` will be displayed in the default order and after those covered in `input_layout` and `output_layout`.

**Example 1**: 

```python
@funix.funix(
  input_layout=[
    [{"markdown": "### Sender information"}],  # row 1 
    [
      {"argument": "first_name", "width": 3}, 
      {"argument": "last_name",  "width": 3}, 
    ],    # row 2 
    [{"argument": "address", "width": 6}], # row 3 
    [ # row 4 
      {"argument": "city",  "width": 2.5}, 
      {"argument": "state", "width": 2}, 
      {"argument": "zip_code",   "width": 2}
    ], 
    [{"html": "<a href='http://funix.io'>We love Funix</a>"}],  # row 5 
  ], 
  output_layout = [
    [{"divider":"zip code is ", "return": 2}], 
    [{"divider": "from the town", "return": 0, "return": 1}], 
  ]
)
def layout_shipping(
    first_name: str, 
    last_name: str, 
    address: str, 
    city: str,
    state: str, 
    zip_code: str 
    )-> (str, str, str):
    return city, state, zip_code
```
![Layout sender](screenshot/../screenshots/layout_sender.png)

**Example 2: Using EasyPost API** [Source code](../examples/shipping.py)

![Layout shipping](./screenshots/easypost_shipping.png)

## Conditional input widget display

Funix allows controlling the appearance of input widgets based on the values of other widgets via the attribute `conditional_visible` which is of the type: 

```py
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

```{"argument1": value1, "argument2": value2}```,

then it 
means the condition 

```argument1 == value1 && argument2 == value2```

> TODO: add an example 

## Per-argument configuration via `argument_config`

In all examples above, we provide values for each attribute (such as `widgets`, `examples`, or `argument_labels`) in a Funix decorator like this: 
```py
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

```py
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


## Themes

Theme controls the appearances (such as color, size, font, widget choices) of apps. 

### Using themes

A theme, provided from a local file or a web URL, can be set to update the appearances of all functions decorated by Funix, like the two examples below: 

```py
from funix import set_global_theme

set_global_theme("./sunset_v2.yaml") 

set_global_theme("https://yazawazi.moe/pdf_themes/sunset_v2.yaml") # Theme URL
"""
```

Or a theme can be applied to individual functions like below using a Funix decorator attribute `theme`: 

```py
import funix 

@funix.funix(
  theme = "./sunset_v2.yaml"
)
def foo():
	 pass

@funix.funix(
  theme = "https://yazawazi.moe/pdf_themes/sunset_v2.yaml"
)
def foo():
	 pass
```

You can also import multiple themes, give them aliases, use the aliases to easily switch between themes instead of repeating the lengthy URLs or file paths.

```python
from funix import import_theme

"""
import_theme

# Parameter 1: URL or file path of the theme file
# Your URL must include the schema like http or https
# Parameter 2: Theme name

Local Theme Search Priority:
1. Current directory
2. ~/.funix/themes directory
3. Not found, raise Error
"""
import_theme("https://yazawazi.moe/pdf_themes/sunset_v2.yaml", name="sunset") # From URL 
import_theme("./sunset_v2.yaml", name="sunset") # From Path
```

A named theme can be applied to all functions or individual functions. For example, to use the "sunset" theme imported and name above: 

```python
import funix 
funix.set_global_theme("sunset") 

@funix.funix(
  theme = "sunset"
)
def foo():
	 pass
```

> FIXME: Yazawazi: 1) The theme URL is no longer valid. 2)  Please ensure the syntax and document are consistent. 


### Defining themes

TBD. 

## Call history

Funix automatically logs the calls of an app in your browser for you to review the history later. This can be particularly useful when you want to compare the outputs of an app given different inputs, e.g., different conversations with ChatGPT. Funix offers two ways to view the history: the rightbar and the comprehensive log. 

The history rightbar can be toggled like in GIF below. All calls are timestamps. Clicking on one history call will popular the input and output of the call to the input and output widgets. You can further (re)name, delete and export (to JSON) each call. 

![history sidebar](./screenshots/history_sidebar.gif)

A comprehensive log can be toggled by clicking the clock icon at the top right corner of a Funix-converted app. The inputs and outputs of each call are presented in JSON trees. You can jump from the JSON tree to the UI with the inputs and outputs populated by clicking the "View" button under a call. Note that the comprehensive log presents calls for all Funix-converted apps in your browser, unlike the history rightbar which displays history per-app. 

![history comprehensive log](./screenshots/history_comprehensive_log.gif) 

## Sessions

Need to turn on `t` option when starting Funix. 

```python
from funix import funix


user_word = "https://peps.python.org/pep-0339/"


@funix(
    session_variables=["user_word"],
)
def set_word(word: str) -> str:
    global user_word
    user_word = word
    return "Success"


@funix(
    session_variables=["user_word"],
)
def get_word() -> str:
    return user_word
```



```
@funix()
def set_word(word: str) -> str:
    set_global_variable("user_word", word)
    return "Success"


@funix()
def get_word() -> str:
    return get_global_variable("user_word")
```

## Passing values across pages for multipage apps


## Secret 

## Backend APIs

## Command line options 

funix -g  http://github.com/funix/funix -r examples -R . 

funix -g  http://github.com/funix/funix -r examples  better.py  

TODO: 