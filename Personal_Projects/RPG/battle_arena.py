#battle_arena.py
"""This is a file that lets you put on a battle arena fight. You can create a character and then have it fight other characters.
Requires the tokens.py module for full functionality."""

import tokens
import things
import numpy as np


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
        Backpack (list: Thing): used to track what things a character is holding, to be implemented later.
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
        """Returns a stamina maximum, stamina recharge rate, strength, health, magic attack, magic defense, and dexterity based on the given class."""
        if _class == "Dwarf":
            return 6, 3, 8, 100, 3, 3, 5
        elif _class == "Orc":
            return 7, 1, 10, 100, 1, 0, 3
        elif _class == "Mage":
            return 3, 1, 3, 90, 10, 8, 3
        elif _class == "Warrior":
            return 7, 2, 9, 100, 1, 1, 5
        elif _class == "Assassin":
            return 10, 4, 8, 75, 3, 3, 10
        elif _class == "Healer":
            return 3, 1, 3, 90, 8, 10, 4
        else:
            return 3, 1, 3, 75, 0, 0, 2


    def __init__(self, name, _class, exp=0, level=0):
        self.name = name
        self._class = _class
        self.stamina_max, self.recharge, self.strength, self.health, self.magic_atk, self.magic_dfn, self.dex = self.get_class(_class)
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
        elif action == "block":
            self.block()
        elif action == "charge":
            self.charge()
        elif action == "equip":
            self.equip()
        elif action == "fire":
            self.fire_attack()
        elif action == "get item":
            self.get_item()
        elif action == "heal":
            self.heal()
        elif action == "heal spell":
            self.heal_spell()
        elif action == "save":
            self.save()
        elif action == "scan":
            self.scan()
        elif action == "use item":
            self.use_item()
        elif action == "admin fire":
            self.fire_attack_admin()
        elif action == "admin heal spell":
            self.heal_spell_admin()
        elif action == "help":
            print("Possible actions: \n'attack'\n'block'\n'charge'\n'equip'\n'fire'\n'get item'\n'heal'\n'heal spell'\n'save'\n'scan'\n'use item'\n'help'")
        else:
            print("That's not a valid action.")
            self.action()


    def attack(self, enemy):
        """Lowers the health of your enemy at the cost of stamina."""
        #Don't attack if you're low on stamina
        if self.stamina < 1:
            print("You are out of stamina! Charge now!")
            self.action()
        else:
            #Give the target a chance to dodge based on their dexterity
            if np.random.binomial(1, (enemy.dex*7.5)/100) == 1:
                print(enemy.name + " dodged the attack!")
            else:
                #Check for critical strike
                crit = 1
                if np.random.binomial(1, (self.dex*7.5)/100) == 1:
                    crit = 5
                #Check for blocking
                if any([e.name == "Block" for e in enemy.effects]):
                    for e in enemy.effects:
                        if e.name == "Block":
                            enemy.health -= self.strength*(e.percentage/100)*crit
                            print(enemy.name + " received " + str(self.strength*(e.percentage/100))*crit + " points of damage!")
                else:
                    enemy.health -= self.strength
                    print(enemy.name + " received " + str(self.strength)*crit + " points of damage!")
            print(enemy.name + " health: " + str(enemy.health))
            self.stamina -= 1
            print(self.name + " has " + str(self.stamina) + " stamina.")
    

    def block(self):
        """Reduces damage from target by 50% for one turn."""
        block_token = tokens.BlockToken(self)
        block_token.apply()
        self.effects.append(block_token)


    def charge(self):
        """Increases stamina by the recharge rate until the stamina maximum is reached."""
        if self.stamina >= self.stamina_max:
            print("Already fully charged! Try something else.")
            self.action()
        else:
            self.stamina += self.recharge
            print(self.name + "'s stamina: " + str(self.stamina))


    def equip(self):
        """Chooses an item based on user input and equips it, altering the character's stats."""
        print("Items in the backpack: ")
        print(self.backpack)
        item = input("Which item would you like to equip? ")


    def fire_attack(self):
        """Places a fire token on the target"""
        fire_token = tokens.FireToken(self.target)
        self.target.effects.append(fire_token)
        print(self.target.name + " is on fire!")


    def get_item(self):
        """Chooses an item based on user input and adds it to the backpack, enabling it to be used later."""
        item = input("Which item would you like to get? ")


    def heal(self):
        """Increases your health by one."""
        self.health += 1
        print(self.name + "'s health: " + str(self.health))


    def heal_spell(self):
        """Places a heal token on the player"""
        heal_token = tokens.HealToken(self)
        self.effects.append(heal_token)
        print(self.name + " is being healed!")


    def scan(self):
        """Checks your current stats."""
        print("Health: " + str(self.health))
        print("Stamina: " + str(self.stamina))
        print("Strength: " + str(self.strength))
        print("Stamina recharge rate: " + str(self.recharge))
        for e in self.effects:
            print(e.name + ": " + str(e.timer) + " turns left.")
        self.action()


    def use_item(self):
        """Chooses an item from the backpack based on user input and activates its effect."""
        item = input("Which item would you like to use? ")


    def fire_attack_admin(self):
        """Places a fire token of variable strength and duration on the target"""
        time = int(input("How long will the fire last? "))
        dmg = int(input("How powerful is the fire? "))
        fire_token = tokens.FireToken(self.target,timer=time,damage=dmg)
        self.target.effects.append(fire_token)
        print(self.target.name + " is on fire!")


    def heal_spell_admin(self):
        """Places a heal token of variable strength and duration on the player"""
        time = int(input("How long will the healing last? "))
        hlth = int(input("How powerful is the healing? "))
        heal_token = tokens.HealToken(self, timer=time, heal=hlth)
        self.effects.append(heal_token)
        print(self.name + " is being healed!")
    

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
        if defeated is None:
            if self.player2.health <= 0:
                defeated = self.player2
            elif self.player1.health <= 0:
                defeated = self.player1
            if self.player2.health <= 0 and self.player1.health <= 0:
                print("Both " + self.player1.name + " and " + self.player2.name + " have been defeated.")
                return
        print(defeated.name + " has been defeated!")
        



if __name__ == "__main__":
    Gimli = Character("Gimli", "Dwarf")
    Ghook = Character("Ghook", "Orc")
    arena = Arena(Gimli, Ghook)
    #arena.player1 = arena.load_save()
    #arena. player2 = arena.load_save()
    arena.fight()