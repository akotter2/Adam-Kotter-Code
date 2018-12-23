#planet_chooser.py
"""An experiment in making choices. Based on the mobile game "Seed Ship," this code 
models a scenario where a colony ship must choose a planet to settle but cannot go back 
to any unchosen planets. Thus, the colony ship must guess at each planet whether or not 
it is likely to find a better planet for its human passengers. Additionally, the ship 
gets damaged over time, adding an element of pressure to choose quickly to this 
scenario. This code could easily be modified to model the problem of choosing whom to 
marry, given that you can only seriously date one person at a time and breaking up with 
a person is usually final."""


import numpy as np
from matplotlib import pyplot as plt


class Planet():
    """This class stores information about a planet's habitability. Each attribute is 
    a decimal between -1 and 1, inclusive. Positive numbers represent liveability 
    without special equipment (anything from especially thick clothing to domed 
    cities), where 1 represents perfectly ideal conditions and 0 represents the bare 
    edge of unassisted liveability. Negative numbers represent conditions in which 
    humans cannot live without special equipment, where close to 0 represents a need 
    for primitive equipment like spears or reasonably thick clothing and -1 
    represents a need for futuristic equipment like domed cities or armor-piercing 
    missiles.
    As an aside, these attributes represent the planet's most ideal landing site. 
    Future updates may allow for various landing sites per planet.
    
    Attributes: 
    (Note that each attribute with a bracketed number is stored in that position of 
    the attributes array)
        Name (str): the planet's name.
        Gravity[0] (float): how ideal the planet's gravity is, essential.
        Water[1] (float): how ideal the planet's water supply is, essential.
        Atmosphere[2] (float): how ideal the planet's atmosphere is, essential.
        Temperature[3] (float): how ideal the planet's temperature is, essential.
        Food[4] (float): how ideal the planet's supply of edible life is, essential.
        Resources[5] (float): how ideal the planet's supply of resources like wood and 
        metal is, essential.
        Radiation[6] (float): how ideal the planet's protection from cosmic radiation 
        is, essential.
        Life[7] (float): how helpful or harmful local plants and animals are for things 
        other than being eaten. Note that 0 represents neutral in this case.
        Relics[8] (float): how helpful or harmful ruins and other technological remains 
        on a planet are. Note that 0 represents neutral in this case.
        Neighbors[9] (float): how helpful or harmful other intelligent species on a 
        planet are. Note that 0 represents neutral in this case.
    
    Functions:
        Habitability (None; float): returns the planet's habitability, given by the 
        average of the essential attributes plus a scaled sum of the nonessential 
        attributes.
    """
    
    def __init__(self, name, atr):
        """Accepts a name and list-like object of floats between -1 and 1, then 
        assigns them to the different planetary attributes."""
        if len(atr) != 10:
            raise ValueError("Planets have 10 attributes, not " + str(len(atr)))
        for a in atr:
            if a < -1 or a > 1:
                raise ValueError("Planetary attributes range from -1 to 1, which "
                                 "doesn't include " + str(a))
        self.name = str(name)
        self.attributes = atr

    def habitability(self):
        """Returns the planet's habitability score given its essential and 
        nonessential attributes."""
        #Average the essential attributes
        essential = np.mean(self.attributes[0:7])
        #Sum and scale the nonessential attributes
        nonessential = sum((self.attributes[7:10])) / 7
        return essential + nonessential
    
    #Removed because the habitability function is better
    """ 
    def simple_habitability(self):
        #A simpler version of the habitability function for testing purposes.
        return np.mean([self.gravity, self.water, self.atmosphere, self.temperature, 
                       self.food, self.resources, self.radiation, self.life, 
                       self.relics, self.neighbors])

    def both_habitability(self):
        return self.habitability(), self.simple_habitability()
    #"""
    
    def __str__(self):
        return self.name
    

class Ship():
    """An object that tracks the colony ship's status and decides whether or not to 
    colonize a given world, given that the colony ship can only ever settle one world 
    and can't go back to previous worlds. Its attributes that correspond to planetary 
    attributes are scalar values that determine how influential a planetary quality 
    is in determining colonial suitability. For example, a value of 0 for gravity 
    would indicate that the strength of a planet's gravity has no influence at all on 
    whether or not it would make for a good colony site, probably due to advanced 
    technology on the colony ship, a 0.5 would indicate a smaller than normal impact, 
    a 1 would indicate an average impact, a 2 would indicate a larger than normal 
    influence, and a 5 would indicate an extreme influence on colonial suitability, 
    perhaps due to structural fragility of the colony ship.
    Sometimes a ship is physically incapable of handling potential colony sites with 
    certain properties, such as very dangerous wildlife or constantly extreme cold. 
    The No-Go's attribute automatically disqualifies any potential colony site with a 
    negative value in an attribute corresponding to a True value in the No-Go's list. 
    For example, a planet with a -0.2 in the Life attribute could never be colonized 
    by a ship with a True value in nogo[7] because that ship simply cannot handle the 
    dangerous life forms on the planet.
    
    Attributes:
    (Note that each attribute with a bracketed number is stored in that position of 
    the needs array)
        Name (str): the ship's name.
        Colonists (int): the number of living colonists in hibernation, default 1000.
        Scanners (float): the ship's ability to locate "good" planets, default 1.
        Construction (float): the ship's ability to establish a functional colonial 
        infrastructure upon landing, default 1.
        Gravity[0] (float): how much planetary gravitaty impacts colonial suitability, 
        default 1.
        Water[1] (float): how much planetary water quality impacts colonial suitability, 
        default 1.
        Atmosphere[2] (float): how much planetary air quality impacts colonial 
        suitability, default 1.
        Temperature[3] (float): how much planetary temperature impacts colonial 
        suitability, default 1.
        Food[4] (float): how planetary food quality impacts colonial suitability, 
        default 1.
        Resources[5] (float): how planetary resource quality impacts colonial 
        suitability, default 1.
        Radiation[6] (float): how planetary radiation shielding impacts colonial 
        suitability, default 1.
        Life[7] (float): how the usefulness or dangerousness of life on a planet impacts 
        colonial suitability, default 1.
        Relics[8] (float): how the usefulness or dangerousness of technological ruins or 
        artifacts on a planet impacts colonial suitability, default 1.
        Neighbors[9] (float): how the helpfulness or dangerousness of intelligent life 
        on a planet impacts colonial suitability, default 1.
        No-Go's (ndarray, bool): whether or not a negative value in a planetary 
        attribute is permissible for considering a potential colony site, where each 
        position in the array corresponds to the attribute in the same position in 
        the list of planetary attributes.
    
    Functions:
        Get_Planet (None; Planet): returns a random Planet object for decision making.
        Choose (Planet; bool): decides whether or not to colonize a planet.
    """
    
    def __init__(self, name, col=1000, sca=1, con=1, needs=np.full(10,1), nogo=np.full(10,False)):
        """Accepts a name, a number of colonists, a scanner quality, a construction 
        module quality, and a list-like object of floats between 0 and 5, then 
        assigns the list elements to the different ship needs. Additionally, accepts 
        a list of boolean values representing whether or not a negative value for a 
        planetary attribute is permissible."""
        self.name = name
        self.colonists = col
        self.scanners = sca
        self.construction = con
        self.needs = needs
        self.nogo = nogo

    def get_planet(self):
        """Creates a random planet.
        Future updates will allow for draws from different distributions."""
        return Planet("Random", np.random.randint(-10, 11, size=10)/10)

    def score(self, planet=None):
        """Return the colonizability score (which is a probability value) of a given 
        planet given the ship's current state. If no planet is given, a random one is 
        generated."""
        #Create random planet if necessary
        if planet is None:
            planet = self.get_planet()
        #Check for deal breakers
        for i in range(10):
            if self.nogo[i] and planet.attributes[i] < 0:
                return 0
        #Scale planetary attributes according to the ship's needs.
        scaled = [self.needs[i]*planet.attributes[i] for i in range(10)]
        #Average the essential scaled attributes
        essential = np.mean(scaled[0:7])
        #Sum and scale the nonessential scaled attributes
        nonessential = sum((scaled[7:10])) / 7
        #Get the planet's colonizability score
        score = (5 + essential + nonessential) / 10
        #Return the score as a probability
        if score < 0:
            return 0
        elif score > 1:
            return 1
        else:
            return score

    def choose(self, planet=None):
        """Return True or False based on whether or not the ship should colonize the 
        given planet. If no planet is given, a random one is generated."""
        prob = self.score(planet)
        return np.random.rand() < prob

    def __str__(self):
        return self.name




#For testing porpoises only
if __name__ == "__main__":
    S = Ship("Test")
    P = S.get_planet()
    #Test the Planet attributes
    """
    print(P)
    print("Name: "+ str(P.name))
    print("Gravity: " + str(P.gravity))
    print("Water: " + str(P.water))
    print("Atmosphere: " + str(P.atmosphere))
    print("Temperature: " + str(P.temperature))
    print("Edible life: " + str(P.food))
    print("Resources: " + str(P.resources))
    print("Radiation: " + str(P.radiation))
    print("Useful Life: " + str(P.life))
    print("Relics: " + str(P.relics))
    print("Neighbors: " + str(P.neighbors))
    print("Habitability: " + str(P.habitability()))
    #"""
    #Test the habitability of different planets
    """
    A = Planet("Antarctica", [1, -0.5, 0.9, -0.8, -0.4, -0.7, 0.8, 0, 0, 0])
    print(A.name + ": " + str(A.habitability()) + "\t\t" + str(round(A.habitability(), 2)))
    D = Planet("Sahara", [1, -0.8, 0.9, -0.3, -0.4, -0.7, 0.5, -0.2, 0, 0])
    print(D.name + ": " + str(D.habitability()) + "\t\t" + str(round(D.habitability(), 2)))
    J = Planet("Jungle", [1, 1, 1, 0.9, 0.8, 0.8, 1, -0.8, -0.1, -0.4])
    print(J.name + ": " + str(J.habitability()) + "\t\t" + str(round(J.habitability(), 2)))
    Mg = Planet("Smog", [1, 0.1, -0.1, -0.3, 0.4, 0.4, 0.8, 0.1, 0, 0])
    print(Mg.name + ": " + str(Mg.habitability()) + "\t\t" + str(round(Mg.habitability(), 2)))
    Cc = Planet("Citified, civil", [0.8, 0.7, 0.4, 0.8, 0.4, 0.4, 0.9, 0, 0, -0.3])
    print(Cc.name + ": " + str(Cc.habitability()) + "\t" + str(round(Cc.habitability(), 2)))
    Ch = Planet("Citified, hostile", [0.8, 0.7, 0.4, 0.8, 0.4, 0.4, 0.8, -0.1, 0, -0.9])
    print(Ch.name + ": " + str(Ch.habitability()) + "\t" + str(round(Ch.habitability(), 2)))
    Mn = Planet("Moon", [-0.1, -1, -1, -0.5, -1, -0.9, 0, 0, 0, 0])
    print(Mn.name + ": " + str(Mn.habitability()) + "\t\t" + str(round(Mn.habitability(), 2)))
    W = Planet("Water World", [0.9, 0.3, 0.8, 0.8, 0.8, 0, 0.9, -0.8, 0, 0])
    print(W.name + ": " + str(W.habitability()) + "\t\t" + str(round(W.habitability(), 2)))
    print(P.name + ": " + str(P.habitability()) + "\t\t" + str(round(P.habitability(), 2)))
    #"""
    #Plot the differences between the two habitability functions
    """
    random_planets = [S.get_planet().both_habitability() for _ in range(int(1e5))]
    plt.subplot(131)
    plt.title("Habitability")
    plt.hist([x[0] for x in random_planets], bins=np.linspace(-1,1,200), density=True)
    plt.subplot(132)
    plt.title("Simple Habitability")
    plt.hist([x[1] for x in random_planets], bins=np.linspace(-1,1,200), density=True)
    plt.subplot(133)
    plt.title("Difference of Complex and Simple Habitability")
    plt.hist([x[0]-x[1] for x in random_planets], bins=np.linspace(-1,1,75), density=True)
    plt.show()
    #"""
    #Test score function
    """
    plt.subplot(221)
    plt.title("1% Chance of Deal-Breaking per Attribute")
    random_probs = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=[(np.random.rand() < 0.01) for _ in range(10)]).score() for _ in range(int(1e5))]
    plt.hist(random_probs, bins=np.linspace(0,1,100), density=True)
    plt.subplot(222)
    plt.title("5% Chance of Deal-Breaking per Attribute")
    random_probs = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=[(np.random.rand() < 0.05) for _ in range(10)]).score() for _ in range(int(1e5))]
    plt.hist(random_probs, bins=np.linspace(0,1,100), density=True)
    plt.subplot(223)
    plt.title("10% Chance of Deal-Breaking per Attribute")
    random_probs = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=[(np.random.rand() < 0.1) for _ in range(10)]).score() for _ in range(int(1e5))]
    plt.hist(random_probs, bins=np.linspace(0,1,100), density=True)
    plt.subplot(224)
    plt.title("20% Chance of Deal-Breaking per Attribute")
    random_probs = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=[(np.random.rand() < 0.2) for _ in range(10)]).score() for _ in range(int(1e5))]
    plt.hist(random_probs, bins=np.linspace(0,1,100), density=True)
    plt.show()
    #"""
    #Test choose function
    """
    iters = int(1e5)
    print("1% Chance of Deal-Breaking per Attribute")
    random_choice = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=[(np.random.rand() < 0.01) for _ in range(10)]).choose() for _ in range(iters)]
    acceptances = random_choice.count(True)
    print("Acceptance rate: " + str(acceptances/iters) + "\n")
    print("5% Chance of Deal-Breaking per Attribute")
    random_choice = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=[(np.random.rand() < 0.05) for _ in range(10)]).choose() for _ in range(iters)]
    acceptances = random_choice.count(True)
    print("Acceptance rate: " + str(acceptances/iters) + "\n")
    print("10% Chance of Deal-Breaking per Attribute")
    random_choice = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=[(np.random.rand() < 0.1) for _ in range(10)]).choose() for _ in range(iters)]
    acceptances = random_choice.count(True)
    print("Acceptance rate: " + str(acceptances/iters) + "\n")
    print("20% Chance of Deal-Breaking per Attribute")
    random_choice = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=[(np.random.rand() < 0.2) for _ in range(10)]).choose() for _ in range(iters)]
    acceptances = random_choice.count(True)
    print("Acceptance rate: " + str(acceptances/iters))
    #"""
