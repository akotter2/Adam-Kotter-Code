#tokens.py
"""A file for storing the various effect tokens used in the battle_arena.py program."""

class Token:
    """A counter for keeping track of character effects.
    
    Attributes:
        Name (str): the effect's name.
        Timer (int): how long the effect will last before undoing itself, usually decremented by 1 per turn by the Arena hosting the battle.
        Used (bool): whether or not the effect can be applied again.
        Host (Character): the character receiving the effect.
    
    Functions:
        Apply: Changes an attribute of the host.
        Undo: Undoes the effect when the timer runs out."""
    
    def __init__(self, host, timer=1):
        self.name = "Generic Effect"
        self.host = host
        self.timer = timer
        self.used = False

    def apply(self):
        """To be implemented in subclasses of Token"""

    def undo(self):
        """To be implemented in subclasses of Token"""




class BlockToken(Token):
    """A subclass of the Token class. Reduces damage done to the host by a certain percent (default 50%).
    Default time: 1 turn"""
    
    def __init__(self, host, timer=0, percentage=50):
        Token.__init__(self, host, timer)
        self.name = "Block"
        self.percentage = percentage

    def apply(self):
        """Accesses the host's target and removes the given percentage of strength"""
        if self.used:
            pass
        else:
            if self.host.target is None:
                raise AttributeError("Nothing to block!")
            else:
                self.host.target.strength *= (self.percentage/100)
                print(self.host.name + " is blocking!")
                self.used = True

    def undo(self):
        """Accesses the host's target and returns the previously removed percentage of strength"""
        if self.host.target is None:
            pass
        else:
            self.host.target.strength /= (self.percentage/100)
            print(self.host.name + " finished blocking.")




class FireToken(Token):
    """A subclass of the Token class. Deals damage to the host each turn.
    Default time: 2 turn
    Default damage: 10"""
    
    def __init__(self, host, timer=0, damage=10):
        Token.__init__(self, host, timer)
        self.name = "Fire"
        self.percentage = percentage

    def apply(self):
        """Accesses the host's target and removes the given percentage of strength"""
        if self.used:
            pass
        else:
            if self.host.target is None:
                raise AttributeError("Nothing to block!")
            else:
                self.host.target.strength *= (self.percentage/100)
                print(self.host.name + " is blocking!")
                self.used = True

    def undo(self):
        """Accesses the host's target and returns the previously removed percentage of strength"""
        if self.host.target is None:
            pass
        else:
            self.host.target.strength /= (self.percentage/100)
            print(self.host.name + " finished blocking.")