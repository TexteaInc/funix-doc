# FIXME: The code bloe is not working 
from funix import funix
@funix(
    theme="./sunset_v2.yaml"
)
def hello(your_name: str) -> str:
    return f"Hello, {your_name}."


# FIXME: The code bloe is not working 
# from funix import funix_yaml
# @funix_yaml("""
#     theme: 
#         "https://yazawazi.moe/pdf_themes/sunset_v2.yaml"
#     """)
# def hello(your_name: str) -> str:
#     return f"Hello, {your_name}."


# FIXME: The code below is not working
# from funix import import_theme, funix_yaml

# import_theme("https://yazawazi.moe/pdf_themes/sunset_v2.yaml", name="sunset") # From URL 

# @funix_yaml("""theme: sunset""") # From name
# def hello(your_name: str) -> str:
#     return f"Hello, {your_name}."