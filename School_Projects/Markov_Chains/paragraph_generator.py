#paragraph_generator.py
"""A modification of the markov_chains.py file that creates random paragraphs, not just 
random sentences."""

import numpy as np

class ParagraphGenerator():
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
        line_transition ((nxn) ndarray): the transition matrix corresponding the end 
        of one line to the beginning of the next.

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
        #Initialize the line transition matrix
        self.line_transition = np.zeros([num_words+2, num_words+2])
        #Fill the line transition matrix
        for i in range(len(sentences)-1):
            words1 = sentences[i].split()
            words2 = sentences[i+1].split()
            if words1 == []:
                continue
            if words2 == []:
                self.line_transition[self.to_index["$top"], self.to_index[words1[-1]]] += 1
            else:
                self.line_transition[self.to_index[words2[0]], self.to_index[words1[-1]]] += 1
        self.line_transition[self.to_index["$top"], self.to_index["$top"]] = 1
        #Normalize the columns of the line transition matrix
        for i in range(num_words+2):
            self.line_transition[:,i] /= sum(self.line_transition[:,i])

            
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

    def specific_babble(self, starter):
        """Create a random sentence beginning with a specific word in the training set."""
        #Set current to index of "$tart" and initialize the sentence
        try:
            self.to_index[starter]
        except Exception:
            starter = "$tart"
        current = self.to_index[starter]
        sentence = [starter]
        if starter == "$tart":
            sentence.remove("$tart")
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
        

    def continuous_babble(self):
        """Babble until the end of a paragraph is reached. Returns a list of strings 
        where each string is a sentence."""
        #Get a sentence
        sentence = self.babble()
        words = sentence.split()
        #Set current to index of the last word and initialize the paragraph
        current = self.to_index[words[-1]]
        paragraph = [sentence]
        #Transition from sentence to sentence until "$top" is reached
        while current != self.to_index["$top"]:
            next = np.random.multinomial(1, self.line_transition[:, int(current)])  #list
            current = np.argmax(next)  #int
            if current == self.to_index["$top"]:
                break
            new_sentence = self.specific_babble(self.from_index[current])  #str
            paragraph.append(new_sentence)  #str
            new_words = new_sentence.split()
            current = self.to_index[new_words[-1]]
        return paragraph

#For testing porpoises only
if __name__ == "__main__":
    #for i in range(1,11):
        #print(random_chain(i)
        #print(forecast(i))
        #print(four_state_forecast(i))
    PG = ParagraphGenerator("yoda.txt")
    stanza = PG.continuous_babble()
    for line in stanza:
        print(line)