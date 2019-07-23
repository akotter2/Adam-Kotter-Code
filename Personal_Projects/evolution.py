#evolution.py
"""
An attempt at practicing with genetic algorithms.
"""



import numpy as np
from scipy import stats
from scipy import linalg as la
from matplotlib import pyplot as plt



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
        Index_to_Name (dict): A dictionary mapping attribute indices to names.
    (The following are stored at [index] as entries in a vector called attributes)
        Temp:
        Strength:
        Viral Tolerance:
        Bacterial Tolerance:
        Toxin Tolerance:
        Fertility:
    
    Functions:
        Permute (None): Causes random changes to the attributes vector based on one 
        of several probability distributions."""
    
    
    def __init__(self, attr=np.zeros(7), mut_rate=0.1, temp=None, strength=None, 
                   viral=None, bacterial=None, toxin=None, fertility=None):
        """Creature constructor. Accepts an array of attributes which defaults to all 
        zeros. Also accepts values for individual attributes.
        Parameters:
            Mut_rate (float): The rate of mutation, corresponding to the scale of the 
            normal distribution from which mutations are drawn.
            Temp:
            Strength:
            Viral Tolerance:
            Bacterial Tolerance:
            Toxin Tolerance:
            Fertility:"""
        
        #Catch potential errors
        n = len(attr)
        if n != 7:
            raise ValueError("Creatures have seven attributes, not " + str(n) + "!")
        
        #Define attributes
        self.attributes = attr
        self.num = n
        for i, a in enumerate([temp, strength, viral, bacterial, toxin, fertility, mut_rate]):
            if not a is None:
                self.attributes[i] = a
        self.name_to_index = {"temp":0, "strength":1, "viral":2, "bacterial":3, 
                                              "toxin":4, "fertility":5, "mut_rate":6}
        self.index_to_name = {0:"temp", 1:"strength", 2:"viral", 3:"bacterial", 
                                              4:"toxin", 5:"fertility", 6:"mut_rate"}
    
    
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
        Temp:
        Predator:
        Virality:
        Bacterial Infectivity:
        Toxicity:
        Overcrowding:
    
    Functions:
        Permute (None): Causes random changes to the attributes vector based on one 
        of several probability distributions."""
    
    
    def __init__(self, attr=np.zeros(7), mut_rate=0.1, temp=None, predator=None, 
                 viral=None, bacterial=None, toxin=None, overcrowd=None):
        """Selector constructor. Accepts an array of attributes which defaults to all 
        zeros. Also accepts values for individual attributes.
        Parameters:
            Mut_rate (float): The rate of mutation, corresponding to the scale of the 
            normal distribution from which mutations are drawn.
            Temp:
            Predator:
            Viral Tolerance:
            Bacterial Tolerance:
            Toxin Tolerance:
            Overcrowding:"""
        
        #Catch potential errors
        n = len(attr)
        if n != 7:
            raise ValueError("Selectors have seven attributes, not " + str(n) + "!")
        self.attributes = attr
        self.num = n
        for i, a in enumerate([temp, predator, viral, bacterial, toxin, overcrowd, mut_rate]):
            if not a is None:
                self.attributes[i] = a
        self.name_to_index = {"temp":0, "predator":1, "viral":2, "bacterial":3, 
                                              "toxin":4, "overcrowd":5, "mut_rate":6}
        self.index_to_name = {0:"temp", 1:"predator", 2:"viral", 3:"bacterial", 
                                              4:"toxin", 5:"overcrowd", 6:"mut_rate"}
    
    
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
        -Capacity (int): The number of creatures that the simulation can support.
        -Cap_scale (float): The variability of the range in which overpopulation 
        begins to adversely affect the creatures in the simulation, corresponding to 
        the scale of a normal distribution.
    
    Functions:
        Step (None): Steps the simulation forward by a generation.
        Run (None): Steps the simulation forward several generations and plots the 
        average attributes of each generation."""
    
    
    def __init__(self, num_c=10, num_s=1, capacity=1000, cap_scale=100, 
                   creatures=None, selectors=None, just_one=True, distr="normal", 
                   center_c=0., scale_c=1., center_s=0., scale_s=1., mut_rate_c=0.1, 
                   mut_rate_s=0.1):
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
        
        #Set numeric attributes
        self.generation = 0
        self.just_one = just_one
        self.capacity = capacity
        self.cap_scale = cap_scale
        
        #Populate the creatures list
        if creatures is None:
            self.num_c = num_c
            if distr == "normal":
                self.creatures = [Creature(np.random.normal(center_c, scale_c, 7), 
                       mut_rate=mut_rate_c) for _ in range(num_c)]
            elif distr == "uniform":
                self.creatures = [Creature(np.random.random(7)*(-2)*scale_c + scale_c 
                              + center_c, mut_rate=mut_rate_c) for _ in range(num_c)]
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
                self.selectors = [Selector(np.random.normal(center_s, scale_s, 7), 
                                          mut_rate=mut_rate_s) for _ in range(num_s)]
            elif distr == "uniform":
                self.selectors = [Selector(np.random.random(7)*(-2)*scale_s + scale_s 
                                       + center_s, mut_rate_s) for _ in range(num_s)]
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
        To determine survival, for each attribute of each creature (except for 
        fertility and mutation rate) draw from a normal distribution centered at that 
        attribute's value. Compare it with a similar draw centered at each selective 
        pressure's corresponding attribute. If any draw from a selector is greater 
        than a creature's draw, remove that creature. Otherwise, keep that creature.
        Future implementations may cause changes in the selective pressures based on 
        the number of creatures present."""
        
        #Iterate through each creature
        for c in self.creatures:
            #Iterate through each attribute except for disallowed ones
            skipped_attr = ["mut_rate", "fertility"]
            for i, a in enumerate(c.attributes):
                if c.index_to_name[i] in skipped_attr:
                    continue
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
        
        #Account for population effects
        for s in self.selectors:
            s_draw = np.random.normal(s.attributes[s.name_to_index["overcrowd"]])
            cap = self.capacity - self.cap_scale*s_draw
            if self.num_c > cap and self.num_c > 0:
                #How strong must you be to survive?
                frac_overpop = (self.num_c - cap)/self.num_c
                avg_str = np.average([c.attributes[c.name_to_index["strength"]] for 
                                                                c in self.creatures])
                cut_off = stats.norm.ppf(avg_str*frac_overpop, loc=avg_str)
                for c in self.creatures:
                    #Mark the outcompeted creatures
                    c_draw = np.random.normal(c.attributes[c.name_to_index["strength"]])
                    if c_draw < cut_off:
                        c.attributes[c.name_to_index["strength"]] = -np.inf
        
        #Remove any creature marked for removal
        removed = 0
        i = 0
        while i < len(self.creatures):
            if self.creatures[i].attributes[c.name_to_index["strength"]] == -np.inf:
                self.creatures.pop(i)
                removed += 1
            else:
                i += 1
        self.num_c -= removed
        
        #Repopulate
        if self.just_one:
            pass
        else:
            add_list = []
            for c in self.creatures:
                offspring_center = c.attributes[c.name_to_index["fertility"]]
                num_offspring = int(np.ceil(np.random.normal(offspring_center, 0.5)))
                for _ in range(num_offspring):
                    add_list.append(Creature(c.permute(scale=
                                        c.attributes[c.name_to_index["mut_rate"]])))
                if num_offspring > 0:
                    self.num_c += num_offspring
            for c in add_list:
                self.creatures.append(c)
        
        #Update the generation number
        self.generation += 1
    
    
    def run(self, gen_max=25, return_num=False):
        """Steps the simulation forward until either the creatures die out or the 
        maximum number of generations is reached, then plots the average attributes as 
        a function of generation.
        Parameters:
        -Gen_max (int): The maximum number of steps allowed.
        -Return_num (bool): Whether or not to return the number of creatures at each 
        generation.
        Returns:
        -Averages (ndarray): The average attributes at each generation.
        -Num_C (list): The number of creatures at each generation.
        """
        
        #Initialize arrays and such
        averages = np.average(np.vstack([c.attributes for c in self.creatures]), 
                                                                            axis=0)
        att_ind_to_name = self.creatures[0].index_to_name
        if return_num:
            num_c = [self.num_c]
        while self.num_c > 0 and self.generation < gen_max:
            try:
                #Step and record the averages
                self.step()
                if return_num:
                    num_c.append(self.num_c)
                    print(self.num_c)
                if self.num_c <= 0:
                    break
                averages = np.vstack([averages, np.average(np.vstack([c.attributes for 
                                                    c in self.creatures]), axis=0)])
            except KeyboardInterrupt:
                break
        
        #Plot and return the averages
        two_d = True
        try:
            n = averages.shape[1]
        except IndexError:
            two_d = False
            n = len(averages)
        a = round(np.sqrt(n))
        b = np.ceil(np.sqrt(n))
        for i in range(n):
            plt.subplot(a, b, i+1)
            plt.title(att_ind_to_name[i])
            if two_d:
                plt.plot(averages[:,i])
            else:
                plt.plot(averages[i])
            plt.xlabel("Generation")
            plt.ylabel(att_ind_to_name[i] + " value")
        plt.suptitle("Average Attributes by Generation")
        plt.tight_layout()
        plt.show()
        if return_num:
            plt.plot(num_c)
            plt.title("Population")
            plt.xlabel("Generation")
            plt.ylabel("Population")
            plt.show()
            return averages, num_c
        return averages
    
    
    def __str__(self):
        """Returns a comma-separated string with the current generation, the current 
        list of creatures, and the current list of selectors."""
        return (str(self.generation) + "," + str([str(c) for c in self.creatures]) + 
                                        "," + str([str(s) for s in self.selectors]))








