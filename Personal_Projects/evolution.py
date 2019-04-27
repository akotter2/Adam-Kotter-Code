#evolution.py
"""
An attempt at practicing with genetic algorithms.
"""


import numpy as np
from scipy import stats
from scipy import linalg as la


class Creature():
    """This class represents the thing to be evolved. A simulator creates several of 
    these per generation, then selectors eliminate several of these. The survivors 
    populate the next generation with their traits, leaving the next generation in a 
    slightly different state than the first.
    
    Attributes:
        Num (int): The number of attributes
        Mut_rate (float): The rate of mutation, corresponding to the scale of the 
        normal distribution from which mutations are drawn.
        Name_to_Index (dict): A dictionary mapping attribute names to indices.
    (The following are stored at [index] as entries in a vector called attributes)
        Health:
        Strength:
        Viral Tolerance:
        Bacterial Tolerance:
        Toxin Tolerance:
        Fertility:
    
    Functions:
        Permute (None): Causes random changes to the attributes vector based on one 
        of several probability distributions."""
    
    def __init__(self, attr=np.zeros(6), mut_rate=0.1, health=None, strength=None, viral=None, 
                 bacterial=None, toxin=None, fertility=None):
        """Creature constructor. Accepts an array of attributes which defaults to all 
        fives. Also accepts values for individual attributes.
        Parameters:
            Mut_rate (float): The rate of mutation, corresponding to the scale of the 
            normal distribution from which mutations are drawn.
            Health:
            Strength:
            Viral Tolerance:
            Bacterial Tolerance:
            Toxin Tolerance:
            Fertility:"""
        self.attributes = np.full(6,5)
        self.attributes = attr
        self.num = len(attr)
        for i, a in enumerate([health, strength, viral, bacterial, toxin, fertility]):
            if not a is None:
                self.attributes[i] = a
        self.mut_rate = mut_rate
        self.name_to_index = {"health":0, "strength":1, "viral":2, "bacterial":3, "toxin":4, "fertility":5}
    
    def permute(self, distr="normal", center=0., scale=1.):
        """Causes random changes to the attributes vector based on one of several 
        probability distributions.
        Parameters: 
            Distr (str): The probability distribution used to permute the attributes. 
            Can include "normal", "gamma", "beta", and "uniform".
            Center (float): A paramater defining the mean of applicable distributions.
            Scale (float): A paramater defining the variance of applicable 
            distributions.
        Returns:
            Permuted (ndarray): The permuted attributes."""
        #Get the right kind of permutation
        if distr == "normal":
            permutation = np.random.normal(center, scale, self.num)
        elif distr == "uniform":
            permutation = np.random.random(self.num)*(-2)*scale + scale
        elif distr == "gamma":
            raise NotImplementedError("This distribution hasn't been implemented.")
        elif distr == "beta":
            raise NotImplementedError("This distribution hasn't been implemented.")
        else:
            raise ValueError(distr + " isn't a recognized probability distribution.")
        #Permute that bad boy!
        return self.attributes + permutation
    
    def __str__(self):
        return str(self.attributes)


class Selector():
    """This class represents selective forces for driving evolution.
    
    Attributes:
        Mut_rate (float): The rate of mutation, corresponding to the scale of the 
        normal distribution from which mutations are drawn.
        Name_to_Index (dict): A dictionary mapping attribute names to indices.
    (The following are stored at [index] as entries in a vector called attributes)
        Intensity:
        Competition:
        Virality:
        Bacterial Infectivity:
        Toxicity:
        Overcrowding:
    
    Functions:
        Permute (None): Causes random changes to the attributes vector based on one 
        of several probability distributions."""
    
    def __init__(self, attr=np.zeros(6), mut_rate=0.1, intensity=None, competition=None, viral=None, 
                 bacterial=None, toxin=None, overcrowd=None):
        """Selector constructor. Accepts an array of attributes which defaults to all 
        zeros. Also accepts values for individual attributes.
        Parameters:
            Mut_rate (float): The rate of mutation, corresponding to the scale of the 
            normal distribution from which mutations are drawn.
            Health:
            Strength:
            Viral Tolerance:
            Bacterial Tolerance:
            Toxin Tolerance:
            Fertility:"""
        self.attributes = np.zeros(6)
        self.attributes = attr
        self.num = len(attr)
        for i, a in enumerate([intensity, competition, viral, bacterial, toxin, overcrowd]):
            if not a is None:
                self.attributes[i] = a
        self.mut_rate = mut_rate
        self.name_to_index = {"intensity":0, "competition":1, "viral":2, "bacterial":3, "toxin":4, "overcrowd":5}
    
    def permute(self, distr="normal", center=0., scale=0.1):
        """Returns a vector of attributes made from randomly permutating the creature's 
        attributes vector based on one of several probability distributions.
        Parameters: 
            Distr (str): The probability distribution used to permute the attributes. 
            Can include "normal", "gamma", "beta", and "uniform".
            Center (float): A paramater defining the mean of applicable distributions.
            Scale (float): A paramater defining the variance of applicable 
            distributions.
        Returns: 
            Permuted (ndarray): The permuted attributes."""
        #Get the right kind of permutation
        if distr == "normal":
            permutation = np.random.normal(center, scale, self.num)
        elif distr == "uniform":
            permutation = np.random.random(self.num)*(-2)*scale + scale + center
        elif distr == "gamma":
            raise NotImplementedError("This distribution hasn't been implemented.")
        elif distr == "beta":
            raise NotImplementedError("This distribution hasn't been implemented.")
        else:
            raise ValueError(distr + " isn't a recognized probability distribution.")
        #Permute that bad boy!
        return self.attributes + permutation
    
    def __str__(self):
        return str(self.attributes)



class Simulator():
    """A class for managing evolution simulations over several generations.
    
    Attributes:
        -Generation (int): The current iteration of the simulation.
        -Creatures (list): A list of the different creatures in the current iteration 
        of the simulation.
        -Selectors (list)): A list of the different selectors in the current iteration 
        of the simulation.
        -Num_c (int): The number of creatures in the simulation.
        -Num_s (int): The number of selection factors in the simulation.
    
    Functions:
        Step (None): Steps the simulation forward by a generation."""
    
    def __init__(self, num_c=10, num_s=1, creatures=None, selectors=None, 
                   just_one=True, distr="normal", center_c=0., scale_c=1., 
                   center_s=0., scale_s=1., mut_rate_c=0.1, mut_rate_s=0.1):
        """Simulator constructor.
        Parameters:
            -Num_c (int): The number of creatures in the beginning of the simulation. 
            Defaults to 10.
            -Num_s (int): The number of selection factors in the beginning of the 
            simulation. Defaults to 1.
            -Creatures (list: Creature): A list of creatures for generation zero of 
            the simulation. If None, then num_c creatures are randomly generated 
            according to the probability distribution. If not None, then num_c is 
            overwritten with the length of this list.
            -Selectors (list: Selector): A list of selection factors for the 
            simulation. If None, then num_s selectors are randomly generated 
            according to the probability distribution. If not None, then num_s is 
            overwritten with the length of this list.
            -Just_One (bool): Whether or not only the fittest creature will be able 
            to influence the next generation.
            -Distr (str): The probability distribution used to permute the attributes. 
            Can include "normal", "gamma", "beta", and "uniform".
            -Center_C (float): A paramater defining the mean of applicable creature 
            distributions.
            -Scale_C (float): A paramater defining the variance of applicable creature 
            distributions.
            -Center_S (float): A paramater defining the mean of applicable selector 
            distributions.
            -Scale_S (float): A paramater defining the variance of applicable selector 
            distributions.
            -Mut_rate_c (float): The initial rate of creature mutation, corresponding 
            to the scale of the normal distribution from which mutations are drawn.
            -Mut_rate_s (float): The initial rate of selector mutation, corresponding 
            to the scale of the normal distribution from which mutations are drawn.
        """
        #Set the initial generation and just_one conditions
        self.generation = 0
        self.just_one = just_one
        #Populate the creatures list
        if creatures is None:
            self.num_c = num_c
            if distr == "normal":
                self.creatures = [Creature(np.random.normal(center_c, scale_c, 6), 
                       mut_rate_c) for _ in range(num_c)]
            elif distr == "uniform":
                self.creatures = [Creature(np.random.random(6)*(-2)*scale_c + scale_c 
                                        + center_c, mut_rate_c) for _ in range(num_c)]
            elif distr == "gamma":
                raise NotImplementedError("This distribution isn't yet implemented.")
            elif distr == "beta":
                raise NotImplementedError("This distribution isn't yet implemented.")
            else:
                raise ValueError(distr + " isn't a recognized distribution.")
        else:
            self.creatures = creatures
            self.num_c = len(creatures)
            
        #Populate the selectors list
        if selectors is None:
            self.num_s = num_s
            if distr == "normal":
                self.selectors = [Selector(np.random.normal(center_s, scale_s, 6), 
                                                 mut_rate_s) for _ in range(num_s)]
            elif distr == "uniform":
                self.selectors = [Selector(np.random.random(6)*(-2)*scale_s + scale_s + 
                                          center_s, mut_rate_s) for _ in range(num_s)]
            elif distr == "gamma":
                raise NotImplementedError("This distribution isn't yet implemented.")
            elif distr == "beta":
                raise NotImplementedError("This distribution isn't yet implemented.")
            else:
                raise ValueError(distr + " isn't a recognized distribution.")
        else:
            self.selectors = selectors
            self.num_s = len(selectors)
    
    def step(self):
        """Advances the simulation by one generation. Most of the creatures will be 
        removed based on the selective pressures, and the remainder will influence 
        the attributes of the next generation.
        To determine survival, for each attribute of each creature draw from a normal 
        distribution centered at that attribute's value. Compare it with a similar 
        draw centered at each selective pressure's corresponding attribute. If any 
        draw from a selector is greater than a creature's draw, remove that creature.
        Otherwise, keep that creature.
        Future implementations may cause changes in the selective pressures based on 
        the number of creatures present."""
        #Iterate through each creature
        for c in self.creatures:
            #Iterate through each attribute
            for i, a in enumerate(c.attributes):
                c_draw = np.random.normal(a)
                #Iterate through each selector
                for s in self.selectors:
                    s_draw = np.random.normal(s.attributes[i])
                    #Mark the creature for removal if necessary
                    if s_draw >= c_draw:
                        c.attributes[i] = -np.inf
                        break
        #Remove any creature marked for removal
        removed = 0
        i = 0
        while i < len(self.creatures):
            if any([a == -np.inf for a in self.creatures[i].attributes]):
                self.creatures.pop(i)
                removed += 1
            else:
                i += 1
        self.num_c -= removed
        #Repopulate
        if self.just_one:
            pass
        else:
            for c in self.creatures:
                num_offspring = int(np.ceil(c.attributes[c.name_to_index["fertility"]]))
                for _ in range(num_offspring):
                    self.creatures.append(Creature(c.permute(scale=c.mut_rate)))
                self.num_c += num_offspring
        #Update the generation number
        self.generation += 1
        
    
    def __str__(self):
        """Returns a comma-separated string with the current generation, the current 
        list of creatures, and the current list of selectors."""
        return (str(self.generation) + "," + str([str(c) for c in self.creatures]) + 
                                        "," + str([str(s) for s in self.selectors]))








