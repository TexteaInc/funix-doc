from funix import funix

@funix(
)
def hello(name: str) -> str:
    return f"Hi, {name}."






# from funix import funix , set_theme_yaml, set_default_theme 


# slider_int = int

# set_theme_yaml("""
#     types: 
#         int: slider 
#         slider_int: slider 

# """, "test")

# set_default_theme('test')


# @funix(
#         widgets={"x":"slider[0,100,2]"}
# )


# @funix(
#     theme="https://github.com/TexteaInc/funix/blob/main/examples/sunset_v2.yaml"
# )



# Script 
# 1. Hello
# 2. Widget choices are associated with types for consistent appearances and isolate Python data developers from frontend matters.
# 3. Change the theme in a snap. 
# 4. Local customization Declaratively
# 4. AI, the worlds shortest chat GPT program 
# 5. table and plot 
# 6. customize new type on the fly 
