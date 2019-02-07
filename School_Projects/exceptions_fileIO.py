# exceptions_fileIO.py
"""Python Essentials: Exceptions and File Input/Output.
Adam Kotter
White/Gray Cohort
8/30/18
"""

from random import choice
import numpy as np


# Problem 1
def arithmagic():
    """Performs a "magic" trick with arithmetic, raising errors if done incorrectly"""
    #Get first input
    step_1 = input("Enter a 3-digit number where the first and last "
                                           "digits differ by 2 or more: ")
    #Check errors on step 1
    if len(step_1) != 3:
        raise ValueError("Entered number not three digits!")
    if abs(int(step_1[2]) - int(step_1[0])) < 2:
        raise ValueError("Entered number's first and last digits differ by less than 2!")
    #Get second input
    step_2 = input("Enter the reverse of the first number, obtained "
                                              "by reading it backwards: ")
    #Check errors on step 2
    if step_2[::-1] != step_1:
        raise ValueError("Entered number not the reverse of first number!")
    #Get third input
    step_3 = input("Enter the positive difference of these numbers: ")
    #Check errors on step 3
    if int(step_3) != abs(int(step_1)-int(step_2)):
        raise ValueError("Entered number not the positive difference of the first two numbers")
    #Get last input
    step_4 = input("Enter the reverse of the previous result: ")
    #Check errors on step 4
    if step_4[::-1] != step_3:
        raise ValueError("Entered number not the reverse of third number!")
    #Print magic trick
    print(str(step_3), "+", str(step_4), "= 1089 (ta-da!)")


# Problem 2
def random_walk(max_iters=1e12):
    """Randomly increments or decrements the walk by 1 a given number of times.
    If interrupted with ctrl+c, prints the iteration at which interrupted."""
    #Initialize walk and possible incrementation values
    walk = 0
    directions = [1, -1]
    #Randomly change the walk until the maximum iteration is reached or interrupted 
    #with ctrl+c
    try:
        for i in range(int(max_iters)):
            walk += choice(directions)
    except KeyboardInterrupt:
        print("Process interrupted at iteration",i)
    #Print completion of process if not interrupted
    else:
        print("Process completed.")
    #Always return the final randomized value
    finally:
        return walk


# Problems 3 and 4: Write a 'ContentFilter' class.
class ContentFilter:
    """Accepts the name of a file to be read, prompting the user for another
    file name if the given file name is invalid, and stores the file information.
    
    Attributes:
        name (str): The name of the file.
        contents (str): The contents of the file."""

    def __init__(self, name):
        """Set the name of the file to be read, requesting a different file name 
        if the initial file name is invalid.
        
        Parameters:
            name (str): The name of the file to be read."""
        #Repeats until a valid file name is given
        done = False
        while not done:
            try:
                #Attempts to read the given file into the contents attribute
                with open(name, "r") as file:
                    self.contents = file.read()
                #Sets the name attribute to the file name
                self.name = name
            #Asks for valid input if the file isn't successfully read
            except Exception:
                name = input("Please enter a valid file name: ")
            #Stops repeating when a valid file name is given
            else:
                done = True

    def uniform(self, out_name, mode="w", case="upper"):
        """Writes the data stored in contents to a specified outfile, all in
        a specified uniform case."""
        #Raises a ValueError if an invalid case is given
        if case != "upper" and case != "lower":
            raise ValueError("Case argument must either be 'upper' or 'lower', written in lowercase.")
        #Opens a new file to write to
        with open(out_name, mode) as u_file:
            #Upper case
            if case == "upper":
                u_file.write(self.contents.upper())
            #Lower case
            if case == "lower":
                u_file.write(self.contents.lower())
    
    def reverse(self, out_name, mode="w", unit="word"):
        """Writes the data in contents to a specified outfile in reverse order,
        reversing either the order of words in a line or lines in the file."""
        #Raises error if invalid reversal unit given
        if unit != "line" and unit != "word":
            raise ValueError("Unit argument must either be 'line' or 'word', written in lowercase.")
        #Opens a new file to write to
        with open(out_name, mode) as u_file:
            #Break the content into lines
            lines = self.contents.split("\n")
            #Line reversal
            if unit == "line":
                for i in range(1,len(lines)):
                    #Writes the lines in reverse order, followed by a new line
                    u_file.write(lines[-i]+"\n")
                #Doesn't add a new line after the last line
                u_file.write(lines[0])
            #Word reversal
            if unit == "word":
                #Goes through each line
                for i in range(len(lines)):
                    words = lines[i].split()
                    #Skips if line is empty
                    if len(words) == 0:
                        continue
                    #Goes through each word backwards
                    for j in range(1,len(words)):
                        u_file.write(words[-j]+" ")
                    #Doesn't add a space or a new line to the last word in the file
                    if i == len(lines)-1:
                        u_file.write(words[0])
                    #Adds a new line instead of a space to the end of each line
                    else:
                        u_file.write(words[0] + "\n")
        

    def transpose(self, out_name, mode="w"):
        """Writes a "transposed" version of contents to a specified outfile such
        that the original columns of words become the new lines of words. Assume
        an equal number of words on each line of the input file."""
        #Breaks the file into lines
        lines = self.contents.split("\n")
        #Breaks the first line into words to use the number of words
        words = lines[0].split()
        #Creates an appropriately sized "matrix" to fill with words
        grid = [[[] for j in range(len(lines))] for i in range(len(words))]
        #Loop through each line
        for i in range(len(lines)):
            #Breaks the i-th row into words
            words = lines[i].split()
            #Fills the i-th column with words from the i-th line
            for j in range(len(words)):
                grid[j][i] = words[j]
        #Writes each entry of the matrix to an appropriate row and column in the file
        with open(out_name, mode) as out_file:
            for k in range(len(grid)):
                #Writes in all but the last word, separating each word with a space
                for l in range(len(lines)-1):
                    out_file.write(grid[k][l] + " ")
                #Writes in the last word of each line, adding a new line if not the 
                #end of the file
                if k != len(grid)-1:
                    out_file.write(str(str(grid[k][-1]) + "\n"))
                else:
                    out_file.write(str(grid[-1][-1]))
            
    def __str__(self):
        """Returns the source file; the numbers of total, alphabetic, numerical, 
         and whitespace characters; and the number of lines."""
        #Sets the various statistics to return as appropriately spaced strings
        #String telling source file name
        source = "Source file:\t\t" + self.name + "\n"
        #String telling total amount of characters
        total_char = "Total characters:\t" + str(len(self.contents)) + "\n"
        #The number of alphabetic characters
        num_alph = sum([char.isalpha() for char in self.contents])
        #String telling number of alphabetic characters
        alph_char = "Alphabetic characters:\t" + str(num_alph) + "\n"
        #Number of numbers
        num_num = sum([char.isdigit() for char in self.contents])
        #String telling number of numbers
        num_char = "Numerical characters:\t" + str(num_num) + "\n"
        #Number of whitespace characters
        num_space = sum([char.isspace() for char in self.contents])
        #String telling number of whitespace characters
        space_char = "Whitespace characters:\t" + str(num_space) + "\n"
        #String telling total number of lines
        total_lines = "Number of lines:\t" + str(len(self.contents.split("\n")))
        #Returns the various statistics strings listed above
        return source + total_char + alph_char +  num_char + space_char + total_lines

#For testing purposes
if __name__ == "__main__":
    #arithmagic()
    #print(random_walk())
    #print(random_walk(1e6))
    cf1 = ContentFilter("hello_world.txt")
    """print(cf1.contents)
    print(cf1.name)"""
    cf2 = ContentFilter("cf_example2.txt")
    """print(cf2.contents)
    print(cf2.name)"""
    cf3 = ContentFilter("cf_example1.txt")
    """print(cf3.contents)
    print(cf3.name)
    print(cf1,"\n")
    print(cf2,"\n")
    print(cf3,"\n")"""
    cf1.uniform("hello_world_upper.txt")
    cf2.uniform("example2.txt","a","lower")
    cf1.reverse("hello_world_reverse_words.txt")
    cf2.reverse("example2_reverse_words.txt")
    cf2.reverse("example2_reverse_lines.txt", unit="line")
    cf1.reverse("hello_world_reverse_lines.txt", unit="line")
    cf3.transpose("example1_transpose.txt")
    cf1.transpose("hello_world_transpose.txt")
    cf2.transpose("example2_transpose.txt")