#chess_knight.py

"""A program designed to help determine the average number of moves it takes for a 
knight starting in a corner and moving randomly to return to its starting corner. 
Uses Markov chains as the primary theoretical basis."""

import numpy as np
from scipy import linalg as la

"""The expected number of moves to get to the knight's original starting space from a 
given space is 1 plus the expected number of moves from the valid next spaces divided 
by the number of valid next spaces. Mathematically, we can write this as 
    E(i,j) = 1 + (sum(E(valid)))/N(valid).
The strategy is to write the expectation values as a system of equations, then solve 
for the expectation values of the various spaces using linear algebra."""

def matrix_maker():
    """Make a matrix representation of the system of equations, setting each equation 
    equal to -1. We use the convention that the knight's original corner is (1,1), 
    with other spaces ranging up to (8,8). The board is diagonally symmetric from the 
    knight's first space, so we only include rows for the upper half of the board (36 
    spaces total). Row 0 corresponds to (1,1), and we fill subsequent rows by 
    traversing the board row-wise."""
    #Initialize the matrix
    M = -np.eye(36)
    #(1,1)
    M[0,9] = 1
    #(1,2)
    M[1,[2,15,10]] = 1/3
    #(1,3)
    M[2,[1,9,11,16]] = 1/4
    #(1,4) to (1,6)
    indices = np.array([8, 12, 15, 17])
    for i, index in enumerate([3,4,5]):
        M[index,indices+i] = 1/4
    #(1,7)
    M[6,[11,18,20]] = 1/3
    #(1,8)
    M[7,[12,19]] = 1/2
    #(2,2)
    M[8,[3,16]] = 1/2
    #(2,3)
    M[9,[2,4,10,17,21]] = 1/6
    #(2,4)
    M[10,[1,5,9,16,18,22]] = 1/6
    #(2,5) and (2,6)
    indices = np.array([2, 6, 15, 19, 21, 23])
    for i, index in enumerate([11, 12]):
        M[index,indices+i] = 1/6
    #(2,7)
    M[13,[4,17,23,25]] = 1/4
    #(2,8)
    M[14,[5,24]] = 1/2
    #(3,3)
    M[15,[11,22]] = 1/2
    #(3,4)
    M[16,[2,4,8,10,12,17,23,26]] = 1/8
    #(3,5)
    M[17,[3,5,9,13,16,22,24,27]] = 1/8
    #(3,6)
    M[18,[4,6,10,14,21,25,26,28]] = 1/8
    #(3,7)
    M[19,[5,7,11,22,27,29]] = 1/6
    #(3,8)
    M[20,[6,12,23,28]] = 1/4
    #(4,4)
    M[21,[9,11,18,27]] = 1/4
    #(4,5)
    M[22,[10,12,15,17,19,23,28,30]] = 1/8
    #(4,6)
    M[23,[11,13,16,20,22,27,29,31]] = 1/8
    #(4,7)
    M[24,[12,14,17,26,30,32]] = 1/6
    #(4,8)
    M[25,[13,18,27,31]] = 1/4
    #(5,5)
    M[26,[16,18,24,31]] = 1/4
    #(5,6)
    M[27,[17,19,21,23,25,28,32,33]] = 1/8
    #(5,7)
    M[28,[18,20,22,27,31,34]] = 1/6
    #(5,8)
    M[29,[19,23,30,33]] = 1/4
    #(6,6)
    M[30,[22,24,29,34]] = 1/4
    #(6,7)
    M[31,[23,25,26,28,32,35]] = 1/6
    #(6,8)
    M[32,[24,27,31,34]] = 1/4
    #(7,7)
    M[33,[27,29]] = 1/2
    #(7,8)
    M[34,[28,30,32]] = 1/3
    #(8,8)
    M[35,31] = 1
    #Return the matrix
    return M

if __name__ == "__main__":
    #Find the inverse of the matrix, then solve for the expected number of moves
    inverse = la.inv(matrix_maker())
    constant = -np.ones(36)
    expectations = inverse@constant
    print(expectations)

