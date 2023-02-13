
from funix.hint import Markdown

## If decorating in Python's syntax, 
## use the following:
# from funix import funix
# @funix(
#     widgets={
#         "x": "slider[0,10,1]",
#         "op": "radio"
#         }, 
#     whitelist={"op": ["square", "cube"]}
# )

## If decorating in YAML syntax,
## use the following:
# from funix import funix_yaml
# @funix_yaml("""
#     widgets:
#         x: slider[0,10,1]
#         op: radio
#     whitelist:
#         op: 
#             - square
#             - cube
# """
# )
            
## If decorating in JSON5 syntax,
## use the following:
from funix import funix_json5
@funix_json5("""
{
    widgets: {
        x: "slider[0,10,1]",
        op: "radio" } , 
    whitelist: {
        op: ["square", "cube"] } 
}
"""
)

def power(x: int, op: str) -> Markdown:
    if op =="square":
        return  f"\
* The _square_ of {x} is **{x * x}**. \n \
* Made by [Funix](http://funix.io)"
    elif op == "cube":
        # return x * x * x
        return  f"\
* The _cube_ of {x} is **{x * x * x}**. \n \
* Made by [Funix](http://funix.io)"
    



# description="""
# ## Compute the power of a _number_. 
# Two options: 
# * Choose `op` as `square` to compute the square of `x`.
# * Choose `op` as `cube` to compute the cube of `x`.

# **Made with [Funix](http://funix.io)**"""