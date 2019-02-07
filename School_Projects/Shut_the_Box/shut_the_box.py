# shut_the_box.py
"""
Adam Kotter
Math 321 - 1
8/23/18
"""

import sys
import box
import random
import time

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
    if len(sys.argv) == 3:
        shut_the_box()