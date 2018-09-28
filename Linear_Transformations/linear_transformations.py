# linear_transformations.py
"""Volume 1: Linear Transformations.
Adam Kotter
Math 345 - 1
9-25-18
"""

from random import random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
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


#Linear Transformations:
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


def solar_system(T, x_e, x_m, omega_e, omega_m, plot=True):
    """Plot the trajectories of the earth and moon over the time interval [0,T]
    assuming the initial position of the earth is (x_e,0) and the initial
    position of the moon is (x_m,0). Calculates trajectory over 1000 steps.

    Parameters:
        T (int): The final time.
        x_e (float): The earth's initial x coordinate.
        x_m (float): The moon's initial x coordinate.
        omega_e (float): The earth's angular velocity.
        omega_m (float): The moon's angular velocity.
        plot (boolean): Whether to print the plot or return the trajectory coordinates
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
    if plot == True:
        plt.plot(p_et[0], p_et[1], "b-")
        plt.plot(p_mt[0], p_mt[1], "r-")
        plt.gca().set_aspect("equal")
        plt.show()
    #Return the position vectors
    else:
        return (p_et, p_mt)


def solar_system_animation(T, x_e, x_m, omega_e, omega_m):
    """Plot the trajectories of the earth and moon over the time interval [0,T]
    assuming the initial position of the earth is (x_e,0) and the initial
    position of the moon is (x_m,0). Calculates and animates trajectories over 1000
    frames.

    Parameters:
        T (int): The final time.
        x_e (float): The earth's initial x coordinate.
        x_m (float): The moon's initial x coordinate.
        omega_e (float): The earth's angular velocity.
        omega_m (float): The moon's angular velocity."""
    (earth, moon) = solar_system(T, x_e, x_m, omega_e, omega_m, False)
    # Make a figure explicitly.
    fig, ax = plt.subplots(1,1)
    # Set the window limits.
    plt.axis([-1.1*(x_m),1.1*(x_m),-1.1*(x_m),1.1*(x_m)])
    # Make the window square.
    ax.set_aspect("equal")
    # Blue dot for the earth.
    earth_dot, = ax.plot([],[], 'C0o', ms=10)
    # Blue line for the earth.
    earth_path, = ax.plot([],[], 'C0-')
    # Green dot for the moon.
    moon_dot, = ax.plot([],[], 'C2o', ms=5)
    # Green line for the moon.
    moon_path, = ax.plot([],[], 'C2-')
    # Yellow dot for the sun.
    ax.plot([0],[0],'yo', ms=20)
    def animate(index):
        earth_dot.set_data(earth[0,index], earth[1,index])
        earth_path.set_data(earth[0,:index], earth[1,:index])
        moon_dot.set_data(moon[0,index], moon[1,index])
        moon_path.set_data(moon[0,:index], moon[1,:index])
        return earth_dot, earth_path, moon_dot, moon_path,
    a = FuncAnimation(fig, animate, frames=earth.shape[1], interval=25)
    plt.show()

    
#Creating and timing multiplication of random vectors and matrices
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


def timing():
    """Uses time.time() to time matrix_vector_product() and matrix-matrix-mult() 
    with increasingly large inputs. Generates the inputs A, x, and B with 
    random_matrix() and random_vector() (so each input will be nxn or nx1).
    Only time the multiplication functions, not the generating functions.
    Reports findings in a single figure with two subplots: one with matrix-
    vector times, and one with matrix-matrix times.
    """

    #Initialize lists of times
    times_m = []
    times_v = []
    #Repeat eight times
    for n in range(1,9):
        #Generate inputs
        A = random_matrix(2**n)
        B = random_matrix(2**n)
        x = random_vector(2**n)
        #Time matrix-matrix multiplication
        start_m = time.time()
        matrix_matrix_product(A,B)
        end_m = time.time()
        #Time matrix-vector multiplication
        start_v = time.time()
        matrix_vector_product(A,x)
        end_v = time.time()
        #Enter times in lists
        times_m.append(end_m - start_m)
        times_v.append(end_v - start_v)
    #Plot results
    n_list = [2**n for n in range(1,len(times_v)+1)]
    plt.subplot(121)
    plt.title("Matrix-Vector Multiplication")
    plt.plot(n_list, times_v, "b.-")
    plt.xlabel("n")
    plt.ylabel("Seconds")
    plt.subplot(122)
    plt.title("Matrix-Matrix Multiplication")
    plt.plot(n_list, times_m, "g.-")
    plt.xlabel("n")
    plt.ylabel("Seconds")
    plt.show()


def np_timing():
    """Times matrix_vector_product(), matrix_matrix_product(), and np.dot().
    Report findings in a single figure with two subplots: one with all four sets 
    of execution times on a regular linear scale, and one with all four sets of 
    exections times on a log-log scale.
    """

    #Initialize lists of times
    times_m_np = []
    times_v_np = []
    times_m = []
    times_v = []
    #Repeat nine times
    for n in range(1,10):
        #Generate normal Python inputs
        A1 = random_matrix(2**n)
        B1 = random_matrix(2**n)
        x1 = random_vector(2**n)
        #Generate NumPy inputs
        A2 = np.array(random_matrix(2**n))
        B2 = np.array(random_matrix(2**n))
        x2 = np.array(random_vector(2**n))
        #Time normal matrix-matrix multiplication
        start_m = time.time()
        matrix_matrix_product(A1,B1)
        end_m = time.time()
        #Time normal matrix-vector multiplication
        start_v = time.time()
        matrix_vector_product(A1,x1)
        end_v = time.time()
        #Time NumPy matrix-matrix multiplication
        start_m_np = time.time()
        A2@B2
        end_m_np = time.time()
        #Time NumPy matrix-vector multiplication
        start_v_np = time.time()
        A2@x2
        end_v_np = time.time()
        #Enter times in lists
        times_m.append(end_m - start_m)
        times_v.append(end_v - start_v)
        times_m_np.append(end_m_np - start_m_np)
        times_v_np.append(end_v_np - start_v_np)
    #Plot results
    n_list = [2**n for n in range(1,len(times_v)+1)]
    plt.subplot(121)
    plt.title("Linear Scale")
    plt.plot(n_list, times_m, "b.-", label="Normal Matrix-Matrix")
    plt.plot(n_list, times_m_np, "r.-", label="NumPy Matrix-Matrix")
    plt.plot(n_list, times_v, "g.-", label="Normal Matrix-Vector")
    plt.plot(n_list, times_v_np, "y.-", label="NumPy Matrix-Vector")
    plt.legend(loc="upper left")
    plt.xlabel("n")
    plt.ylabel("Seconds")
    plt.subplot(122)
    plt.title("Log Scale")
    plt.loglog(n_list, times_m, "b.-", label="Normal Matrix-Matrix", basex=2, basey=2)
    plt.loglog(n_list, times_m_np, "r.-", label="NumPy Matrix-Matrix", basex=2, basey=2)
    plt.loglog(n_list, times_v, "g.-", label="Normal Matrix-Vector", basex=2, basey=2)
    plt.loglog(n_list, times_v_np, "y.-", label="NumPy Matrix-Vector", basex=2, basey=2)
    plt.legend(loc="upper left")
    plt.xlabel("n")
    plt.ylabel("Seconds")
    plt.show()
    
    
#For testing purposes
if __name__ == "__main__":
    #test_plot("horse.npy")
    #solar_system(np.pi*2, 400, 401, 1, 13)
    #prob3()
    solar_system_animation(np.pi*2, 10, 11, 1, 13)