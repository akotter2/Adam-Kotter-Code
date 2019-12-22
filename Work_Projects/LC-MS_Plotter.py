#LC-MS_Plotter.py
"""Asks for the name of a properly formatted .csv file and plots its LC-MS data."""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Ask for the data until it's successfully gotten
while True:
    try:
        file_name = input("Full name of file: ")
        df = pd.read_csv(file_name)
        assert len(df.columns.values) == 3, "Need three columns: m/z, RT, and intensity"
    except:
        print("Invalid file.")
        restart = input("Try again with a different file name? Y/N ")
        if restart != "Y":
            break
    break

# Display the data...
fig = plt.figure()
# ... from the m/z angle
ax = fig.add_subplot(221, projection="3d")
ax.view_init(elev=0., azim=-90)
plt.title(r"$\frac{m}{z}$ View")
ax.scatter(df.iloc[:,0], df.iloc[:,1], df.iloc[:,2])
plt.xlabel(r"$\frac{m}{z}$")
plt.ylabel("RT")
ax.set_zlabel("Counts")
# ... from the RT angle
ax = fig.add_subplot(222, projection="3d")
ax.view_init(elev=0., azim=0)
plt.title(r"RT View")
ax.scatter(df.iloc[:,0], df.iloc[:,1], df.iloc[:,2])
plt.xlabel(r"$\frac{m}{z}$")
plt.ylabel("RT")
ax.set_zlabel("Counts")
# ... and from two other angles
ax = fig.add_subplot(223, projection="3d")
ax.view_init(elev=5., azim=-45)
plt.title(r"Combination View")
ax.scatter(df.iloc[:,0], df.iloc[:,1], df.iloc[:,2])
plt.xlabel(r"$\frac{m}{z}$")
plt.ylabel("RT")
ax.set_zlabel("Counts")
# ... and from two other angles
ax = fig.add_subplot(224, projection="3d")
ax.view_init(elev=5., azim=-135)
plt.title(r"Combination View")
ax.scatter(df.iloc[:,0], df.iloc[:,1], df.iloc[:,2])
plt.xlabel(r"$\frac{m}{z}$")
plt.ylabel("RT")
ax.set_zlabel("Counts")
plt.show()