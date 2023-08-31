from funix import funix

@funix()
def foo(x: int) -> int:
    return x + 1

def bar(x: int) -> int:
    return x + 2

@funix()
def foobar(x: int) -> int:
    return foo(x) + bar(x)

if __name__ == "__main__":
    print(foobar(1))
