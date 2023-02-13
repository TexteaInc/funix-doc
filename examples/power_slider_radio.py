from funix import funix

@funix(
    widgets={
        "x": "slider[0,10,1]",
        "op": "radio"
        }, 
    whitelist={"op": ["square", "cube"]},
    description="""
## Compute the power of a _number_. 
Two options: 
* Choose `op` as `square` to compute the square of `x`.
* Choose `op` as `cube` to compute the cube of `x`.

**Made with [Funix](http://funix.io)**"""
)

def power(x: int, op: str) -> int:
    if op =="square":
        return x * x
    elif op == "cube":
        return x * x * x