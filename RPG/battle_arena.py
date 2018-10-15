#battle_arena.py
"""This is a file that lets you put on a battle arena fight. You can create a character and then have it fight other characters.
Requires the tokens.py module for full functionality."""

import tokens

class Equipment():
    """To be implemented later."""




class Character:
    """An entity that takes part in battles in an arena.
    
    Attributes:  
        Name (str): the character's name.
        Class (str): the character's type. This determines the character's stamina max, recharge, strength, and health.
        Stamina max (int): the character's maximum stamina, defined initially by their class.
        Stamina (int): how many attacks a character can make without needing to recharge. Usually decrements by 1 with each attack.
        Recharge (int): how much stamina is regained by each charge, defined initially by their class.
        Strength (int): how much damage the character deals with each attack, defined initially by their class.
        Health (int): how much damage the character can receive before dying, defined initially by their class.
        Experience (int): used to increase the character's statistics, to be implemented later.
        Level (int): used to track the number of increases to the character's statistics, to be implemented later.
        Backpack (list: Equipment): used to track what equipment a character is holding, to be implemented later.
        Effects (list: Token): used to track the effects a character is being affected by.
        Target (Character): the character's enemy, the target of the character's offensive actions.

    Functions:
        Get class (str; int, int, int, int): returns a stamina maximum, stamina recharge rate, strength, and health based on the given class.
        Action: asks for user input about which action to do, then performs that action.
        Attack: lowers the health of the target in proportion to the character's strength.
        Charge: increases the character's stamina by the recharge rate until the stamina maximum is reached.
        Heal: increases the character's health.
        Scan: prints the character's current statistics then gives an opportunity for a different action.
        Block: applies a block token to the character.
        Level up: increases the character's level, to be implemented later.
        Save: writes the character's stats to a file to be retrieved later, to be implemented later."""


    def get_class(self,_class):
        """Returns a stamina maximum, stamina recharge rate, strength, and health based on the given class."""
        if _class == "Dwarf":
            return 6, 3, 8, 100
        if _class == "Orc":
            return 7, 1, 10, 100


    def __init__(self, name, _class, exp=0, level=0):
        self.name = name
        self._class = _class
        self.stamina_max, self.recharge, self.strength, self.health = self.get_class(_class)
        self.stamina = self.stamina_max
        self.exp = exp
        self.level = level
        self.backpack = []
        self.effects = []
        self.target = None


    def action(self):
        """Asks for user input about which action to use"""
        action = input("What would " + self.name + " like to do? ")
        if action == "attack":
            self.attack(self.target)
        elif action == "charge":
            self.charge()
        elif action == "heal":
            self.heal()
        elif action == "scan":
            self.scan()
        elif action == "block":
            self.block()
        elif action == "fire":
            self.fire_attack()
        elif action == "save":
            self.save()
        else:
            print("That's not a valid action.")
            self.action()


    def attack(self, enemy):
        """Lowers the health of your enemy."""
        if self.stamina < 1:
            print("You are out of stamina! Charge now!")
            self.action()
        else:
            enemy.health -= self.strength
            print(enemy.name + " received " + str(self.strength) + " points of damage!")
            print(enemy.name + " health: " + str(enemy.health))
            self.stamina -= 1
            print(self.name + " has " + str(self.stamina) + " stamina.")


    def charge(self):
        """Increases stamina by the recharge rate until the stamina maximum is reached."""
        if self.stamina >= self.stamina_max:
            print("Already fully charged! Try something else.")
            self.action()
        else:
            self.stamina += self.recharge
            print(self.name + "'s stamina: " + str(self.stamina))


    def heal(self):
        """Increases your health by one."""
        self.health += 1
        print(self.name + "'s health: " + str(self.health))


    def scan(self):
        """Checks your current stats."""
        print("Health: " + str(self.health))
        print("Stamina: " + str(self.stamina))
        print("Strength: " + str(self.strength))
        print("Stamina recharge rate: " + str(self.recharge))
        for e in self.effects:
            print(e.name + ": " + str(e.timer) + " turns left.")
        self.action()
    

    def block(self):
        """Reduces damage from target by 50% for one turn."""
        block_token = tokens.BlockToken(self)
        block_token.apply()
        self.effects.append(block_token)


    def fire_attack(self):
        """Places a fire token on the target"""
        fire_token = tokens.FireToken(self.target)
        self.target.effects.append(fire_token)
        print(self.target.name + " is on fire!")
    

    def level_up(self):
        """Not implemented yet"""


    def save(self):
        """Writes the character's stats to an appropriately named outfile."""

        def _write(attempts):
            """A helper function to recursively attempt to write to an appropriately named and numbered outfile."""
            try:
                with open(self.name + "_" + self._class + "_" + str(attempts) + ".txt", "x") as outfile:
                    outfile.write(self.name + "\n")
                    outfile.write(self._class + "\n")
                    outfile.write(str(self.stamina_max) + "\n")
                    outfile.write(str(self.recharge) + "\n")
                    outfile.write(str(self.strength) + "\n")
                    outfile.write(str(self.health) + "\n")
                    outfile.write(str(self.stamina) + "\n")
                    outfile.write(str(self.exp) + "\n")
                    outfile.write(str(self.level) + "\n")
                    for b in self.backpack:
                        outfile.write(str(b) + "\n")
                    for e in self.effects:
                        outfile.write(str(e) + "\n")
            except FileExistsError:
                choice = input("Character of that class by that name already exists. [O]verwrite or create [N]ew file? ")
                if choice == "O":
                    with open(self.name + "_" + self._class + "_" + str(attempts) + ".txt", "w") as outfile:
                        outfile.write(self.name + "\n")
                        outfile.write(self._class + "\n")
                        outfile.write(str(self.stamina_max) + "\n")
                        outfile.write(str(self.recharge) + "\n")
                        outfile.write(str(self.strength) + "\n")
                        outfile.write(str(self.health) + "\n")
                        outfile.write(str(self.stamina) + "\n")
                        outfile.write(str(self.exp) + "\n")
                        outfile.write(str(self.level) + "\n")
                        for b in self.backpack:
                            outfile.write(str(b) + "\n")
                        for e in self.effects:
                            outfile.write(str(e) + "\n")
                if choice == "N":
                    _write(attempts+1)
        
        #Attempt to write to a file with a simple name.
        try:
            with open(self.name + "_" + self._class + ".txt", "x") as outfile:
                outfile.write(self.name + "\n")
                outfile.write(self._class + "\n")
                outfile.write(str(self.stamina_max) + "\n")
                outfile.write(str(self.recharge) + "\n")
                outfile.write(str(self.strength) + "\n")
                outfile.write(str(self.health) + "\n")
                outfile.write(str(self.stamina) + "\n")
                outfile.write(str(self.exp) + "\n")
                outfile.write(str(self.level) + "\n")
                for b in self.backpack:
                    outfile.write(str(b) + "\n")
                for e in self.effects:
                    outfile.write(str(e) + "\n")
        #If simple name already exists, recursively choose to overwrite or add a unique number to the end
        except FileExistsError:
                choice = input("Character of that class by that name already exists. [O]verwrite or create [N]ew file? ")
                if choice == "O":
                    with open(self.name + "_" + self._class + ".txt", "w") as outfile:
                        outfile.write(self.name + "\n")
                        outfile.write(self._class + "\n")
                        outfile.write(str(self.stamina_max) + "\n")
                        outfile.write(str(self.recharge) + "\n")
                        outfile.write(str(self.strength) + "\n")
                        outfile.write(str(self.health) + "\n")
                        outfile.write(str(self.stamina) + "\n")
                        outfile.write(str(self.exp) + "\n")
                        outfile.write(str(self.level) + "\n")
                        for b in self.backpack:
                            outfile.write(str(b) + "\n")
                        for e in self.effects:
                            outfile.write(str(e) + "\n")
                if choice == "N":
                    _write(1)




class Arena:
    """A class for managing the battles themselves.
    
    Attributes:
        Player 1 (Character): The first character in the fight.
        Player 2 (Character): The second character in the fight.
        Other players to be implemented later.
        Environmental effects to be implemented later.

    Functions:
        Load save (str; Character): loads a saved character file to generate the statistics they had in a previous battle, to be implemented later.
        Fight: Begins and runs a battle between the players.
        Check effects (Character): iterates through a player's effects and applies or undoes them appropriately."""

    def __init__(self, player1=None, player2=None):
        self.player1 = player1
        self.player2 = player2

    def load_save(self):
        """Loads a saved character file specified by user input. Saved files have names of the format "name_class.txt" or "name_class_#", with larger numbers being more 
        recent saves."""
        name = input("Specify the name of a character to load: ")
        _class = input("Specify the class of that character: ")
        num = input("Are there multiple saved files of this character? If so, specify the save number: ")
        if num.isdigit():
            if int(num) != 0:
                with open(name + "_" + _class + "_" + num + ".txt", "r") as file:
                    stats_raw = file.read()
                stats = stats_raw.split("\n")
            else:
                with open(name + "_" + _class + ".txt", "r") as file:
                    stats_raw = file.read()
                stats = stats_raw.split("\n")
        else:
            with open(name + "_" + _class + ".txt", "r") as file:
                stats_raw = file.read()
            stats = stats_raw.split("\n")
        for i in range(2,9):
            stats[i] = int(stats[i])
        new_character = Character(stats[0], stats[1], exp=stats[7], level=stats[8])
        new_character.stamina_max = stats[2]
        new_character.recharge = stats[3]
        new_character.strength = stats[4]
        new_character.health = stats[5]
        new_character.stamina = stats[6]
        #Backpack load to be implemented later
        #Token load to be implemented later
        return new_character

    def load_class(self, _class):
        """Creates a generic character of a given class, to be implemented later"""


    def check_effects(self, player):
        """Iterates through a player's effects and applies or undoes them appropriately."""
        for e in player.effects:
            if e.timer > 0:
                e.apply()
                e.timer -= 1
            else:
                e.undo()
                player.effects.remove(e)


    def fight(self):
        """Begins and runs a battle between the players."""
        #Initialize variable for defeated player
        defeated = None
        self.player1.target = self.player2
        self.player2.target = self.player1
        if self.player1 is None:
            raise AttributeError("Player 1 missing!")
        if self.player2 is None:
            raise AttributeError("Player 2 missing!")
        while self.player1.health > 0 and self.player2.health > 0:
            self.check_effects(self.player1)
            self.player1.action()
            print()
            if self.player2.health < 1:
                defeated = self.player2
                break
            self.check_effects(self.player2)
            self.player2.action()
            print()
            if self.player1.health < 1:
                defeated = self.player1
                break
        print(defeated.name + " has been defeated!")
        



if __name__ == "__main__":
    #Gimli = Character("Gimli", "Dwarf")
    #Ghook = Character("Ghook", "Orc")
    arena = Arena()
    arena.player1 = arena.load_save()
    arena. player2 = arena.load_save()
    arena.fight()