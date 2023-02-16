from typing import List 
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


# let's turn it into a web app via Funix 
from funix import funix 

@funix(
        widgets={
           "a": "sheet",
           "b": ["sheet", "slider[0,1,0.01]"]
        }
)


# below is a simple matplotlib function 
def table_plot(a: List[int], b: List[float]) -> Figure:
    fig = plt.figure()
    plt.plot(a, b)
    return fig
