# linear_transformations.py
"""Volume 1: Linear Transformations.
Adam Kotter
Math 345 - 1
9-25-18
"""

from random import random
import numpy as np
from matplotlib import pyplot as plt
import time


def test_plot(file):
    """Takes in a .npy file to use as a reference image, then performs and plots various 
    linear transformations on the reference image."""
    #Get the image
    data = np.load(file)
    plt.subplot(231)
    plt.title("Original")
    plt.plot(data[0], data[1], "k,")
    plt.axis([-1,1,-1,1])
    plt.subplot(232)
    plt.title("Stretch")
    data_stretch = stretch(data, 0.5, 2)
    plt.plot(data_stretch[0], data_stretch[1], "k,")
    plt.axis([-1,1,-1,1])
    plt.subplot(233)
    plt.title("Shear")
    data_shear = shear(data, 0.5, 1)
    plt.plot(data_shear[0], data_shear[1], "k,")
    plt.axis([-1,1,-1,1])
    plt.subplot(234)
    plt.title("Reflect")
    data_reflect = reflect(data, 0.5, 2)
    plt.plot(data_reflect[0], data_reflect[1], "k,")
    plt.axis([-1,1,-1,1])
    plt.subplot(235)
    plt.title("Rotate")
    data_rotate = rotate(data, np.pi)
    plt.plot(data_rotate[0], data_rotate[1], "k,")
    plt.axis([-1,1,-1,1])
    plt.subplot(236)
    plt.title("Composite")
    data_weird = rotate(reflect(shear(stretch(data, 0.5, 2), 0.5, 1), 0.5, 2), 2)
    plt.plot(data_weird[0], data_weird[1], "k,")
    plt.axis([-1,1,-1,1])
    plt.suptitle("Horses")
    plt.gca().set_aspect("equal")
    plt.show()

# Problem 1
def stretch(A, a, b):
    """Scale the points in A by a in the x direction and b in the
    y direction.

    Parameters:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        a (float): scaling factor in the x direction.
        b (float): scaling factor in the y direction.
    """
    #The matrix for a stretch linear transformation
    M = np.array([[a,0],[0,b]])
    return M@A

def shear(A, a, b):
    """Slant the points in A by a in the x direction and b in the
    y direction.

    Parameters:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        a (float): scaling factor in the x direction.
        b (float): scaling factor in the y direction.
    """
    #The matrix for a shear linear transformation
    M = np.array([[1,a],[b,1]])
    return M@A

def reflect(A, a, b):
    """Reflect the points in A about the line that passes through the origin
    and the point (a,b).

    Parameters:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        a (float): x-coordinate of a point on the reflecting line.
        b (float): y-coordinate of the same point on the reflecting line.
    """
    #The matrix for a reflection linear transformation
    M = np.array([[a**2 - b**2, 2*a*b],[2*a*b, b**2 - a**2]])
    return (1/(a**2 + b**2))*M@A

def rotate(A, theta):
    """Rotate the points in A about the origin by theta radians.

    Parameters:
        A ((2,n) ndarray): Array containing points in R2 stored as columns.
        theta (float): The rotation angle in radians.
    """
    #The matrix for a rotation linear transformation
    M = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])
    return M@A


# Problem 2
def solar_system(T, x_e, x_m, omega_e, omega_m):
    """Plot the trajectories of the earth and moon over the time interval [0,T]
    assuming the initial position of the earth is (x_e,0) and the initial
    position of the moon is (x_m,0). Calculates trajectory over 1000 steps.

    Parameters:
        T (int): The final time.
        x_e (float): The earth's initial x coordinate.
        x_m (float): The moon's initial x coordinate.
        omega_e (float): The earth's angular velocity.
        omega_m (float): The moon's angular velocity.
    """
    #Set p_e0 (earth's initial position) and p_m0 (moon's initial position)
    p_e0 = np.array([x_e, 0])
    p_m0 = np.array([x_m, 0])
    #Initialize p_et (earth's position at time t) and p_mt (moon's position at time t)
    p_et = np.zeros([2,1000])
    p_mt = np.zeros([2,1000])
    #Initialize indices as 0
    t = 0
    i = 0
    #Get earth's absolute position by rotating p_e0 by omega_e times t 1000 times
    while i < 1000:
        p_et[0,i] = rotate(p_e0, omega_e*t)[0]
        p_et[1,i] = rotate(p_e0, omega_e*t)[1]
        t += (T/1000)
        i += 1
    #Reinitialize indices as 0
    t = 0
    i = 0
    #Get moon's relative position by rotating p_m0 - p_e0 by omega_m times t 1000 times
    p_mtemp = p_m0 - p_e0
    while i < 1000:
        p_mt[0,i] = rotate(p_mtemp, omega_m*t)[0]
        p_mt[1,i] = rotate(p_mtemp, omega_m*t)[1]
        t += (T/1000)
        i += 1    #Reinitialize indices as 0
    t = 0
    i = 0
    #Get moon's absolute position by translating the previous matrix by p_et
    while i < 1000:
        p_mt[0,i] = p_mt[0,i] + p_et[0,i]
        p_mt[1,i] = p_mt[1,i] + p_et[1,i]
        t += (T/1000)
        i += 1
    #Plot the orbits
    plt.plot(p_et[0], p_et[1], "b-")
    plt.plot(p_mt[0], p_mt[1], "r-")
    plt.gca().set_aspect("equal")
    plt.show()


def random_vector(n):
    """Generate a random vector of length n as a list."""
    return [random() for i in range(n)]

def random_matrix(n):
    """Generate a random nxn matrix as a list of lists."""
    return [[random() for j in range(n)] for i in range(n)]

def matrix_vector_product(A, x):
    """Compute the matrix-vector product Ax as a list."""
    m, n = len(A), len(x)
    return [sum([A[i][k] * x[k] for k in range(n)]) for i in range(m)]

def matrix_matrix_product(A, B):
    """Compute the matrix-matrix product AB as a list of lists."""
    m, n, p = len(A), len(B), len(B[0])
    return [[sum([A[i][k] * B[k][j] for k in range(n)])
                                    for j in range(p) ]
                                    for i in range(m) ]

# Problem 3
def prob3():
    """Use time.time(), timeit.timeit(), or %timeit to time
    matrix_vector_product() and matrix-matrix-mult() with increasingly large
    inputs. Generate the inputs A, x, and B with random_matrix() and
    random_vector() (so each input will be nxn or nx1).
    Only time the multiplication functions, not the generating functions.

    Report your findings in a single figure with two subplots: one with matrix-
    vector times, and one with matrix-matrix times. Choose a domain for n so
    that your figure accurately describes the growth, but avoid values of n
    that lead to execution times of more than 1 minute.
    """
    #Generate inputs
    #Time matrix-vector multiplication
    #Time matrix-matrix multiplication
    #Plot results
    plt.subplot(121)
    plt.title("Matrix-Vector Multiplication")
    plt.plot(domain, times, "b.-")
    plt.xlabel("n")
    plt.ylabel("Seconds")
    plt.subplot(122)
    plt.title("Matrix-Matrix Multiplication")
    plt.plot(domain, times, "g.-")
    plt.xlabel("n")
    plt.ylabel("Seconds")
    plt.show
    raise NotImplementedError("Problem 3 Incomplete")


# Problem 4
def prob4():
    """Time matrix_vector_product(), matrix_matrix_product(), and np.dot().

    Report your findings in a single figure with two subplots: one with all
    four sets of execution times on a regular linear scale, and one with all
    four sets of exections times on a log-log scale.
    """
    raise NotImplementedError("Problem 4 Incomplete")

if __name__ == "__main__":
    #test_plot("horse.npy")
    solar_system(np.pi*2, 400, 401, 1, 13)