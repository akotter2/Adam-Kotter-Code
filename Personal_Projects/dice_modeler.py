#dice_modeler.py

"""Shows a graph of the statistical probabilities of rolling certain amounts using 
different combinations of dice."""

import numpy as np
from matplotlib import pyplot as plt

def default():
    """Models rolls of dice without any special rules."""
    #Initialize variables
    one_in_bag = False
    #Add one die to start
    while not one_in_bag:
        dice_bag = [input("How many sides on the first die? ")]
        if not dice_bag[0].isdigit():
            print("Die must have an integer number of sides!")
        else:
            one_in_bag = True
            dice_bag[0] = int(dice_bag[0])
    #Add more dice until a non-integer is entered
    last_die = False
    while not last_die:
        next_die = input("How many sides on the next die? If not applicable, 'N'. ")
        if next_die.isdigit():
            dice_bag.append(int(next_die))
        else:
            last_die = True
    #Roll each die 1e6 times, adding the results of each die for each roll
        num_dice = len(dice_bag)
        rolls = np.zeros(int(1e6))
        for i in range(num_dice):
            rolls += np.random.randint(1, dice_bag[i]+1, int(1e6))
    #Show the results
    max_roll = sum(dice_bag)
    plt.title("Probability per Result")
    plt.ylabel("Probability")
    plt.xlabel("Result")
    plt.xticks(np.linspace(0,max_roll+1,max_roll+2))
    plt.hist(rolls, bins=np.linspace(0, max_roll+1, max_roll+2), density=True)
    plt.show()

def top_dice():
    """Models rolls of one kind of die where only the top few dice count."""
    #Initialize variables
    has_num_sides = False
    #Set number of sides
    while not has_num_sides:
        num_sides = input("How many sides on these dice? ")
        if not num_sides.isdigit():
            print("Dice must have an integer number of sides!")
        else:
            has_num_sides = True
            num_sides = int(num_sides)
    #Set number of dice
    has_num_dice = False
    while not has_num_dice:
        num_dice = input("How many dice? ")
        if not num_dice.isdigit():
            print("There must be an integer number of dice!")
        else:
            has_num_dice = True
            num_dice = int(num_dice)
    #Set number of dice to keep
    has_num_keep = False
    while not has_num_keep:
        num_keep = input("How many dice to keep? ")
        if not num_keep.isdigit():
            print("There must be an integer number of dice to keep!")
        else:
            has_num_keep = True
            num_keep = int(num_keep)
    #Roll each die 1e6 times, adding the results of the top dice for each roll
        rolls = np.random.randint(1, num_sides+1, size=(num_dice, int(1e6)))
        sums = np.zeros(int(1e6))
        list_ints = np.arange(0, int(1e6))
        for i in range(num_keep):
            sums += np.max(rolls, axis=0)
            argmaxes = np.argmax(rolls, axis=0)
            rolls[(argmaxes, list_ints)] = 0
    #Show the results
    max_roll = np.max(sums)
    plt.title("Probability per Result")
    plt.ylabel("Probability")
    plt.xlabel("Result")
    plt.xticks(np.linspace(0,max_roll+1,max_roll+2))
    plt.hist(sums, bins=np.linspace(0, max_roll+1, max_roll+2), density=True)
    plt.show()

def bottom_dice():
    """Models rolls of one kind of die where only the bottom few dice count.."""
    #Initialize variables
    has_num_sides = False
    #Set number of sides
    while not has_num_sides:
        num_sides = input("How many sides on these dice? ")
        if not num_sides.isdigit():
            print("Dice must have an integer number of sides!")
        else:
            has_num_sides = True
            num_sides = int(num_sides)
    #Set number of dice
    has_num_dice = False
    while not has_num_dice:
        num_dice = input("How many dice? ")
        if not num_dice.isdigit():
            print("There must be an integer number of dice!")
        else:
            has_num_dice = True
            num_dice = int(num_dice)
    #Set number of dice to keep
    has_num_keep = False
    while not has_num_keep:
        num_keep = input("How many dice to keep? ")
        if not num_keep.isdigit():
            print("There must be an integer number of dice to keep!")
        else:
            has_num_keep = True
            num_keep = int(num_keep)
    #Roll each die 1e6 times, adding the results of the top dice for each roll
        rolls = np.random.randint(1, num_sides+1, size=(num_dice, int(1e6)))
        sums = np.zeros(int(1e6))
        list_ints = np.arange(0, int(1e6))
        for i in range(num_keep):
            sums += np.min(rolls, axis=0)
            argmins = np.argmin(rolls, axis=0)
            rolls[(argmins, list_ints)] = num_sides*num_dice*1000
    #Show the results
    max_roll = np.max(sums)
    plt.title("Probability per Result")
    plt.ylabel("Probability")
    plt.xlabel("Result")
    plt.xticks(np.linspace(0,max_roll+1,max_roll+2))
    plt.hist(sums, bins=np.linspace(0, max_roll+1, max_roll+2), density=True)
    plt.show()

if __name__ == "__main__":
    #Pick which way to roll the dice
    choice = input("Normal (N), top few (T), or bottom few (B)? ")
    if choice == "N":
        default()
    if choice == "T":
        top_dice()
    if choice == "B":
        bottom_dice()
