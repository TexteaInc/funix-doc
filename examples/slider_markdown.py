from funix import funix

@funix(
    widgets={"x": "slider[0,10,1]"}, 
    description="**Square** a _number_. Made with [Funix](http://funix.io)" 
)
def square(x: int) -> int:
    return x * x
