#book_of_mormon_words.py
"""An adaptation of paragraph_generator.py. This file is designed to parse selected 
verses and chapters from the Book of Mormon and analyze the different linguistic 
styles of the different narrators present. When complete, this will include a text 
generator to see if a human can tell which author is speaking and a statistical 
analysis method for determining the differences between the styles of the different 
writers."""


# Import needed modules
import re
import sys
import time
import requests
import numpy as np


def download_full_text():
    """Request and return the full text of The Book of Mormon (and some legalese) 
    from the Project Gutenberg website."""
    # Download the needed text
    url = "http://www.gutenberg.org/cache/epub/17/pg17.txt"
    full_text = requests.get(url).text.splitlines()
    return full_text


def reference_regex(book, chap_start="1", chap_end=None, verse_start="1", 
                    verse_end=None):
    """Compiles a regex for Book of Mormon references.
    
    Parameters: 
        book (str): The book in The Book of Mormon from which the text is to be 
            drawn. The "Nephi" books are formatted as "1 Nephi".
        chap_start (str): The first chapter in the aforementioned book from which the 
            text is to be drawn, formatted as a numeral. Default is "1".
        chap_end (str): The last chapter in the aforementioned book from which the 
            text is to be drawn, formatted as a numeral. Default is None, indicating 
            the last chapter of the book. If the last chapter indicated is not in the 
            book, then the last chapter actually in the book will be used.
        verse_start (str): The first verse in the aforementioned chapter(s) from 
            which the text is to be drawn, formatted as a numeral. Default is "1".
        verse_end (str): The last verse is the aforementioned chapter(s) from which 
            the text is to be drawn, formatted as a numeral. Default is None, 
            indicating the last verse of the chapter. If multiple chapters are 
            selected, this range of verses will be selected from each chapter. If the 
            last verse indicated is not in the chapter(s), then the last verse 
            actually in the chapters will be used.
    
    Returns:
        finder (compiled regex): A regex for the selected reference."""
    # Check for a valid book name
    valid_books = ["1 Nephi", "2 Nephi", "Jacob", "Enos", "Jarom", "Omni", 
                   "Words of Mormon", "Mosiah", "Alma", "Helaman", "3 Nephi", 
                   "4 Nephi", "Mormon", "Ether", "Moroni"]
    if book not in valid_books:
        raise ValueError("Given book {} not in The Book of Mormon.".format(book))
    
    # Triple-digit chapter number and verse number support not yet available
    if len(chap_start) > 2:
        raise ValueError("Support for triple-digit chapter numbers not yet available")
    if chap_end is not None:
        if len(chap_end) > 2:
            raise ValueError("Support for triple-digit chapter numbers not yet available")
    if len(verse_start) > 2:
        raise ValueError("Support for triple-digit verse numbers not yet available")
    if verse_end is not None:
        if len(verse_end) > 2:
            raise ValueError("Support for triple-digit verse numbers not yet available")
    
    # Break the problem up into cases based on end chapters and verses
    
    # All chapters
    if chap_start == "1" and chap_end is None:
        chapter_regex = "\d+"
    
    # First chapter to another chapter
    elif chap_start == "1" and chap_end is not None:
        # Single-digit last chapter
        if len(chap_end) == 1:
            chapter_regex = "[1-{}]".format(chap_end)
        # Last chapter between 10 and 19
        elif chap_end[0] == "1":
            chapter_regex = "([1-9]|1[0-{}])".format(chap_end[1])
        # Last chapter between 20 and 99
        else:
            chapter_regex = "([1-9]|[1-{}]\d|{}[0-{}])".format(chap_end[0]-1, 
                                                             chap_end[0], chap_end[1])
    
    # Middle chapter to end
    elif chap_start != "1" and chap_end is None:
        # Single-digit first chapter
        if len(chap_start) == 1:
            chapter_regex = "([{}-9]|\d\d)".format(chap_start)
        # First chapter between 10 and 89
        elif int(chap_start[0]) < 9:
            chapter_regex = "({}[{}-9]|[{}-9]\d)".format(chap_start[0], 
                                                       chap_start[1], chap_start[0]+1)
        # First chapter between 90 and 99
        else:
            chapter_regex = "9[{}-9]".format(chap_start[1])
    
    # Middle chapter to middle chapter
    elif chap_start != "1" and chap_end is not None:
        # Single-digit first and last chapter
        if len(chap_start) == 1 and len(chap_end) == 1:
            chapter_regex = "[{}-{}]".format(chap_start, chap_end)
        # Single-digit first chapter, double-digit last chapter
        elif len(chap_start) == 1 and len(chap_end) != 1:
            # Last chapter between 10 and 19
            if int(chap_end[0]) < 2:
                chapter_regex = "([{}-9]|1[0-{}])".format(chap_start, chap_end[1])
            # Last chapter between 20 and 99
            else:
                chapter_regex = "([{}-9]|[1-{}]\d|{}[0-{}])".format(chap_start, 
                                                             chap_end[0]-1, 
                                                             chap_end[0], chap_end[1])
        # Double-digit first and last chapters
        else:
            # First and last chapters in same ten-chapter block
            if chap_start[0] == chap_end[0]:
                chapter_regex = "{}[{}-{}]".format(chap_start[0], chap_start[1], 
                                                   chap_end[1])
            # First and last chapters in non-contiguous ten-chapter blocks
            elif int(chap_end[0]) - int(chap_start[0]) > 1:
                chapter_regex = "({}[{}-9]|[{}-{}]\d|{}[0-{}])".format(chap_start[0], 
                                                      chap_start[1], chap_start[0]+1, 
                                                      chap_end[0]-1, chap_end[0], 
                                                      chap_end[1])
            # First and last chapters in contiguous ten-chapter blocks
            else:
                chapter_regex = "({}[{}-9]|{}[0-{}])".format(chap_start[0], 
                                                      chap_start[1], chap_end[0], 
                                                      chap_end[1])
    
    # All verses
    if verse_start == "1" and verse_end is None:
        verse_regex = "\d+"
    
    # First verse to another verse
    elif verse_start == "1" and verse_end is not None:
        # Single-digit last verse
        if len(verse_end) == 1:
            verse_regex = "[1-{}]".format(verse_end)
        # Last verse between 10 and 19
        elif verse_end[0] == "1":
            verse_regex = "([1-9]|1[0-{}])".format(verse_end[1])
        # Last verse between 20 and 99
        else:
            verse_regex = "([1-9]|[1-{}]\d|{}[0-{}])".format(verse_end[0]-1, 
                                                           verse_end[0], verse_end[1])
    
    # Middle verse to end
    elif verse_start != "1" and verse_end is None:
        # Single-digit first verse
        if len(verse_start) == 1:
            verse_regex = "([{}-9]|\d\d)".format(verse_start)
        # First verse between 10 and 89
        elif verse_start[0] < 9:
            verse_regex = "({}[{}-9]|[{}-9]\d)".format(verse_start[0], verse_start[1], 
                                                       verse_start[0]+1)
        # First chapter between 90 and 99
        else:
            verse_regex = "9[{}-9]".format(verse_start[1])
    
    # Middle verse to middle verse
    elif verse_start != "1" and verse_end is not None:
        # Single-digit first and last verses
        if len(verse_start) == 1 and len(verse_end) == 1:
            verse_regex = "[{}-{}]".format(verse_start, verse_end)
        # Single-digit first verse, double-digit last verse
        elif len(verse_start) == 1 and len(verse_end) != 1:
            # Last verse between 10 and 19
            if int(verse_end[0]) < 2:
                verse_regex = "([{}-9]|1[0-{}])".format(verse_start, verse_end[1])
            # Last verse between 20 and 99
            else:
                verse_regex = "([{}-9]|[1-{}]\d|{}[0-{}])".format(verse_start, 
                                                           verse_end[0]-1, 
                                                           verse_end[0], verse_end[1])
        # Double-digit first and last verses
        else:
            # First and last verses in same ten-chapter block
            if verse_start[0] == verse_end[0]:
                verse_regex = "{}[{}-{}]".format(verse_start[0], verse_start[1], 
                                                   verse_end[1])
            # First and last verses in non-contiguous ten-verse blocks
            elif int(verse_end[0]) - int(verse_start[0]) > 1:
                verse_regex = "({}[{}-9]|[{}-{}]\d|{}[0-{}])".format(verse_start[0], 
                                                    verse_start[1], verse_start[0]+1, 
                                                    verse_end[0]-1, verse_end[0], 
                                                    verse_end[1])
            # First and last verses in contiguous ten-verse blocks
            else:
                verse_regex = "({}[{}-9]|{}[0-{}])".format(verse_start[0], 
                                                      verse_start[1], verse_end[0], 
                                                      verse_end[1])
    
    # Compile and the regex
    regex_string = "^"+book+" "+chapter_regex+":"+verse_regex+"$"
    finder = re.compile(regex_string)
    return finder


def text_getter(book, chap_start="1", chap_end=None, verse_start="1", verse_end=None):
    """A method for getting selected chapters and verses from a given book in The 
    Book of Mormon. This method accesses the text found online at 
    http://www.gutenberg.org/cache/epub/17/pg17.txt.
    
    Parameters: 
        book (str): The book in The Book of Mormon from which the text is to be 
            drawn. The "Nephi" books are formatted as "1 Nephi".
        chap_start (str): The first chapter in the aforementioned book from which the 
            text is to be drawn, formatted as a numeral. Default is "1".
        chap_end (str): The last chapter in the aforementioned book from which the 
            text is to be drawn, formatted as a numeral. Default is None, indicating 
            the last chapter of the book. If the last chapter indicated is not in the 
            book, then the last chapter actually in the book will be used.
        verse_start (str): The first verse in the aforementioned chapter(s) from 
            which the text is to be drawn, formatted as a numeral. Default is "1".
        verse_end (str): The last verse is the aforementioned chapter(s) from which 
            the text is to be drawn, formatted as a numeral. Default is None, 
            indicating the last verse of the chapter. If multiple chapters are 
            selected, this range of verses will be selected from each chapter. If the 
            last verse indicated is not in the chapter(s), then the last verse 
            actually in the chapters will be used.
    
    Returns:
        ref_text (list): a list of strings containing the reference text but not any 
            of the references."""
    
    # Get the full text
    full_text = download_full_text()
    
    # Get the regex for the text
    text_finder = reference_regex(book, chap_start, chap_end, verse_start, verse_end)
    
    # Scan each reference and add the ones with valid references
    text_len = len(full_text)
    ref_text = []
    for i, line in enumerate(full_text):
        if text_finder.search(line):
            # Combine the relevant lines into one verse
            new_verse = " "
            temp_lines = []
            j = i+1
            while full_text[j] != "" and text_finder.search(full_text[j]) is None:
                temp_lines.append(full_text[j].lstrip())
                j += 1
            new_verse = new_verse.join(temp_lines)
            ref_text.append(new_verse)
    
    # Strip out verse numbers (single- and double-digit) and initial white space
    for i, line in enumerate(ref_text):
        if line[0].isdigit():
            while ref_text[i][0].isdigit():
                ref_text[i] = ref_text[i][2:]
            ref_text[i] = ref_text[i].lstrip()
    
    # Return the complete text of the references
    return ref_text


def speaker_getter(name):
    """Searches the BoM_by_Speaker.txt file (obtained from the Church Historical 
    Document Corpus at https://bcgmaxwell.wordpress.com/book-of-mormon-by-authors/
    book-of-mormon-annotated-by-author-and-speaker/) for every instance of words by 
    the given speaker.
    
    Parameters:
        name (str): The name of the speaker to search for. If multiple speakers with 
            the same name exist, then must be formatted as "Name #", as in the case 
            of "Moroni 2".
    
    Returns:
        text (list): A list of verses (str) corresponding to the given speaker. 
            Returns an empty list if the given speaker doesn't exist."""
    
    # Initialize the list and current speaker index
    text = []
    current = ""
    
    # Define a regex for getting speakers and for switching speakers
    new_speaker = re.compile(r"\[([\w ]*)\[")
    switch_speaker = re.compile(r"\]\] ?")
    
    # Get the text of The Book of Mormon
    with open("BoM_by_Speaker.txt", "r") as file:
        verses = file.readlines()
        # Run through each verse
        for verse in verses:
            pass
        # Check for switches in speaker
        # If the current speaker is the right one, save that part of the verse


class TextGenerator():
    """Markov chain creator for simulating text from Book of Mormon authors.

    Attributes:
        to_index (dict): a dictionary corresponding words to indices in the text's
            transition matrix.
        from_index (dict): a dictionary corresponding indices in the transition 
            matrix to words.
        transition ((nxn) ndarray): the transition matrix corresponding to the 
            specified text. The [i,j] entry of the matrix represents the likelihood 
            of the word with index j being followed by the word with index i in the 
            to/from_index dictionaries.
        verse_transition ((nxn) ndarray): the transition matrix corresponding the end 
            of one verse to the beginning of the next.
    
    Functions:
        simulate_verse
        simulate_specific_verse
        simulate_chapter
        simulate_specific_chapter
        
    """
    def __init__(self, verses):
        """Reads the specified text and builds a transition matrix from its contents. 
        Text must be broken into a list of verses."""
        #Count all the unique words in the text
        unique_words = set()
        for verse in verses:
            for word in verse.split():
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
        for verse in verses:
            words = verse.split()
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
        #Initialize the verse transition matrix
        self.verse_transition = np.zeros([num_words+2, num_words+2])
        #Fill the verse transition matrix
        for i in range(len(verses)-1):
            words1 = verses[i].split()
            words2 = verses[i+1].split()
            if words1 == []:
                continue
            if words2 == []:
                self.verse_transition[self.to_index["$top"], self.to_index[words1[-1]]] += 1
            else:
                self.verse_transition[self.to_index[words2[0]], self.to_index[words1[-1]]] += 1
        self.verse_transition[self.to_index["$top"], self.to_index["$top"]] = 1
        #Normalize the columns of the verse transition matrix
        for i in range(num_words+2):
            self.verse_transition[:,i] /= sum(self.verse_transition[:,i])

    def simulate_verse(self):
        """Begins at the start state and transitions through the Markov chain for 
        this text. Returns a single-string verse written in the style of the given 
        text."""
        #Set current to index of "$tart" and initialize the verse
        current = self.to_index["$tart"]
        verse = []
        #Transition from word to word until "$top" is reached
        while current != self.to_index["$top"]:
            next = np.random.multinomial(1, self.transition[:,current])  #list
            current = np.argmax(next)  #int
            verse.append(self.from_index[current])  #str
        verse.remove("$top")
        #Convert list of words in the verse into a single string
        verse_str = ""
        for word in verse:
            verse_str += word + " "
        return verse_str.rstrip()

    def simulate_specific_verse(self, starter):
        """Creates a verse in the style of the given text beginning with a specific 
        word found in the text."""
        #Set current to index of "$tart" if given starter word isn't in the text
        try:
            self.to_index[starter]
        except Exception:
            print(starter, "not found in given text.")
            starter = "$tart"
        # Initialize the verse
        current = self.to_index[starter]
        verse = [starter]
        if starter == "$tart":
            verse.remove("$tart")
        #Transition from word to word until "$top" is reached
        while current != self.to_index["$top"]:
            next = np.random.multinomial(1, self.transition[:,current])  #list
            current = np.argmax(next)  #int
            verse.append(self.from_index[current])  #str
        verse.remove("$top")
        #Convert list of words in the verse into a single string
        verse_str = ""
        for word in verse:
            verse_str += word + " "
        return verse_str.rstrip()
        
    def simulate_chapter(self):
        """Simulate until the end of a chapter is reached. Returns a list of strings 
        where each string is a verse."""
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





