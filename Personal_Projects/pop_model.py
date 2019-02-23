#pop_model.py
"""A file for testing the use of various systems to model population dynamics.

Classes:
    Projector: A super-class for modeling future conditions based on an initial 
    condition and evolution factors.
    LinAlg (Projector): An extension of Projector that uses linear algebra

Last updated: 1-18-19
"""


import numpy as np
from matplotlib import pyplot as plt


class Projector():
    """Used to model future conditions based on an initial condition and change factors.
    
    Attributes:
        Initial (ndarray (float)): The initial conditions for the scenario, set during 
        object construction.
        Labels (ndarray (str)): A list of labels for the elements of the scenario.
        N (int): The number of elements in the scenario
    
    Functions:
        Perturb (float, str; None): Change some part of the scenario by a semi-random 
        amount.
        Project (int, bool; n-darray (float)): Returns the state of the scenario during 
        a certain number of iterations, optionally plotting a visual representation of 
        the scenario through its iterations.
        Tol (float): How close to zero you can get before redefining the number to be 
        exactly zero.
    """
    
    def __init__(self, initial, labels, tol=0.1):
        """Creates the scenario, defining the initial conditions and the labels of each 
        element in the scenario."""
        #Check for matching attribute lengths
        if len(initial) != len(labels):
            raise ValueError("Element-label length mismatch!")
        self.initial = initial
        self.labels = labels
        self._n = len(initial)
        self.tol = tol
    
    def perturb(self, x):
        NotImplementedError("To be implemented later.")
    
    def project(self, periods, plot=True, log=False):
        """See class docstring."""
        #Store the initial conditions
        timeline = np.zeros((periods+1, self._n))
        #This is generic, so just copy the initial conditions repeatedly
        for i in range(periods+1):
            timeline[i] = self.initial
        #Plot, if applicable
        if not plot:
            return timeline
        if log:
            for j in range(self._n):
                plt.semilogy(timeline[:,j], label=self.labels[j])
        else:
            for j in range(self._n):
                plt.plot(timeline[:,j], label=self.labels[j])
        plt.legend()
        plt.xlabel("Periods")
        plt.ylabel("Population")
        plt.title("Population of Elements by Period")
        plt.show()
        return timeline



class LinAlg(Projector):
    """An extension of the Projector class that uses linear algebra to model population 
    dynamics.
    
    Attributes:
        Initial (ndarray (float)): The initial conditions for the scenario, set during 
        object construction.
        Evolution (nxn array (float)): A matrix representing the relationships between 
        the various elements of the scenario.
        OverPop (bool): Whether or not to account for overpopulation in the scenario.
        PopBounds (ndarray (float)): Criteria that determine whether or not the 
        elements of the scenario are in overpopulation or not.
        Stress (ndarray (float)): Overpopulation effects that happen when criteria in 
        the PopBounds matrix are reached.
    """

    def __init__(self, initial, evolution, labels, overpop=False, popbounds=None, stress=None, tol=0.1):
        """Creates the scenario, defining the initial conditions and the relationships 
        that determine the evolution of the scenario."""
        #Check for matching attribute lengths
        if len(initial) != len(evolution):
            raise ValueError("Non-equal number of elements in initial conditions and "
                              "evolution matrix!")
        if len(evolution[0]) != len(evolution):
            raise ValueError("Evolution matrix must be square!")
        Projector.__init__(self, initial, labels, tol)
        self.evolution = evolution
        #Account for overpopulation, if applicable
        if overpop:
            self.overpop = True
            if stress is None:
                self.stress = np.full((self._n, self._n), 1)
            else:
                self.stress = stress
            if popbounds is None:
                self.popbounds = np.full((self._n, self._n), 1)
            else:
                self.popbounds = popbounds
        else:
            self.overpop = False
            self.stress = None
            self.popbounds = None
    
    def project(self, periods, plot=True, log=False):
        """See class docstring."""
        #Store the initial conditions
        timeline = np.zeros((periods+1, self._n))
        timeline[0] = self.initial
        current = self.initial
        #Iterate, multiply, and store until the last period
        for i in np.arange(1, periods+1):
            current = self.evolution@current
            for j in range(self._n):
                if current[j] < self.tol:
                    current[j] = 0
            #Apply overpopulation conditions
            if self.overpop:
                for j in range(self._n):
                    for k in np.delete(np.arange(self._n), j):
                        diff = current[j] - current[k]*self.popbounds[j,k]
                        #Debugging
                        """
                        print(self.labels[j] + " difference with " + self.labels[k] + ": " + str(diff))
                        #"""
                        if diff > 0:
                            #Debugging
                            """
                            print(self.labels[j] + " lost " + str(diff*self.stress[j,k]) + 
                            " population because of overpopulation effects with " + self.labels[k])
                            #"""
                            current[j] -= diff*self.stress[j,k]
                        if current[j] < self.tol:
                            current[j] = 0
            timeline[i] = current
            #For debugging purposes
            """
            print("Period " + str(i) + ":" + str(timeline[i]))
            #"""
        #Plot, if applicable
        #For debugging purposes
        """
        for i in range(periods):
            for j in range(self._n):
                print(self.labels[j] + " at period " + str(i) + ": " + str(timeline[i,j]))
        #"""
        if not plot:
            return timeline
        if log:
            for j in range(self._n):
                plt.semilogy(timeline[:,j], label=self.labels[j])
        else:
            for j in range(self._n):
                plt.plot(timeline[:,j], label=self.labels[j])
        plt.legend()
        plt.xlabel("Periods")
        plt.ylabel("Population")
        plt.title("Population of Elements by Period")
        plt.show()
        return timeline



class OverPop(Projector):
    """An extension of the Projector class that accounts for overpopulation effects in 
    modeling population dynamics.
    
    Attributes:
        Initial (ndarray (float)): The initial conditions for the scenario, set during 
        object construction.
        Evolution (ndarray (float)): The relationships determining the evolution of 
        the scenario."""

    
    def __init__(self, initial, growth, evolution, labels):
        """Creates the scenario, defining the initial conditions and the relationships 
        that determine the evolution of the scenario."""
        #Check for matching attribute lengths
        if len(initial) != len(evolution):
            raise ValueError("Non-equal number of elements in initial conditions and "
                              "evolution matrix!")
        if len(evolution[0]) != len(evolution):
            raise ValueError("Evolution matrix must be square!")
        Projector.__init__(self, initial, labels)
        self.evolution = evolution
    
    def project(self, periods, plot=True, log=False):
        """See class docstring."""
        #Store the initial conditions
        timeline = np.zeros((periods+1, self._n))
        timeline[0] = self.initial
        current = self.initial
        new = np.zeros(self._n)
        #Iterate, multiply, and store until the last period
        for i in np.arange(1, periods+1):
            for j in range(self._n):
                for k in np.delete(np.arange(self._n), j):	
                    pass
            current = self.evolution@current
            timeline[i] = current
        #Plot, if applicable
        if not plot:
            return timeline
        if log:
            for j in range(self._n):
                plt.semilogy(timeline[:,j], label=self.labels[j])
        else:
            for j in range(self._n):
                plt.plot(timeline[:,j], label=self.labels[j])
        plt.legend()
        plt.xlabel("Periods")
        plt.ylabel("Population")
        plt.title("Population of Elements by Period")
        plt.show()
        return timeline



