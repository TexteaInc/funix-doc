# The Reference Manual of Funix 

*Who should read it*: This reference manual is for those who want to customize their apps under the Funix framework. If you are new to Funix, please read the [QuickStart Guide](QuickStart.md) first.  

## The lazy mode

The lazy mode converts a type-hinted Python function into a web app with default settings. It is the simplest way to build a web app in Funix. 

Suppose you have a Python function defined in a file `hello.py`. Then you can convert it to a web app using the command 

```bash
funix -l hello.py
```

and then see the web app at `http://localhost:80` in a browser window automatically poped. The arguments of the function are mapped to the input widgets of the web app. The return values of the function are displayed in the output widget.

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

## Supported I/O types and widgets

To customize the widget of a Funix-decorated function, use the Funix decorator attribute `widget`. 
The value provided to `widget` must be a `Dict[str, str]` where the first string is an argument name and the second string is a widget name.

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

        @funix.funix_yaml("""
        widgets:
        a:
            - sheet
        b:
            - sheet
            - 'slider[0, 100.0, 0.1]'
        """)
        def just_test(a: List[int], b: List[float]) -> dict:
            return {"a": a, "b": b}
      ```
      ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e354e547-4f57-4ba2-a907-387d6aed8471/Untitled.png)


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

## Decorator syntaxes

## Themes

### Using themes

### Defining themes

## Layouts

## Conditional widget display

## Decorator syntaxes

## Backend APIs
