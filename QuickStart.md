# The Quick Start Guide of Funix 

Your Python function definition is your web app! 

![How funix works](./illustrations/workflow.png)


## Introduction

* Funix allows you to build web apps by focusing on your core logic in Python, without bothering about the front-end or web UI.
* With **as few as two more lines of code**, you can turn any Python function into a web app via Funix.
* Unlike other Python-based frameworks for building web apps, Funix does not require you to create widgets in Python. **Just focus on your core logic.**
* But if you need to customize the UI, you can do it declaratively in Python, YAML, or JSON. Themes can also be used to provide consistent UI across your web apps.
* How: Funix automatically chooses I/O widgets for your web app by analyzing the typing hint in your function's signature. 
* Open source under the MIT license.

## Acknowledgement
We were inspired by FastAPI's approach of using typing hints to build apps. We also want to thank Streamlit, Gradio, PyWebIO, and Pynecone for their influence on the development of Funix. Our backend is implemented using Flask, and the front-end primarily using Material UI. Lastly, Funix was made possible with the generous investment from Miracle Plus Fund I to Textea Inc. 

## Installing Funix

```bash
pip install funix
```

or from Funix's GitHub repo

```bash
pip install "git+https://github.com/TexteaInc/funix.git"
```

## Just two more lines of code 

Funix's goal is to minimize the amount of code you need to write to build a web app. A Python function can be turned into a web app by adding **as few as two lines of code**. For example, the code below prepends two lines (first importing a Funix decorator and then decorate the function `hello` using the decorator `@funix()`) to the function `hello()`:

```python
from funix import funix # add line one

@funix()                # add line two 
def hello(your_name: str) -> str:
    return f"Hello, {your_name}."
# You are done! 
```

Save the code above as `hello.py`.
Then run this at the terminal:

```bash
python3 -m funix hello
```

A web app will be launched at `http://localhost:80`.

Note that on many Linux systems, you may need  need to run the above command with `sudo` to use port 80. Or, you can use a port that does not need the root privilege, such as 3000, by running:

```bash
python3 -m funix hello_world -P 3000
```

Then the web app will be launched at `http://localhost:3000`.

![](screenshots/hello.png)

Wolla! Now anyone can use a Python function you write without knowing Python or having the computing environment. 

## More examples

**Customizing widgets is easy**

**Vector opeartions**

**Slider and plots**

**Only decorated functions are converted to web apps.**

**Multiple I/Os**

## Funtion I/O types and widgets

Funix works by mapping the I/O types of a function to the corresponding I/O widgets. 
Typing hints must be included for all the inputs and outputs of a function. 

### Customizing individual widgets

To customize widgets, use the parameter `widgets` in a Funix decorator. For example, 
the code below changes the widget for an integer input from the default input box to a slider:

```python
from funix import funix
@funix(widgets={"x": "slider"})
def square(x: int) -> int:
    return x * x
```

Funix supports decorating a function with three  decorators: `@funix`, `@funix_yaml`, and `@funix_json5`, which are based on the syntaxes of Python, YAML, and JSON5, respectively. More details are in the section [Decorator syntaxes](#decorator-syntaxes). We will use whatever syntax the easiest to get the job done in this document.

The three decorators are equivalent except on the syntax. The code above is equivalent to YAML and JSON5 verisons below. 

```python
from funix import funix_json5
@funix_json5("""
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
from funix import funix_yaml
@funix_yaml("""
widgets:
  x: slider
""")
def square(x: int) -> int:
    return x * x
``` 

#### **Input widgets**

The input widgets are mapped from the inputs of a function. Their default and optional widgets are listed below.

#### **Output widgets**
ddddd

## Decorator syntaxes

## Themes

### Using themes

### Defining themes

## Layouts

## Conditional widget display

## Decorator syntaxes

## Backend APIs
