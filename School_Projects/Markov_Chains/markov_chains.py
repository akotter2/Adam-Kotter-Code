# markov_chains.py
"""Volume II: Markov Chains.
Adam Kotter
Math 321-1
11-1-18
"""

import numpy as np
from scipy import linalg as la


# Problem 1
def random_chain(n):
    """Create and return a transition matrix for a random Markov chain with
    'n' states. This should be stored as an nxn NumPy array.
    """
    #Get a random vector
    M = np.random.random((n,n))
    #Make each column sum to 1
    for i in range(n):
        M[:,i] /= sum(M[:,i])
    return M


# Problem 2
def forecast(days):
    """Forecast the weather for a given number of days given that today is hot.
        Parameters: days (int): The number of days over which to run the forecast.
        Returns: predictions (list): The day-by-day weather predictions, with 0 
            representing "hot" and 1 representing "cold"."""
    #Set probabilities and today's weather
    transition = np.array([[0.7, 0.6], [0.3, 0.4]])
    today = 0
    predictions = []
    #Each day select the appropriate probability and predict the weather
    for _ in range(days):
        today = np.random.binomial(1, transition[1,today])
        predictions.append(today)
    return predictions


# Problem 3
def four_state_forecast(days):
    """Run a simulation for the weather over the specified number of days,
    with mild as the starting state, using the four-state Markov chain.
    Return a list containing the day-by-day results, not including the
    starting day.
    Weather states: Hot(0), Mild(1), Cold(2), Freezing(3).
    This is not a fun place to live.

    Examples:
        >>> four_state_forecast(3)
        [0, 1, 3]
        >>> four_state_forecast(5)
        [2, 1, 2, 1, 1]
    """
    #Set probabilities and today's weather
    weather_probs = np.array([[0.5,0.3,0.1,0],[0.3,0.3,0.3,0.3],[0.2,0.3,0.4,0.5],[0,0.1,0.2,0.2]])
    today = 1
    predictions = []
    #Each day select the appropriate probability and predict the weather
    for _ in range(days):
        which_weather = np.random.multinomial(1, weather_probs[:,today])
        today = np.argmax(which_weather)
        predictions.append(today)
    return predictions


# Problem 4
def steady_state(A, tol=1e-12, N=40):
    """Compute the steady state of the transition matrix A.

    Inputs:
        A ((n,n) ndarray): A column-stochastic transition matrix.
        tol (float): The convergence tolerance.
        N (int): The maximum number of iterations to compute.

    Raises:
        ValueError: if the iteration does not converge within N steps.

    Returns:
        x ((n,) ndarray): The steady state distribution vector of A.
    """
    #Make a random state distribution vector
    x = np.random.random(len(A))
    x /= sum(x)
    #Iterate until steady state distribution is found or max iterations reached
    for k in range(N):
        x_next = A@x
        if la.norm(x - x_next) < tol:
            return x
        x = x_next
    raise ValueError("A^k does not converge!")


# Problems 5 and 6
class SentenceGenerator(object):
    """Markov chain creator for simulating bad English.

    Attributes:
        to_index (dict): a dictionary corresponding words to indices in the transition 
        matrix.
        from_index (dict): a dictionary corresponding indices in the transition matrix 
        to words.
        transition ((nxn) ndarray): the transition matrix corresponding to the 
        specified training set. The [i,j] entry of the matrix represents the 
        likelihood of the word with index j being followed by the word with index i 
        in the states dictionary.

    Example:
        >>> yoda = SentenceGenerator("Yoda.txt")
        >>> print(yoda.babble())
        The dark side of loss is a path as one with you.
    """
    def __init__(self, filename):
        """Read the specified file and build a transition matrix from its
        contents. You may assume that the file has one complete sentence
        written on each line.
        """
        #Read in the sentences of the training set
        with open(filename, "r") as file:
            sentences = file.readlines()
        #Count all the unique words in the training set
        unique_words = set()
        for line in sentences:
            for word in line.split():
                unique_words.add(word)
        num_words = len(unique_words)
        #Initialize the transition matrix
        self.transition = np.zeros([num_words+2, num_words+2])
        #Initialize a dictionary corresponding words to indices
        self.to_index = {"$tart":0}
        for i,word in enumerate(unique_words):
            self.to_index[word] = i + 1
        self.to_index["$top"] = num_words + 1
        #Initialize a dictionary corresponding indices to words
        self.from_index = {0:"$tart"}
        for i,word in enumerate(unique_words):
            self.from_index[i+1] = word
        self.from_index[num_words + 1] = "$top"
        #Fill the transition matrix
        for sentence in sentences:
            words = sentence.split()
            if words == []:
                continue
            self.transition[self.to_index[words[0]], self.to_index["$tart"]] += 1
            for i in range(len(words)-1):
                self.transition[self.to_index[words[i+1]], self.to_index[words[i]]] += 1
            self.transition[self.to_index["$top"], self.to_index[words[-1]]] += 1
        self.transition[self.to_index["$top"],self.to_index["$top"]] = 1
        #Normalize the columns of the transition matrix
        for i in range(num_words+2):
            self.transition[:,i] /= sum(self.transition[:,i])
            
    def babble(self):
        """Begin at the start state and use the strategy from
        four_state_forecast() to transition through the Markov chain.
        Keep track of the path through the chain and the corresponding words.
        When the stop state is reached, stop transitioning and terminate the
        sentence. Return the resulting sentence as a single string.
        """
        #Set current to index of "$tart" and initialize the sentence
        current = self.to_index["$tart"]
        sentence = []
        #Transition from word to word until "$top" is reached
        while current != self.to_index["$top"]:
            next = np.random.multinomial(1, self.transition[:,current])  #list
            current = np.argmax(next)  #int
            sentence.append(self.from_index[current])  #str
        sentence.remove("$top")
        #Convert list of words in the sentence into a single string
        sentence_str = str()
        for word in sentence:
            sentence_str += word + " "
        return sentence_str

#For testing porpoises only
if __name__ == "__main__":
    #for i in range(1,11):
        #print(random_chain(i)
        #print(forecast(i))
        #print(four_state_forecast(i))
    SG = SentenceGenerator("trump.txt")
    done = False
    while not done:
        stuff = input("Continue? ")
        if stuff == "no":
            done = True
        print(SG.babble())