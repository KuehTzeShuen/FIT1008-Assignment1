"""
This module contains PokeType, TypeEffectiveness and an abstract version of the Pokemon Class
"""
from abc import ABC
from enum import Enum
from math import ceil

from data_structures.referential_array import ArrayR

class PokeType(Enum):
    """
    This class contains all the different types that a Pokemon could belong to
    """
    FIRE = 0
    WATER = 1
    GRASS = 2
    BUG = 3
    DRAGON = 4
    ELECTRIC = 5
    FIGHTING = 6
    FLYING = 7
    GHOST = 8
    GROUND = 9
    ICE = 10
    NORMAL = 11
    POISON = 12
    PSYCHIC = 13
    ROCK = 14

class TypeEffectiveness:
    """
    Represents the type effectiveness of one Pokemon type against another.
    """
    # The tablesize variable is calculated as the square of the number of Pokemon types. 
    # It represents the total number of possible interactions between different Pokemon types.
    # I used the len(PokeType) to determine how many types there are, to make it easier in case we ever feel like adding fairy, dark and steel types from gen 2 some day.
    table_size = len(PokeType) ** 2
    EFFECT_TABLE = ArrayR(table_size)

    # The effectiveness table is then populated with the values from the type_effectiveness.csv file.
    # Only one array is strictly necessary, as all the values are stored sequentially to the type of the attacker against the type of the defender.
    # The values are stored in the array in the order of the PokeType enum, so the first 15 values are the effectiveness of fire against all types, the next 15 are the effectiveness of water against all types, etc.
    # The time complexity of this method is O(n), where n is the number of lines in the .csv file / the number of types of pokemon.
    # There is no best or worst case, as the number of types and their interactions are fixed.
    with open("type_effectiveness.csv", encoding='utf-8') as file:
        next(file)
        
        i = 0
        for line in file:
            values = line.strip().split(",")
            for value in values:
                EFFECT_TABLE[i] = value
                i += 1
    
    # So we retrieve the effectiveness of one type against another by multiplying the attacker's type value (Grass = 2) to the number of types to get to the 15 values of the attacker's type (2*15 = 30), and adding the defender's type value (Water = 1, 30 + 1 = 31)
    # The 31st element (0 indexed so technically 32nd element) in the .csv and the effect table are both 2.0, meaning grass pokemon are super effective against water pokemon.
    # The time complexity of this method is O(1), as it only requires a single lookup in the array, and the getitem method of the array is O(1).
    @classmethod
    def get_effectiveness(cls, attack_type: PokeType, defend_type: PokeType) -> float:
        """
        Returns the effectiveness of one Pokemon type against another, as a float.

        Parameters:
            attack_type (PokeType): The type of the attacking Pokemon.
            defend_type (PokeType): The type of the defending Pokemon.

        Returns:
            float: The effectiveness of the attack, as a float value between 0 and 4.
        """
        return float(TypeEffectiveness.EFFECT_TABLE[(attack_type.value * len(PokeType)) + defend_type.value])

        
    # The time complexity of this method is O(1), as the size of the Poketype enum is known in advance, so we just return that value.
    def __len__(self) -> int:
        """
        Returns the number of types of Pokemon
        """
        return len(PokeType)


class Pokemon(ABC):
    """
    Represents a base Pokemon class with properties and methods common to all Pokemon.
    """
    def __init__(self):
        """
        Initializes a new instance of the Pokemon class.
        """
        self.health = None
        self.level = None
        self.poketype = None
        self.battle_power = None
        self.evolution_line = None
        self.name = None
        self.experience = None
        self.defence = None
        self.speed = None
        # To keep track of which pokemon is which after reordering
        self.id = None


    def get_name(self) -> str:
        """
        Returns the name of the Pokemon.

        Returns:
            str: The name of the Pokemon.
        """
        return self.name

    def get_health(self) -> int:
        """
        Returns the current health of the Pokemon.

        Returns:
            int: The current health of the Pokemon.
        """
        return self.health

    def get_level(self) -> int:
        """
        Returns the current level of the Pokemon.

        Returns:
            int: The current level of the Pokemon.
        """
        return self.level

    def get_speed(self) -> int:
        """
        Returns the current speed of the Pokemon.

        Returns:
            int: The current speed of the Pokemon.
        """
        return self.speed

    def get_experience(self) -> int:
        """
        Returns the current experience of the Pokemon.

        Returns:
            int: The current experience of the Pokemon.
        """
        return self.experience

    def get_poketype(self) -> PokeType:
        """
        Returns the type of the Pokemon.

        Returns:
            PokeType: The type of the Pokemon.
        """
        return self.poketype

    def get_defence(self) -> int:
        """
        Returns the defence of the Pokemon.

        Returns:
            int: The defence of the Pokemon.
        """
        return self.defence

    def get_evolution(self):
        """
        Returns the evolution line of the Pokemon.

        Returns:
            list: The evolution of the Pokemon.
        """
        return self.evolution_line

    def get_battle_power(self) -> int:
        """
        Returns the battle power of the Pokemon.

        Returns:
            int: The battle power of the Pokemon.
        """
        return self.battle_power

    # We calculate the base damage through the formula given for the current battle power multiplied by the type effectiveness.
    # The time complexity of this method is O(1), as it only involves lookups of attributes of the Pokemon class and comparisons of basic data types int, assuming ceil = n(1) as well. We already established that getting the type effectiveness value is also O(1).
    def attack(self, other_pokemon) -> int:
        """
        Calculates and returns the damage that this Pokemon inflicts on the
        other Pokemon during an attack.

        Args:
            other_pokemon (Pokemon): The Pokemon that this Pokemon is attacking.

        Returns:
            int: The damage that this Pokemon inflicts on the other Pokemon during an attack.
        """
        attack = self.battle_power
        defence = other_pokemon.defence
        if defence < attack / 2:
            damage = attack - defence
        elif defence < attack:
            damage = ceil(attack * 5/8 - defence / 4)
        else:
            damage = ceil(attack / 4)
            
        effectiveness = TypeEffectiveness.get_effectiveness(self.poketype, other_pokemon.poketype)
        damage *= effectiveness

        print(f"{self.name} attacking for {damage} {effectiveness}")
        return damage

    def defend(self, damage: int) -> None:
        """
        Reduces the health of the Pokemon by the given amount of damage, after taking
        the Pokemon's defence into account.

        Args:
            damage (int): The amount of damage to be inflicted on the Pokemon.
        """
        effective_damage = damage/2 if damage < self.get_defence() else damage
        self.health = self.health - effective_damage

    # Then we continue the damage calculation by multiplying the damage by the ratio of pokedex completion of the attacker and defender to get the effective damage.
    # The defending pokemon then uses the defend meethod to reduce its health by the reduced damage.
    # The time complexity of this method is O(1), as this and the defend method only involve getting the attributes of the Pokemon class, and comparisons and arithmetic of basic data types of int, assuming ceil = n(1) as well.
    def calculate_damage(self, defender, pokedex_ratio_multiplier: float) -> None:
        battle_power = self.attack(defender)
        effective_damage = ceil(battle_power * pokedex_ratio_multiplier)
        print(pokedex_ratio_multiplier)
        defender.defend(effective_damage)

    def level_up(self) -> None:
        """
        Increases the level of the Pokemon by 1, and evolves the Pokemon if it has
          reached the level required for evolution.
        """
        self.level += 1
        if len(self.evolution_line) > 0 and self.evolution_line.index\
            (self.name) != len(self.evolution_line)-1:
            self._evolve()

    # The function first updates the name of the Pokemon to the next stage in its evolution line. It does this by indexing the list by the position of the Pokemon's name in the evolution_line list and then getting the name at the next index, which takes O(1) time.
    # It then multiplies the Pokemon's battle power, health, speed and defence by 1.5 as per the Task's requirements, all of which are basic arithmetic operations that take O(1) time.
    # The time complexity of this method is O(1).
    def _evolve(self) -> None:
        """
        Evolves the Pokemon to the next stage in its evolution line, and updates
          its attributes accordingly.
        """
        self.name = self.evolution_line[self.evolution_line.index(self.name)+1]
        self.battle_power *= 1.5
        self.health *= 1.5
        self.speed *= 1.5
        self.defence *= 1.5

    def is_alive(self) -> bool:
        """
        Checks if the Pokemon is still alive (i.e. has positive health).

        Returns:
            bool: True if the Pokemon is still alive, False otherwise.
        """
        return self.get_health() > 0

    def __str__(self):
        """
        Return a string representation of the Pokemon instance in the format:
        <name> (Level <level>) with <health> health and <experience> experience
        """
        return f"{self.name} (Level {self.level}) with {self.get_health()} health and {self.get_experience()} experience"


# TODO
if __name__ == "__main__":
    print(TypeEffectiveness.get_effectiveness(PokeType.GRASS, PokeType.FLYING))
    print(TypeEffectiveness.get_effectiveness(PokeType.WATER, PokeType.GRASS))
    print(TypeEffectiveness.get_effectiveness(PokeType.FIRE, PokeType.GRASS))
    print(TypeEffectiveness.get_effectiveness(PokeType.GRASS, PokeType.FIRE))
    # print(TypeEffectiveness.__len__(PokeType.WATER,PokeType.FIRE))
