from funix import funix # add line one

@funix()                # add line two 
def hello(your_name: str) -> str:
    return f"Hi, {your_name}."
