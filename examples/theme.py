from funix import funix


@funix(theme="./sunset_v3.json")
def hello(your_name: str) -> str:
    return f"Hello, {your_name}."
