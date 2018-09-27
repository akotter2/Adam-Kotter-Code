# standard_library.py
"""Python Essentials: The Standard Library.
Adam Kotter
Gray/White Cohort
8/23/18
"""

import calculator
from itertools import combinations
from itertools import chain
import sys
import box
import random
import time

# Problem 1
def prob1(L):
    """Return the minimum, maximum, and average of the entries of L
    (in that order).
    """
    return (min(L), max(L), sum(L)/len(L))


# Problem 2
def prob2():
    """Determine which Python objects are mutable and which are immutable.
    Test numbers, strings, lists, tuples, and sets. Print your results.
    """
    mutable = list()
    immutable = list()
    int_1 = 1
    int_2 = int_1
    int_2 = 2
    if int_1 == int_2:
        mutable.append("int")
    else:
        immutable.append("int")
    str_1 = 'a'
    str_2 = str_1
    str_2 = 'b'
    if str_1 == str_2:
        mutable.append("str")
    else:
        immutable.append("str")
    list_1 = [1,2,3]
    list_2 = list_1
    list_2[2] = 2
    if list_1 == list_2:
        mutable.append("list")
    else:
        immutable.append("list")
    tuple_1 = (3,2,1)
    tuple_2 = tuple_1
    tuple_2 += (1,)
    if tuple_1 == tuple_2:
        mutable.append("tuple")
    else:
        immutable.append("tuple")
    set_1 = {"Cool","beans","bro"}
    set_2 = set_1
    set_2.remove("bro")
    set_2.add("broski")
    if set_1 == set_2:
        mutable.append("set")
    else:
        immutable.append("set")
    print("The following object types are mutable:", mutable)
    print("The following object types are immutable:", immutable)
    return


# Problem 3
def hypot(a, b):
    """Calculate and return the length of the hypotenuse of a right triangle.
    Do not use any functions other than those that are imported from your
    'calculator' module.

    Parameters:
        a: the length one of the sides of the triangle.
        b: the length the other non-hypotenuse side of the triangle.
    Returns:
        The length of the triangle's hypotenuse.
    """
    return calculator.sqrt(calculator.sum(calculator.product(a,a),calculator.product(b,b)))

# Problem 4
def power_set(A):
    """Use itertools to compute the power set of A.
    Parameters:
        A (iterable): a str, list, set, tuple, or other iterable collection.
    Returns:
        (list(sets)): The power set of A as a list of sets."""
    p_set = list()
    for i in range(0,len(A)+1):
        comb_list = list(combinations(A,i))
        for k in range(len(comb_list)):
            comb_list[k] = set(comb_list[k])
            p_set.append(comb_list[k])
    return p_set


# Problem 5: Implement shut the box.
def shut_the_box():
    """Plays a game of shut the box
    A player name and time limit in seconds must be entered in the command
    line when this file is executed to play this game."""
#Only output if exactly three command line arguments are entered.
    if len(sys.argv) != 3:
        return
#Get the time limit and player name
    time_limit = float(sys.argv[2])
    name = sys.argv[1]
#Print instructions, wait for them to be read
    print("Objective:\nGet the lowest score possible in the alloted time.")
    print("Instructioms:") 
    print("Two dice are rolled each round. You must eliminate numbers from the box whose sum is equal to the numbers rolled on the dice. Enter the numbers to be eliminated with only one space of separation between each number. Your score is the sum of the remaining numbers in the box.") 
    print("You only have", time_limit, "seconds to play.")
    input_ready = input("Are you ready? ")
    if input_ready.lower() == "no" or input_ready.lower() == "n":
        input_sure = input("Are you sure? ")
        if input_sure.lower() == "yes" or input_sure.lower() == "y":
            print("Awww...")
            print("Game over before it even begins.")
            return
#Make the list of numbers to remove
    num_left = list(range(1,10))
#Get start time
    start_time = time.time()
    current_time = start_time
    end_time = start_time + time_limit
#Keep going until time runs out or the player wins
    while current_time < end_time:
#Print remaining numbers
        print("\nNumbers left: ", num_left)
#Get and print rolls
        if sum(num_left) <= 6:
            roll = random.randint(1,6)
        else:
            roll = random.randint(1,6) + random.randint(1,6)
        print("Roll:", roll)
#Check possibility of matching roll
        if not box.isvalid(roll,num_left):
            print("\nImpossible roll. So sorry!")
            print("Game over!")
            print("Score for player", name + ":", sum(num_left), "points")
            print("Time played: ", round(current_time - start_time,2), "seconds")
            print("Better luck next time ;)")
            return
#Get and print the time
        current_time = time.time()
        print("Seconds left", round(end_time - current_time,2))
#Get the numbers to eliminate, responding to input appropriately
        while True:
            input_str = input("Numbers to eliminate: ")
            num_elim = box.parse_input(input_str, num_left)
            if sum(num_elim) != roll:
                print("\nInvalid input")
                current_time = time.time()
                print("Seconds left:", round(end_time - current_time,2))
                continue
            else:
                break
#Get rid of numbers to eliminate
        for number in num_elim:
            num_left.remove(number)
        current_time = time.time()
#Success or failure?
        if num_left == []:
            print("Score for player", name + ": 0 points")
            print("Time played:", round(current_time - start_time,2), "seconds")
            print("Hooray! You shut the box!")
            return
    print("\nTime's up! Game over!")
    print("Score for player", name + ":", sum(num_left), "points")
    print("Time played: ", round(current_time - start_time,2), "seconds")
    print("Better luck next time ;)")
    return


#Testing:
if __name__ == "__main__":
   """ print(prob1([1,2,3,4,5]))
    print(prob1([0,0,0,1]))
    prob2()
    print(hypot(3,4))
    print(hypot(1,1))
    print(power_set('abc'))
    print(power_set(["A","A","A"]))"""
    if len(sys.argv) == 3:
        shut_the_box()