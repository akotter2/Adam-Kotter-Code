#TKG_HASctiveUsers_Resolver.py
"""For combining entries in user lists in .csv format"""


import csv
import numpy as np


def parse_users(filenameR="HSActiveUsers.csv", filenameW="HSActiveUsersParsed.csv"):
    """Takes in the name of a .csv file, counts the number of users that each agency in 
    the fourth column (D) has, and writes the resulting list to a new .csv file. Each 
    row must have a fourth column."""
    #Get the data
    with open(filenameR, "r") as file:
        csvreader = csv.reader(file)
        data = [row for row in csvreader]
        agencies_raw = np.array([row[3] for row in data])
    
    #Get the agencies
    agencies = set()
    for agency in agencies_raw[:]:
        agencies.add(agency)
    agencies = list(agencies)
    n = len(agencies)
    agency_indices = {agencies[i]:i for i in range(n)}
    
    #Count the users per agency
    user_count = np.zeros(n)
    for agency in agencies_raw:
        user_count[agency_indices[agency]] += 1
    
    #Write new .csv document
    with open(filenameW, "w", newline="") as file:
        csvwriter = csv.writer(file)
        for i in range(n):
            csvwriter.writerow((agencies[i], user_count[i]))


if __name__ == "__main__":
    filenameR = "HSActiveUsers.csv"
    filenameW = "HSActiveUsersParsed.csv"
    print("Default file to read: HSActiveUsers.csv")
    choice = input("Change? Y/N ")
    if choice == "Y":
        filenameR = input("New file to read: ")
    print("Default filename to write: HSActiveUsersParsed.csv")
    choice = input("Change? Y/N ")
    if choice == "Y":
        filenameW = input("New filename to write: ")
    parse_users(filenameR, filenameW)