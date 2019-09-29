#biology_life.py
"""Models reproductive fitness given choices for investment of energy."""

import numpy as np




if __name__ == "__main__":
    #Begin
    print("Basic Biology Simulator")
    print("The objective here is to have as many offspring as possible in your " + 
           "lifespan.")
    energy_per_turn = 1
    week = 1
    maintenance = 0.5
    children = 0
    #Repeat until the end
    done = False
    while not done:
        #Display energy points and maintenance requirements
        print("This week's energy allotment: " + str(energy_per_turn))
        print("This week's maintenance requirements: " + str(maintenance))
        print("Effective energy allotment: " + str(energy_per_turn - maintenance))
        #Give options for growth and reproduction
        growth = input("How much energy would you like to invest in growth?")
        offspring = input("How much energy would you like to invest in reproducing?")
        if growth + offspring > energy_per_turn:
            print("You only get " + str(energy_per_turn) + " energy per week.")
            continue
        energy_per_turn += growth
        children += offspring
        week += 1
        if week >= 11:
            done = True
    print("Week: " + str(week))
    print("Offspring: " + str(children))
        
        
    