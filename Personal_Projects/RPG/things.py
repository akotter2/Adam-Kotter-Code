#things.py
"""A file for storing the various things that characters can place in their backpack and use in the battle_arena.py program."""


class Thing():
    """A general class for objects that can be interacted with by Characters and stored in a Character's backpack. Equipment is an extension of this class.
    
    Attributes:
        Name (str): the thing's name.
        Host (Character): the character holding the thing.
        Integrity (int): how much of a beating the thing can take before breaking.
    
    Functions:
        Implemented by subclasses."""
    

    def __init__(self, name="Thing", host=None, integrity=1):
        """The Thing Constructor."""
        self.name = name
        self.host = host
        self.integrity = integrity




class Equipment(Thing):
    """An extension of the Thing class. Equipment represents objects that modify player statistics while equipped.
    
    Functions:
        Equip: changes the stats of the host character when they use or wield the equipment.
        Unequip: undoes the changes done to the host character by equipping the equipment."""


    def __init__(self, name="Equipment", host=None, integrity=1):
        Thing.__init__(self,name,host,integrity)


    def equip(self):
        """Changes the stats of the host character using the equipment when they equip the equipment. The default is +1 experience points."""
        self.host.exp += 1


    def unequip(self):
        """Undoes the stat changes done by equip when the host character stops using the equipment. The default is to do nothing."""
        pass





class Weapon(Equipment):
    """An item that increases the user's attack strength."""


