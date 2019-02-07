# matplotlib_intro.py
"""Python Essentials: Intro to Matplotlib.
Adam Kotter
Math 321 - 1
8/29/18
"""

import numpy as np
from matplotlib import pyplot as plt

# Problem 1
def var_of_means(n):
    """Construct a random matrix A with values drawn from the standard normal
    distribution. Calculate the mean value of each row, then calculate the
    variance of these means. Return the variance.

    Parameters:
        n (int): The number of rows and columns in the matrix A.

    Returns:
        (float) The variance of the means of each row.
    """
    A = np.random.normal(size=(n,n))
    Means = np.mean(A, axis=1)
    return np.var(Means)

def prob1():
    """Create an array of the results of var_of_means() with inputs
    n = 100, 200, ..., 1000. Plot and show the resulting array.
    """
    Var = np.array(var_of_means(100))
    for m in range(200,1001,100):
        Var = np.hstack((Var,var_of_means(m)))
    x = np.arange(100,1001,100)
    plt.plot(x,Var)
    plt.show()
    return


# Problem 2
def prob2():
    """Plot the functions sin(x), cos(x), and arctan(x) on the domain
    [-2pi, 2pi]. Make sure the domain is refined enough to produce a figure
    with good resolution.
    """
    x = np.linspace(-2*np.pi,2*np.pi,100)
    plt.plot(x,np.sin(x))
    plt.plot(x,np.cos(x))
    plt.plot(x,np.arctan(x))
    plt.show()
    return


# Problem 3
def prob3():
    """Plot the curve f(x) = 1/(x-1) on the domain [-2,6].
        1. Split the domain so that the curve looks discontinuous.
        2. Plot both curves with a thick, dashed magenta line.
        3. Set the range of the x-axis to [-2,6] and the range of the
           y-axis to [-6,6].
    """
    x_left = np.linspace(-2,1,40)
    x_right = np.linspace(1,6,60)
    plt.plot(x_left,1/(x_left-1),"m--", linewidth = 4)
    plt.plot(x_right,1/(x_right-1),"m--", linewidth = 4)
    plt.xlim(-2,6)
    plt.ylim(-6,6)
    plt.show()
    return


# Problem 4
def prob4():
    """Plot the functions sin(x), sin(2x), 2sin(x), and 2sin(2x) on the
    domain [0, 2pi].
        1. Arrange the plots in a square grid of four subplots.
        2. Set the limits of each subplot to [0, 2pi]x[-2, 2].
        3. Give each subplot an appropriate title.
        4. Give the overall figure a title.
        5. Use the following line colors and styles.
              sin(x): green solid line.
             sin(2x): red dashed line.
             2sin(x): blue dashed line.
            2sin(2x): magenta dotted line.
    """
    x = np.linspace(0,2*np.pi,100)
    y1 = np.sin(x)
    y2 = np.sin(2*x)
    y3 = 2*np.sin(x)
    y4 = 2*np.sin(2*x)
    plt.subplot(221)
    plt.plot(x,y1,"g-")
    plt.title("sin(x)")
    plt.axis([0,2*np.pi,-2,2])
    plt.subplot(222)
    plt.plot(x,y2,"r--")
    plt.title("sin(2x)")
    plt.axis([0,2*np.pi,-2,2])
    plt.subplot(223)
    plt.plot(x,y3,"b--")
    plt.title("2sin(x)")
    plt.axis([0,2*np.pi,-2,2])
    plt.subplot(224)
    plt.plot(x,y4,"m:")
    plt.title("2sin(2x)")
    plt.axis([0,2*np.pi,-2,2])
    plt.suptitle("Sine Functions")
    plt.show()
    return


# Problem 5
def prob5():
    """Visualize the data in FARS.npy. Use np.load() to load the data, then
    create a single figure with two subplots:
        1. A scatter plot of longitudes against latitudes. Because of the
            large number of data points, use black pixel markers (use "k,"
            as the third argument to plt.plot()). Label both axes.
        2. A histogram of the hours of the day, with one bin per hour.
            Label and set the limits of the x-axis.
    """
    FARS = np.load("FARS.npy")
    long = FARS[:,1]
    lat = FARS[:,2]
    plt.subplot(121)
    plt.plot(long,lat,"k,")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.axis("equal")
    plt.subplot(122)
    plt.hist(FARS[:,0], bins=np.arange(0,25))
    plt.xlabel("Time of day")
    plt.suptitle("US Traffic Accidents")
    plt.show()
    return


# Problem 6
def prob6():
    """Plot the function f(x,y) = sin(x)sin(y)/xy on the domain
    [-2pi, 2pi]x[-2pi, 2pi].
        1. Create 2 subplots: one with a heat map of f, and one with a contour
            map of f. Choose an appropriate number of level curves, or specify
            the curves yourself.
        2. Set the limits of each subplot to [-2pi, 2pi]x[-2pi, 2pi].
        3. Choose a non-default color scheme.
        4. Add a colorbar to each subplot.
    """
    x = np.linspace(-2*np.pi,2*np.pi,100)
    y = np.linspace(-2*np.pi,2*np.pi,100)
    X,Y = np.meshgrid(x,y)
    Z = (np.sin(X)*np.sin(Y))/(X*Y)
    plt.subplot(121)
    plt.pcolormesh(X,Y,Z,cmap="hot")
    plt.colorbar()
    plt.axis([-2*np.pi,2*np.pi,-2*np.pi,2*np.pi])
    plt.subplot(122)
    plt.contour(X,Y,Z,np.hstack([np.linspace(-0.25,-0.001,10),np.linspace(0,1,10)]),cmap="plasma")
    plt.colorbar()
    plt.axis([-2*np.pi,2*np.pi,-2*np.pi,2*np.pi])
    plt.suptitle("Plot of (sin(x)(sin)y)/(xy)")
    plt.show()
    return

if __name__ == "__main__":
    prob1()
    prob2()
    prob3()
    prob4()
    prob5()
    prob6()