#complex_visualizer.py
"""Contains a function for visualizing complex-valued functions."""

from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np


def plot_complex(f, window=[-1, 1, -1, 1], res=400, title=""):
    """Visualize the complex-valued function f:C->C on the (res x res) domain
    {a + bi | a in [r_min, r_max], b in [i_min, i_max]} by plotting the
    argument of f(z) and the magnitude of f(z) in separate subplots.
    
    Parameters:
        f (func): A function that accepts and returns arrays with complex entries.
        window ([r_min, r_max, i_min, i_max]): The real and imaginary domain bounds.
        res (int): The plot resolution. The domain should be res x res.
        title (str): A label for the function to set as the figure title.
            Use r"$<latex code>$" for pretty printing. For example, for the function
            f = lambda z: z**2 - np.sqrt(z), use title=r"$f(z) = z^2 - \sqrt{z}$".
    """
    #Set up domain
    x = np.linspace(window[0], window[1], res)
    y = np.linspace(window[2], window[3], res)
    X, Y = np.meshgrid(x, y)
    Z = X + Y*1j
    #Evaluate the function on the domain
    ans = f(Z)
    #Plot arg(f(z))
    fig = plt.figure()
    plt.suptitle(title, fontsize=8)
    ax = fig.add_subplot(121, aspect="equal")
    ax.pcolormesh(np.angle(ans), cmap="hsv", vmin=-np.pi, vmax=np.pi)
    plt.title("Angle plot of " + title, fontsize=6)
    plt.axis("off")
    #Plot |f(z)|
    ax = fig.add_subplot(122, aspect="equal")
    ax.pcolormesh(np.abs(ans), cmap="magma", norm=LogNorm())
    plt.title("Magnitude plot of " + title, fontsize=6)
    plt.axis("off")
    plt.show()