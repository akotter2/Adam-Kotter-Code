#session.py

"""This file is the central data-gathering interface for the data-
driven productivity-tracking software developed especially for 
individuals with emotional or mental health difficulties. The central 
feature of this file is the Session object, which manages user input 
throughout a work session and stores data in a dictionary. The data is 
later saved to a more comprehensive CSV file with data from many 
sessions, where other programs can access the information. If the file 
is run on its own, it creates a Session object and runs it."""

import csv
import pandas as pd
from os import path
from datetime import datetime



class Session:
    """An object for managing productivity-tracking during a work 
    session.
    
    Attributes:
        
        ID (int): A unique identifier for this session derived from 
            the start time of the session.
        
        scale_str (str): A description of the productivity scale used 
            for this program. This mostly objective scale is derived 
            by taking the product of the proportion of time spent 
            working and the proportion of the ideal speed at which the 
            user worked. For example, working at half speed for half 
            of the time would be a productivity score of 0.25. This 
            scale helps to ensure consistency and accuracy.
        
        emotion_axes (tuple of str): The names of the emotions for the 
            axes of the emotion vector space. These emotions were 
            chosen to be fundamental, easy to identify, and useful to 
            work with.
        
        user (str): The user's unique identifier, used to tell where 
            to save the data to.
        
        data (dict): A dictionary of lists indexed by attributes. It 
            contains all of the data reported by the user for the 
            session. Corresponding indices between lists in the 
            dictionary represent a "check-in" instance for the 
            beginning or end of each break period and each work period.
            Attributes:
                start_time (datetime): The start time for this period. 
                    This will almost always coincide very closely with 
                    the end time from the previous index except when a 
                    period is the first of the day.
                ID (int): The unique identifier for the session, used 
                    when aggregating data from multiple sessions.
                emotion (list of float): Numbers corresponding to the 
                    emotional state of the user at the beginning of a 
                    period, from 0 to 10. The names of the emotions 
                    are given in self.emotion_axes.
                type (str): The type of productive period for this 
                    time, either "work", "break", or "other".
                activity (set of str): Keywords for the activities 
                    done during this period, such as "typing" or 
                    "stress ball".
                productivity (float, None): A measure of productivity 
                    during the period, from 0 to 1 or higher, where 
                    0 represents no productivity, 1 represents ideal 
                    productivity, and higher than 1 represents hyper-
                    productivity. The value for periods of type 
                    "break" is always None.
                end_time (datetime): The end time for this period. 
                    This will almost always coincide very closely with 
                    the start time for the next index except when a 
                    period is the last of the day.
                duration (int): The duration of the period in minutes, 
                    calculated by subtracting end_time from start_time 
                    for the period.
    
    Methods:
        
        __init__: Creates and runs a new session unless the "run_now" 
            parameter is set to False.
        
        run: Continues collecting information about user productivity 
            until the Session ends. Repeatedly calls "new_period".
        
        new_period (bool, int): Adds a new row to the Session's data  
            dictionary and collects user input for the current period. 
            Returns a boolean value for whether or not the Session is 
            over.
        
        save: Saves the data to a CSV file, appending the new data to 
            an already existing file if the user already has a file."""
    
    
    def __init__(self, user=None, run_now=True):
        """Begins the session by setting up the data structure. The 
        username is usually set by prompted user input, but can be set 
        by passing a string into the parameter "user". The session 
        will run automatically unless "run_now" is set to False."""
        
        # Get the ID for the session
        self.ID = int(datetime.timestamp(datetime.now()))
        
        # Describe the productivity scale to be displayed later
        self.scale_str = "0 means that no productive work was done.\n"\
                         "0.25 means that about half of the time was "\
                         "spent working, and that work was "\
                         "moderately slow, or that about a quarter "\
                         "of the time was spent working quickly.\n"\
                         "0.5 means that productive work was done "\
                         "the whole time, but slowly, or that fast "\
                         "work was done for about half of the time.\n"\
                         "0.75 means that productive work was done "\
                         "the whole time at a moderate pace, or that "\
                         "fast work was done for about three "\
                         "quarter of the time.\n"\
                         "1 means that productive work was done the "\
                         "whole time at an optimally fast pace.\n"\
                         "Anything higher than 1 means that work was "\
                         "done consistently at a manic pace."
        
        # List the axes of the emotion vector space
        self.emotion_axes = ("happy", "sad", "angry", "powerful", 
                             "peaceful", "tired", "stressed", 
                             "anxious", "bored", "lonely")
        
        # Check if the username was set, asking for input if not
        if user is not None:
            self.user = user
        else:
            # Get the user's name to tell where to save the data
            print("Welcome to work!")
            self.user = input("What's your username? Please "
                              "be consistent between sessions. : ")
            print()
        
        # Set up the data dictionary
        self.data = {"start_time": [], "ID": [], "emotion": [], 
                     "type": [], "activity": [], "productivity": [], 
                     "end_time": [], "duration": []}
        
        # Begin the session as applicable, saving if an error occurs
        if run_now:
            try:
                self.run()
            except:
                print("\nUnexpected program shutdown.")
                self.save()
                print("\nCurrent data saved.")
    
    
    def run(self):
        """Begins and continues the data-gathering process until the 
        session is over, at which point it saves the data."""
        
        # Begin looping until the session is complete
        keep_going = True
        while keep_going:
            keep_going = self.new_period()
        
        # Save the data
        self.save()
    
    
    def new_period(self):
        """Appends the user's data to the session's data dictionary 
        for each period. Indexing is kept consistent by always 
        appending exactly one element to each list in the data 
        dictionary for each period. Returns True if this is the last 
        period of the session, returns False otherwise."""
        
        # Add the data that requires no user input
        self.data["start_time"].append(datetime.now())
        self.data["ID"].append(self.ID)
        
        # Set up the emotion-recording system
        emotions = [0.0 for _ in range(len(self.emotion_axes))]
        emotions_done = False
        i = 0
        print("On a scale from 0 to 10, how strongly do you feel each "
              "of the following emotions?")
        
        # Ask for the user's state in each emotion and record it
        while not emotions_done:
            emotion = self.emotion_axes[i]
            em_state = input("How {} do you feel? : ".format(emotion))
            # Make sure that the input is valid
            if em_state.replace(".", "", 1).isdigit():
                emotions[i] = float(em_state)
                i += 1
                # Stop asking if all emotions have been asked for
                if i >= len(self.emotion_axes):
                    emotions_done = True
            else:
                print("Sorry, {} isn't valid input.".format(em_state))
        self.data["emotion"].append(emotions)
        print()
        
        # Ask and record whether this is work or a break
        work_type = "other"
        user_input = input("Are you about to begin work or a break? "
                           "Enter 'w' for work or 'b' for break. : ")
        print()
        if user_input.startswith("w") or user_input.startswith("W"):
            work_type = "work"
        elif user_input.startswith("b") or user_input.startswith("B"):
            work_type = "break"
        self.data["type"].append(work_type)
        
        # Get the end time and duration when the period ends
        fin = input("Are you done with your {}? ".format(work_type) + 
                    "Press Enter when done")
        print()
        self.data["end_time"].append(datetime.now())
        start = self.data["start_time"][-1]
        end = self.data["end_time"][-1]
        duration = end - start
        
        # Convert the duration into an integer number of minutes to add
        duration_int = round(duration.seconds/60)
        self.data["duration"].append(duration_int)
        
        # Ask the user for activity keywords and record them
        activities = set()
        activities_done = False
        while not activities_done:
            activity = input("What did you do with your time? "
                            "If done, press Enter again. : ")
            if activity == "":
                activities_done = True
            else:
                activities.add(activity)
        print()
        if activities == set():
            activities.add(None)
        self.data["activity"].append(activities)
        
        # Ask for the user's productivity if applicable and record it
        if self.data["type"][-1] == "break":
            self.data["productivity"].append(None)
        else:
            # Remind the user of the productivity scale
            print("How would you rate your productivity? As a "
                  "reminder, productivity is rated on a scale from 0 "
                  "to 1 or higher.\n")
            print(self.scale_str)
            productivity = input("How would you rate your "
                                 "productivity for this period? : ")
            print()
            # Record the productivity
            self.data["productivity"].append(float(productivity))
        
        # Ask if the user is going to continue tracking time
        restart = input("Are you going to start another period "
                             "of work or break time that you would "
                             "like to track? Enter 'y' for yes or 'n' "
                             "for no. : ")
        print()
        
        # Return True or False for whether or not to keep going
        if restart.startswith("y") or restart.startswith("Y"):
            return True
        elif restart.startswith("n") or restart.startswith("N"):
            print("Have a good rest of your day!")
            return False
    
    
    def save(self):
        """Exports the data in the data dictionary to a CSV file. If 
        there is already a CSV file with the given username, then the 
        new data is appended to the end of the old file. The data is 
        indexed by the start dates."""
        
        # Convert the data dictionary to a Pandas DataFrame
        out_data = pd.DataFrame(self.data)
        out_data.index = out_data["start_time"]
        
        # If the user already has data, don't append a new header
        write_header = True
        if path.exists("./output/{}_data.csv".format(self.user)):
            write_header = False
        
        # Save the data
        out_data.to_csv("./output/{}_data.csv".format(self.user), 
                        index=False, header=write_header, mode="a")
    
    
    def get_activities(self):
        """Gets the list of previously used activity tags from the 
        "tags" folder, accessing only the file specific to the current 
        user. Creates a new file with generic activities if the user 
        doesn't have a file to pull activity tags from.
        
        Returns: activity_list (list of str): the list of previously 
            used activity tags for the user."""
        
        # Check if the user already has a file
        user_path = "./tags/{}_tags.csv".format(self.user)
        if path.exists(user_path):
            # Get the activities
            activity_list = []
            with open(user_path, "r") as in_file:
                reader = csv.reader(in_file)
                for row in reader:
                    activity_list.append(row)
            return activity_list
        
        # Create a new, generic file if the user has no file
        else:
            # Create a list of generic activities
            generic_activities = ["typing", "reading", "reports", 
                                  "studying", "homework", "exercise", 
                                  "sleep", "listen to music", "walk", 
                                  "run", "TV"]
            
            # Write the list to a new CSV file
            with open(user_path, "w", newline="") as out_file:
                writer = csv.writer(out_file)
                for activity in generic_activities:
                    writer.writerow([activity])
            
            # Use recursion to return the activities list
            return self.get_activities()
    
    
    def write_activities(self, activities):
        """Writes new activities to the list of activity tags in the 
        user's file in the "tags" folder. Uses sets and is not case-
        sensitive in order to avoid repeats, including from within the 
        file to be written to. Will not create a new file if the user 
        does not have a file in the "tags" folder. The 
        "get_activities" method implements new file creation."""
        
        pass



# Open and run a new Session if this file is run directly
if __name__ == "__main__":
    session = Session()