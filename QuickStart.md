# The Quick Start Guide of Funix 

Your Python function definition is your web app! 

* Simple and quick: Funix turns your Python function into a web app in as few as two lines of code. 
* For whom: Python engineers who want to bring their code to the web but do not want to bother anything front-end or GUI, not even creating widgets in Python. 
* Funix vs. them: You don't even need to choose widgets in Python. Just write your core logic. 
* How: Funix automatically chooses I/O widgets for your web app by analyzing your code.
* Customizable: Tune the UI, when you want to, declaratively in Python, YAML, and JSON. 
* Theming supported, and u
* Open source under the MIT license.

## Build a web app from a Python function

```python
from funix import funix

@funix_yaml()
def hello_world(your_name: str) -> str:
    return f"Welcome to Funix, {your_name}."
``` 

