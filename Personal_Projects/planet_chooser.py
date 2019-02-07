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
import copy


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
    Attribute scale:
        1.0: Edenic, paradisiacal conditions
        0.5: Uncomfortable, but liveable without too much extra effort
        0.0: Liveable, but barely
       -0.5: Somewhat complicated technology is required for survival
       -1.0: Very advanced technology is required for survival

    
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
    sufficiently low value in different planetary attributes. For example, a planet 
    with a -0.5 in the Life attribute could never be colonized by a ship with a value 
    of 0 in nogo[7] because that ship simply cannot handle the dangerous life forms 
    on the planet.
    
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
        No-Go's (ndarray, float): how low of a value in a planetary attribute is 
        permissible for considering a potential colony site, where each position in 
        the array corresponds to the attribute in the same position in the list of 
        planetary attributes.
    
    Functions:
        Get_Planet (None; Planet): returns a random Planet object for decision making.
        Choose (Planet; bool): decides whether or not to colonize a planet.
    """
    
    def __init__(self, name, col=1000, sca=1, con=1, needs=np.full(10,1,dtype=float), no=np.full(10,-1,dtype=float)):
        """Accepts a name, a number of colonists, a scanner quality, a construction 
        module quality, and a list-like object of floats between 0 and 5, then 
        assigns the list elements to the different ship needs. Additionally, accepts 
        a list of floats from -1 to 1 representing the minimum acceptable value for a 
        planetary attribute."""
        self.name = name
        self.colonists = col
        self.scanners = sca
        self.construction = con
        self.needs = needs
        self.nogo = no

    def get_planet(self, dist="normal-essential-n", stdev=0.2, s=0.5):
        """Creates a random planet drawn from a specified distribution.
        
        Parameters:
            dist (str): the distribution used to generate the planet.
                "uniform": all attributes are selected from a uniform distribution.
                "normal": all attributes are selected from a normal distribution 
                centered at a mean selected from a uniform distribution and with a 
                standard deviation specified by user input.
                "normal-essential-u": all essential attributes are chosen the same way 
                as in "normal", while non-essential attributes are selected from a 
                uniform distribution.
                "normal-essential-n": all attributes are chosen the same way 
                as in "normal-essential-u", with the exception that non-essential 
                attributes are selected from a normal distribution of standard 
                deviation specified as 's'.
            stdev (float): the standard deviation of the "normal" and the  "normal-
            essential" distributions.
        """
        if dist == "uniform":
            return Planet("Random", np.random.randint(-10, 11, size=10)/10)
        elif dist == "normal":
            base_score = np.random.randint(-10, 11)/10
            attributes = np.random.normal(loc=base_score, scale=stdev, size=10)
            for i in range(len(attributes)):
                if attributes[i] > 1:
                    attributes[i] = 1
                if attributes[i] < -1:
                    attributes[i] = -1
            return Planet("Random", attributes)
        elif dist == "normal-essential-u":
            base_score = np.random.randint(-10, 11)/10
            attributes = np.random.normal(loc=base_score, scale=stdev, size=10)
            attributes[7:10] = np.random.randint(-10, 11, size=3)/10
            for i in range(len(attributes)):
                if attributes[i] > 1:
                    attributes[i] = 1
                if attributes[i] < -1:
                    attributes[i] = -1
            return Planet("Random", attributes)
        elif dist == "normal-essential-n":
            base_score = np.random.randint(-10, 11)/10
            attributes = np.random.normal(loc=base_score, scale=stdev, size=10)
            attributes[7:10] = np.random.normal(loc=0, scale=s, size=3)
            for i in range(len(attributes)):
                if attributes[i] > 1:
                    attributes[i] = 1
                if attributes[i] < -1:
                    attributes[i] = -1
            return Planet("Random", attributes)
        else:
            raise ValueError(str(dist) + " isn't a recognized probability distribution")

    def score(self, planet=None, model="full", desperation=-2.8, standards=3.9, baseline=0.2):
        """Return the colonizability score (which is a probability value) of a given 
        planet given the ship's current state. If no planet is given, a random one is 
        generated.
        
        Parameters:
            Planet (Planet): the planet being analyzed, defaults to random.
            Model (str): the probability scaling model used for determining 
            colonizability. The default ("full") is a composition of an exponential 
            and a logistic model. Other options include "exponential" and "logistic", 
            with more coming in future updates.
            Desperation (float): how willing the ship is to settle for less-than-ideal 
            conditions, corresponding to a horizontal shift in logistic-based models. 
            The more negative the value, the less desperate the ship, the more 
            positive the value, the more desperate the ship.
            Baseline (float): how necessary and non-negotiable ideal conditions in 
            general are for the ship during the scoring. This corresponds to a 
            scaling of the exponential term of exponential-based models. Must be a 
            positive value, with larger values corresponding to a greater need for 
            ideal conditions.
            Standards (float): how quickly non-ideal conditions become unacceptable, 
            corresponding to a scaling of the x-term within the exponential of 
            logistic-based models. Must be positive, with larger values representing 
            faster increases in unacceptability after a certain habitability 
            threshold is reached.
            """
        if type(model) != str:
            raise TypeError("Probability scaling model must be in string format")
        #Create random planet if necessary
        if planet is None:
            planet = self.get_planet()
        #Check for deal breakers
        for i in range(10):
            if self.nogo[i] > planet.attributes[i]:
                return 0
        #Scale planetary attributes according to the ship's needs.
        scaled = [self.needs[i]*planet.attributes[i] for i in range(10)]
        #Average the essential scaled attributes
        essential = np.mean(scaled[0:7])
        #Sum and scale the nonessential scaled attributes
        nonessential = sum((scaled[7:10])) / 7
        #Get the planet's colonizability score by model
        #Treat scaled_habitability as x in each model
        scaled_habitability = (essential + nonessential)
        if model == "exponential":
            score = np.exp((scaled_habitability - 1)*baseline)
        elif model == "logistic":
            score = 1 / (1 + (np.exp(-1*(desperation+scaled_habitability*standards))))
        elif model == "full":
            log_factor = 1 / (1 + (np.exp(-1*(desperation+scaled_habitability*standards))))
            score = np.exp((scaled_habitability - 1)*baseline/log_factor)
        else:
            raise ValueError("Probability scoring model " + str(model) + " not recognized")
        #Return the score as a probability
        if score < 0:
            return 0
        elif score > 1:
            return 1
        else:
            return score

    def choose(self, planet=None, model="full", desperation=-2.8, standards=3.9, baseline=0.2):
        """Return True or False based on whether or not the ship should colonize the 
        given planet. If no planet is given, a random one is generated. See docstring 
        for score() function for more information on parameters and so forth."""
        prob = self.score(planet, model=model, desperation=desperation, standards=standards, baseline=baseline)
        return np.random.rand() < prob

    def __str__(self):
        return self.name


class Simulator():
    """Creates randomized scenarios to find an optimal solution for the planet 
    choosing algorithm.
    
    Attributes:
        Distribution (str): the distribution of planetary attributes in the scenario, 
        corresponding to Ship.get_planet(dist).
        Model (str): the probability scaling model used for determining a planet's 
        colonizability, corresponding to Ship.choose(model).
        Ship (Ship): tracks the status of the ship used in the current simulation.
        Planets (list, Planet): a list of all the planets in the simulation. The 
        length of the list is defined in the constructor, and the simulation ends if 
        the last planet is reached.
        Landed (bool): whether or not the ship has landed on a planet.
        Current (int): the index of the current planet to be selected.
        Desperation (float): how willing the ship is to settle for less-than-ideal 
        conditions. The more negative the value, the less desperate the ship, the 
        more positive the value, the more desperate the ship.
    
    Functions:
        Optimal (none; Planet): returns the most habitable planet in the simulation.
        Turn(none; bool): moves to the next planet in the simulation, chooses whether 
        to settle or not, and applies random changes in ship status. Returns True if 
        the ship settled on a planet, False if the ship reached the end of the 
        simulation without settling on a planet.
        Run (none; float): implements turn() without user input until the end of the 
        simulation, then returns the difference between the ideal planet in the 
        simulation and the planet that was chosen.
        Reset (none; none): creates a new ship, randomizes the planets, and resets 
        the index of the current planet, the desperation, and the landing status to 
        their default values.
    """

    def __init__(self, name="Simulation", length=int(1e2), dist="normal-essential-n", 
                 model="full", desperation=-10.0):
        self.ship = Ship(name)
        self.distribution = dist
        self.model = model
        self.planets = [self.ship.get_planet(dist) for _ in range(length)]
        self.landed = False
        self.current = -1
        self.desperation = desperation
        self.desp_default = desperation
    
    def optimal(self):
        """Get the index of the planet with the highest habitability score."""
        max_i = 0
        for i in range(len(self.planets)):
            if self.planets[i].habitability() > self.planets[max_i].habitability():
                max_i = i
        return max_i
    
    def turn(self):
        """Moves to the next planet in the simulation and apply different effects."""
        #Move to next planet
        if self.landed or self.current >= len(self.planets)-1:
            self.landed = True
            return
        self.current += 1
        #Increase desperation and receive damage
        self.desperation += 0.1
        index = np.random.randint(0,10)
        self.ship.nogo[index] += 0.1
        self.ship.needs[index] += 0.1
        p = self.planets[self.current]
        #print("Habitability of planet " + p.name + ": " + str(p.habitability()))
        self.landed = self.ship.choose(planet=p, model=self.model, desperation=self.desperation)
        if self.current >= len(self.planets):
            self.landed = True
            return
    
    def run(self):
        """Implement turn() repeatedly, then return the difference between the 
        selected planet and the optimal planet."""
        while self.current < len(self.planets) and not self.landed:
            self.turn()
        return self.planets[self.optimal()].habitability() - self.planets[self.current].habitability()
    
    def reset(self):
        """Restores randomization and simulation defaults."""
        name = self.ship.name
        self.ship = None
        self.ship = Ship(name)
        length = len(self.planets)
        self.planets = [self.ship.get_planet(self.distribution) for _ in range(length)]
        self.landed = False
        self.current = -1
        self.desperation = self.desp_default


#For testing porpoises only
if __name__ == "__main__":
    #Create ships with different needs
    all_needs = np.full((11,10),1)
    for i in range(10):
        all_needs[i,i] = 2
    names = ["Gravity", "Water", "Atmosphere", "Temperature", "Edible Life", 
             "Resources", "Radiation", "Useful Life", "Relics", "Neighbors", "Normal"]
    ships = [Ship(names[i], needs=all_needs[i]) for i in range(11)]

    #Create different planets
    S = Ship("Test")
    P = S.get_planet()
    Pl = Planet("Plains", [0.8, 0.3, 0.9, 0.2, 0.5, 0.5, 0.8, 0.1, 0, 0.1])
    A = Planet("Antarctica", [1, -0.5, 0.9, -0.8, -0.4, -0.7, 0.8, 0, 0, 0])
    D = Planet("Sahara", [1, -0.8, 0.9, -0.3, -0.4, -0.7, 0.5, -0.2, 0, 0])
    J = Planet("Jungle", [1, 1, 1, 0.9, 0.8, 0.8, 1, -0.8, -0.1, -0.4])
    Mg = Planet("Smog", [1, 0.1, -0.1, -0.3, 0.4, 0.4, 0.8, 0.1, 0, 0])
    Cc = Planet("Citified, civil", [0.8, 0.7, 0.4, 0.8, 0.4, 0.4, 0.9, 0, 0, -0.3])
    Ch = Planet("Citified, hostile", [0.8, 0.7, 0.4, 0.8, 0.4, 0.4, 0.8, -0.1, 0, -0.9])
    Mn = Planet("Moon", [-0.1, -1, -1, -0.5, -1, -0.9, 0, 0, 0, 0])
    W = Planet("Water World", [0.9, 0.3, 0.8, 0.8, 0.8, 0, 0.9, -0.8, 0, 0])
    E = Planet("Eden", [1, 1, 1, 1, 1, 1, 1, 1, 0, 0])
    I = Planet("Crushing Inferno", [-1, -1, -1, -1, -1, -0.2, -0.5, 0, -0.2, 0])
    planets = [A, D, J, Mg, Cc, Ch, Mn, W, Pl, E, I, P]

    #Test distributions for get_planet()
    """
    plt.suptitle("Planetary Attributes by Distribution")
    labels = names.copy()
    labels.pop()
    labels.append("Habitability")
    distributions = ["uniform", "normal", "normal-essential-n", "normal-essential-u"]
    stdevs = [0.1, 0.2, 0.5, 0.7, 1]
    planets = [[[S.get_planet(dist=d, stdev=st) for _ in range(5)] for st in stdevs] for d in distributions]
    #Uniform
    plt.subplot(321)
    plt.title("Uniform")
    for planet in planets[0][0]:
        plt.plot(np.hstack([planet.attributes, planet.habitability()]))
        plt.xticks(np.arange(0,11), labels)
    #Normal
    for i in range(len(stdevs)):
        plt.subplot(322+i)
        plt.title("Normal, STDEV = " + str(stdevs[i]))
        for planet in planets[1][i]:
            plt.plot(np.hstack([planet.attributes, planet.habitability()]))
            plt.xticks(np.arange(0,11), labels)
    plt.show()
    #Normal-Essential-N
    plt.suptitle("Planetary Attributes by Distribution")
    plt.subplot(321)
    plt.title("Uniform")
    for planet in planets[0][0]:
        plt.plot(np.hstack([planet.attributes, planet.habitability()]))
        plt.xticks(np.arange(0,11), labels)
    for i in range(len(stdevs)):
        plt.subplot(322+i)
        plt.title("Normal-Essential-N, STDEV = " + str(stdevs[i]))
        for planet in planets[2][i]:
            plt.plot(np.hstack([planet.attributes, planet.habitability()]))
            plt.xticks(np.arange(0,11), labels)
    plt.show()
    #Normal-Essential-U
    plt.suptitle("Planetary Attributes by Distribution")
    plt.subplot(321)
    plt.title("Uniform")
    for planet in planets[0][0]:
        plt.plot(np.hstack([planet.attributes, planet.habitability()]))
        plt.xticks(np.arange(0,11), labels)
    for i in range(len(stdevs)):
        plt.subplot(322+i)
        plt.title("Normal-Essential-U, STDEV = " + str(stdevs[i]))
        for planet in planets[3][i]:
            plt.plot(np.hstack([planet.attributes, planet.habitability()]))
            plt.xticks(np.arange(0,11), labels)
    plt.show()
    #"""

    #Test the Normal-Essential distributions
    """
    #Get the planets
    distributions = ["uniform", "normal-essential-n", "normal-essential-u"]
    stdevs = [0.1, 0.2, 0.5, 0.7, 1]
    planets = [[[S.get_planet(dist=d, s=st) for _ in range(5)] for st in stdevs] for d in distributions]
    #Get the x-axis labels
    labels = names.copy()
    labels.pop()
    labels.append("Habitability")
    #Normal-Essential-N
    plt.suptitle("Normal-Essential-N")
    plt.subplot(321)
    plt.title("Uniform")
    for planet in planets[0][0]:
        plt.plot(np.hstack([planet.attributes, planet.habitability()]))
        plt.xticks(np.arange(0,11), labels)
    for i in range(len(stdevs)):
        plt.subplot(322+i)
        plt.title("S = " + str(stdevs[i]))
        for planet in planets[1][i]:
            plt.plot(np.hstack([planet.attributes, planet.habitability()]))
            plt.xticks(np.arange(0,11), labels)
    plt.show()
    #Normal-Essential-U
    plt.suptitle("Normal-Essential-U")
    plt.subplot(321)
    plt.title("Uniform")
    for planet in planets[0][0]:
        plt.plot(np.hstack([planet.attributes, planet.habitability()]))
        plt.xticks(np.arange(0,11), labels)
    for i in range(len(stdevs)):
        plt.subplot(322+i)
        plt.title("S = " + str(stdevs[i]))
        for planet in planets[2][i]:
            plt.plot(np.hstack([planet.attributes, planet.habitability()]))
            plt.xticks(np.arange(0,11), labels)
    plt.show()
    #"""

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
    for p in planets:
        print(p.name + ": " + str(p.habitability()))
        print(round(p.habitability(), 2))
    #"""

    #Test the score of the different planets using different ships and different desperations
    """
    plt.suptitle("Habitability Probability Score")
    for i, d in enumerate([-11, -5, -2.8, -1, 0, 1, 2.8, 5, 11]):
        plt.subplot(331+i)
        plt.title("Desperation Level " + str(i))
        for p in planets:
            scores = [ship.score(p, desperation=d) for ship in ships]
            plt.plot(scores, label=p.name)
        plt.xticks(np.arange(0,11), names, fontsize=5, rotation=0)
    plt.legend()
    #plt.tight_layout()
    plt.show()
    #"""

    #Test choice of different planets using different ships and different desperations, no no-go's
    """
    iters = int(1e2)
    plt.suptitle("Rate of Acceptance")
    for i, d in enumerate([-11, -5, -2.8, -1, 0, 1, 2.8, 5, 11]):
        plt.subplot(331+i)
        plt.title("Desperation Level " + str(i))
        for p in planets:
            acceptances = [np.mean([ship.choose(p, desperation=d) for _ in range(iters)]) for ship in ships]
            plt.plot(acceptances, label=p.name)
        plt.xticks(np.arange(0,11), names, fontsize=5, rotation=0)
        #plt.legend()
        #plt.show()
    plt.legend()
    #plt.tight_layout()
    plt.show()
    #Results: 
        #Only perfection: -11
        #Choosy, no rush: -5
        #Seriously considering really uncomfortable conditions: -2.8
        #Seriously considering some pretty risky conditions: -1
        #If living outside won't kill me, I'll probably take it: 0
        #Honestly contemplating unliveable conditions: 1
        #Honestly contemplating truly hellish conditions: 2.8
        #Please, I'll take almost anything: 5
        #Leaps at any chance: 11
    #"""

    #Test choice of different planets using different ships, desperations, and no-go's
    """
    iters = int(1e2)
    #Create the different no-go parameters and ships to be tested
    nogos = [np.full(10,-1), np.random.choice([-1,-1,0], size=10), np.random.rand(10)*(-0.2)-0.8, np.random.rand(10)*(-0.4)-0.6, np.random.randint(-10, 1, size=10)/10, np.zeros(10)]
    nogo_words = ["No No-Go's", "A Few No-Go's on Negatives", "Deal-Breaking at Random Extremes (0.8)", "Deal-Breaking at Random Extremes (0.6)", "Random Negative No-Go's", "No-Go on Negatives"]
    print(nogo_words[1] + ": " + str(nogos[1]))
    print(nogo_words[2] + ": " + str(nogos[2]))
    print(nogo_words[3] + ": " + str(nogos[3]))
    print(nogo_words[4] + ": " + str(nogos[4]))
    nogo_ships = [copy.deepcopy(ships) for _ in range(len(nogos))]
    for i, n in enumerate(nogos):
        for j in range(len(ships)):
            nogo_ships[i][j].nogo = n
    #Cycle through each no-go variation
    for i in range(len(nogos)):
        #Plot the acceptance rates by desperation level
        plt.suptitle("Rate of Acceptance, " + nogo_words[i])
        for j, d in enumerate([-11, -5, -2.8, -1, 0, 1, 2.8, 5, 11]):
            plt.subplot(331+j)
            plt.title("Desperation Level " + str(j))
            for p in planets:
                acceptances = [np.mean([ship.choose(p, desperation=d) for _ in range(iters)]) for ship in nogo_ships[i]]
                plt.plot(acceptances, label=p.name)
            plt.xticks(np.arange(0,11), names, fontsize=5, rotation=0)
            #plt.legend()
            #plt.show()
        plt.legend()
        #plt.tight_layout()
        plt.show()
    #"""

    #Test score function
    """
    plt.suptitle("Scores of Random Planets by Ship Type")
    plt.subplot(321)
    plt.title("No Deal-Breakers")
    random_probs = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4).score() for _ in range(int(1e5))]
    plt.hist(random_probs, bins=np.linspace(0,1,100), density=True)
    plt.subplot(322)
    plt.title("33% Chance of Deal-Breaking on Negatives")
    random_probs = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=np.random.choice([-1,-1,0], 10)).score() for _ in range(int(1e5))]
    plt.hist(random_probs, bins=np.linspace(0,1,100), density=True)
    plt.subplot(323)
    plt.title("Completely Random Negative Deal-Breaking")
    random_probs = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=np.random.randint(-10, 1, size=10)/10).score() for _ in range(int(1e5))]
    plt.hist(random_probs, bins=np.linspace(0,1,100), density=True)
    plt.subplot(324)
    plt.title("No-Go on All Negatives")
    random_probs = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=np.full(10, 0)).score() for _ in range(int(1e5))]
    plt.hist(random_probs, bins=np.linspace(0,1,100), density=True)
    plt.subplot(325)
    plt.title("No-Go at Random Extremes (0.8)")
    random_probs = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=np.random.rand(10)*(-0.2)-0.8).choose() for _ in range(int(1e5))]
    plt.hist(random_probs, bins=np.linspace(0,1,100), density=True)
    plt.subplot(326)
    plt.title("No-Go at Random Extremes (0.6)")
    random_probs = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=np.random.rand(10)*(-0.4)-0.6).choose() for _ in range(int(1e5))]
    plt.hist(random_probs, bins=np.linspace(0,1,100), density=True)
    plt.show()
    #"""
    #Test choose function
    """
    iters = int(1e5)
    print("No Deal-Breakers")
    random_choice = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4).choose() for _ in range(iters)]
    acceptances = random_choice.count(True)
    print("Acceptance rate: " + str(acceptances/iters) + "\n")
    print("33% Chance of Negative Deal-Breaking per Attribute")
    random_choice = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=np.random.choice([-1,-1,0], size=10)).choose() for _ in range(iters)]
    acceptances = random_choice.count(True)
    print("Acceptance rate: " + str(acceptances/iters) + "\n")
    print("Random Negative Deal-Breaking")
    random_choice = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=np.random.randint(-10, 1, size=10)/10).choose() for _ in range(iters)]
    acceptances = random_choice.count(True)
    print("Acceptance rate: " + str(acceptances/iters) + "\n")
    print("Deal-Breaking at Extremes")
    random_choice = [Ship("Test", needs=np.random.randint(0, 21, size=10)/4, nogo=np.random.rand(10)*(-0.2)-0.8).choose() for _ in range(iters)]
    acceptances = random_choice.count(True)
    print("Acceptance rate: " + str(acceptances/iters))
    #"""

    #Test the Simulator
    """
    Sim = Simulator()
    print("Index of best planet in galaxy: " + str(Sim.optimal()))
    print("Habitability of best planet in galaxy: " + str(Sim.planets[Sim.optimal()].habitability()))
    print("Planetary attributes: \n" + str(Sim.planets[Sim.optimal()].attributes))
    print("Difference with optimal planet habitability: " + str(Sim.run()))
    print("Planetary attributes: \n" + str(Sim.planets[Sim.current].attributes))
    print("Desperation: " + str(Sim.desperation))
    print("No-go's: " + str(Sim.ship.nogo))
    print("Needs: " + str(Sim.ship.needs))
    #"""

    #Test the Simulator repeatedly
    #"""
    iters = int(1e1)
    diffs = np.zeros(iters)
    habs = np.zeros(iters)
    Sim = Simulator(length=200)
    for i in range(iters):
        diffs[i] = Sim.run()
        habs[i] = Sim.planets[Sim.current].habitability()
        print(Sim.current)
        print(Sim.desperation)
        print(Sim.ship.nogo)
        Sim.reset()
    print("Mean difference from optimal planet: " + str(np.mean(diffs)))
    print("Mean habitability of settled planet: " + str(np.mean(habs)))
    #"""



