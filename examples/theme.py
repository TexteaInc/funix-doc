# from funix import funix

# @funix(
#     theme="./sunset_v2.yaml"
# )
# def hello(your_name: str) -> str:
#     return f"Hello, {your_name}."


from funix import funix_yaml
@funix_yaml("""
    theme: 
        "https://raw.githubusercontent.com/TexteaInc/funix-doc/main/examples/sunset_v2.yaml"
    """)
def hello(your_name: str) -> str:
    return f"Hello, {your_name}."

