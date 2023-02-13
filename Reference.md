# The Reference Manual of Funix 

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
