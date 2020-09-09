# bom_utility.py
"""A file for recording miscellaneous code used for the Book of Mormon linguistics 
project."""


# Import needed modules
import re
import requests


def get_prepositions():
    """Get a list of English prepositions from 
    https://www.englishclub.com/vocabulary/prepositions.htm with the requests 
    module."""
    # The list of letters with given preposition lists
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'i', 'l', 'm', 'n', 'o', 'p', 'r', 
               's', 't', 'u', 'v', 'w']
    
    # A regex for getting the prepositions
    prep_getter = re.compile(r"<p><strong>([\w ]*)<\/strong><\/p>")
    
    # For each letter, request the corresponding page and record its prepositions
    prepositions = []
    for char in letters:
        url = "https://www.englishclub.com/vocabulary/prepositions/{}.htm".format(char)
        page_source = requests.get(url).text
        char_preps = re.findall(prep_getter, page_source)
        for prep in char_preps:
            prepositions.append(prep)
    
    # Return the preposition list
    return prepositions