# Unless otherwise stated, we assume that the time complexity of the function described takes O(1) time, and the initialisation of array ADTs that use the referrential array ArrayR take O(n) time, where n is number of elements in the array.
# ADT operations for stack and queue are also assumed take O(1) time, as push and pop, append and serve are all just accessing an element from the top, or back and front of tje arrayADT respectively, unless otherwise stated.

from data_structures.array_sorted_list import ArraySortedList
from pokemon import *
import random
from typing import List
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.bset import BSet
from battle_mode import BattleMode


class PokeTeam:
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()
    CRITERION_LIST = ["health", "defence", "battle_power", "speed", "level"]

    def __init__(self):
        self.team = ArrayR(self.TEAM_LIMIT)
        self.copy = ArrayR(self.TEAM_LIMIT)
        self.team_count = 0
        self.fainted_pokemon = ArrayR(self.TEAM_LIMIT)
        self.optimise_special = 1
        self.criterion = None

    # Choose manually first initialises a self.team array of size TEAM_LIMIT.
    # i is an integer used as the index for adding Pokemon to the self.team array.
    # We then ask the user to input the name of the n Pokemon they want to add to their team, where n is the number of pokemon on their team. 
    # We loop through the all_pokemon_types array = 77 and create an instance of each Pokemon class.
    # We then check if the name input variable is equal to the name of each Pokemon class. If its equal, that means the pokemon exists and we add it to self.team at index i.
    # self.team[i].id is then set to i, which is the original index of the Pokemon in the team.
    # We then increment the team_count variable by 1 and increment i by 1.
    # The user can choose to end the selection after selecting one pokemon, in which case we have to resize the self.team array and insert the n elements that the user chose.
    # The time complexity of this function is O(n) where n is the number of Pokemon the user chooses to add to their team.
    # The best case time complexity is O(1) when the user chooses to add only one Pokemon to their team. The while loop only loops 1 time and the for loop only has to copy one value.
    # The worst case time complexity is O(n) when the user chooses to add all n Pokemon to their team, and all of n are the last pokemon in the all_pokemon_types array. The while loop loops n times and the nested for loop has iterate to the last element every loop.
    def choose_manually(self):
        self.team = ArrayR(self.TEAM_LIMIT)
        print(f"Choose your team of {self.TEAM_LIMIT} Pokemon.")
        self.team_count = 0
        all_pokemon_types = get_all_pokemon_types()
        i = 0
        while i < self.TEAM_LIMIT:
            name = input(f"Enter the name of Pokemon #{i+1} (or type 'done' to stop choosing here): ")
            if name == "done":
                if i == 0:
                    print("You must choose at least one Pokemon for your team.")
                else:
                    print(i)
                    temp_team = ArrayR(i)
                    for j in range(i):
                        temp_team[j] = self.team[j]
                    self.team = temp_team
                    break
            # if all_pokemon_types.index(name) == -1:
            #     print(f"No Pokemon named {name} found.")
            #     continue
            
            for PokemonClass in all_pokemon_types:
                pokemon_instance = PokemonClass()
                if pokemon_instance.name == name:
                    self.team[i] = pokemon_instance
                    self.team[i].id = i
                    self.team_count += 1
                    i += 1
                    break
            else:
                print(f"No Pokemon named {name} found.")

    def choose_randomly(self) -> None:
        self.team = ArrayR(self.TEAM_LIMIT)
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0
        for i in range(self.TEAM_LIMIT):
            rand_int = random.randint(0, len(all_pokemon)-1)
            self.team[i] = all_pokemon[rand_int]()
            self.team_count += 1
            self.team[i].id = i
    
    # The regenerate_team function first initialises a team_length variable to the length of the original version of the array, in case some of our pokemon have fainted and are no longer in the team.
    # We then set the self.team.length to team_length, back to its original length
    # We then create a temp_team array of size team_length to store the pokemon that have fainted (health <= 0), which takes a time where a = number of pokemon that have fainted.
    # We set the health of each pokemon to the default health of the class, and add them to the temp_team array according to their original index at id.
    # We then loop through the current pokemon team array and top up the health of each pokemon to the default health of the class, and add them to the temp_team array. This takes b time, where b = number of pokemon in the team.
    # a + b = O(n) where n is the number of pokemon in the team.
    # We then set the self.fainted_pokemon array to the temp_team array, which takes O(n) time where n is again the number of pokemon in the team.
    # The time complexity of this function is O(n) where n is the number of pokemon in the team.
    # The best/worst case complexity is O(n) where n is the number of Pokemon in the team.
    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        team_length = len(self.copy)
        self.team.length = team_length
        temp_team = ArrayR(team_length)
        for pokemon in self.fainted_pokemon:
            if pokemon:
                pokemon_type = type(pokemon)
                pokemon.health = int(pokemon_type().health)
                temp_team[pokemon.id] = pokemon
        for pokemon in self.team:
            if pokemon:
                pokemon_type = type(pokemon)
                pokemon.health = int(pokemon_type().health)
                temp_team[pokemon.id] = pokemon
        self.fainted_pokemon = ArrayR(self.team.length)
        self.team = ArrayR(team_length)
        for i in range(len(temp_team)):
            self.team[i] = temp_team[i]
        self.team_count = len(self.team)
        if battle_mode == BattleMode.OPTIMISE:
            self.assign_team(criterion)
        else:
            self.assemble_team(battle_mode)

    # An ArrayR is initialised in O(n) time, where n = number of pokemon in the team, which have to be put into the ArrayR.
    # The assemble_team function first checks if the battle_mode is SET or ROTATE. If it is, we create a new team ADT of the same size as the original team array, and a copy array of the same size.
    # We then loop through the original team array and push or append n pokemon to the new team ADT, where n is the number of pokemon in self.team. Then set the id of each pokemon to the index of the pokemon in the new team ADT.
    # We then set the self.team array to the new team ADT.
    # The time complexity of this function is O(n) where n is the number of pokemon in the team.
    # The best case time complexity is O(1) when the method is invalid.
    # The worst case time complexity is O(n) when the method is valid and the user has n Pokemon to their team, which results in n iterations thought either SET or ROTATE to put all the pokemon into the correct ADT for the battle mode..
    def assemble_team(self, battle_mode: BattleMode) -> None:
        self.copy = ArrayR(self.team.__len__())
        if battle_mode == BattleMode.SET:
            team = ArrayStack(self.team.__len__())
            for i in range(len(self.team)):
                pokemon = self.team[i]
                pokemon.id = i
                team.push(pokemon) #
                self.copy[i] = pokemon
        elif battle_mode == BattleMode.ROTATE:
            team = CircularQueue(self.team.__len__())
            for i in range(len(self.team)):
                pokemon = self.team[i]
                pokemon.id = i
                team.append(pokemon) #
                self.copy[i] = pokemon
            self.team = CircularQueue(self.team.__len__())
        else:
            raise ValueError(f"Invalid battle mode")
        self.team = team
        self.team.team_count = self.team.__len__()
        
    # The method updates the poketeam's optimise mode criterion to sort by if it receives a new one.
    # The assign_team function initialises a team array of size team_count and a copy array of the same size.
    # We then loop through the team array and set the key of each pokemon to the criterion value multiplied by the optimise_special variable, and add each pokemon to the team array.
    # We then set the self.team array to the team array.
    # The add function of array sorted list has a time complexity of O(log n) where n is the number of pokemon in the team. This is because it uses binary search to search for the index where the current value should be stored at.
    # The time complexity of this function is O(n log n) where n is the number of pokemon in the team, because the add function which is O(log n) is called n times.
    # The best case time complexity is O(1) when there is only one pokemon to add to the array sorted list. We only need O(1) to open one array space and the for loop only loops once, and the pokemon is added to the array sorted list with O(1) time complexity if the array is empty, or its criterion value perfectly belongs in the middle of the current sorted list.
    # The worst case is where the pokemon team == TEAM_LIMIT, initialising the ArrayRs and iterating through the pokemon to add to the new array sorted list is O(n log n), where n is the number of pokemon.
    def assign_team(self, criterion: str = None) -> None:
        if criterion:
            self.criterion = criterion
        team = ArraySortedList(self.team_count)
        self.copy = ArrayR(self.team_count)
        for i in range(self.team_count):
            pokemon = self.team[i]
            pokemon.id = i
            if pokemon:
                pokemon.key = getattr(pokemon, self.criterion) * self.optimise_special
                team.add(pokemon)
                self.copy[i] = pokemon
        self.team = team
        
    # The special function first checks if the battle_mode is SET. If it is, we create a temp_array of size mid_index, where mid_index is the length of the team array divided by 2.
    # We then loop through the team array and pop n/2 pokemon from the team array and add them to the temp_array. 
    # We then loop through the temp_array and set the id of each pokemon to the team_count variable, and push each pokemon to the team array from first popped to last popped. This effectively reverses the order of the pokemon in the first half of the team array.
    # If it is a ROTATE battle_mode, we loop through half of the team array and append each pokemon to the team array. This effectively rotates the team array by 1.
    # If it is OPTIMISE mode, we simply just multiply all the values of the criterion variable by -1. This makes the biggest value go to the back and the smallest value go to the front.
    # The time complexity of this function is O(n) where n is the number of pokemon in the team.
    # The best case time complexity is O(1) when there is only one pokemon needed to be reversed, so the program would just take the pokemon and put it back in its place. Or if the 
    # The worst case time complexity is O(n) when the user has n Pokemon to their team, which results in n iterations to reverse the order of the first half of the team array.
    def special(self, battle_mode: BattleMode) -> None:
        if battle_mode == BattleMode.SET:
            mid_index = len(self.team) // 2
            temp_array = ArrayR(mid_index)
            for i in range(mid_index):
                temp_array[i] = self.team.pop()
                self.team_count -= 1
            for i in range(mid_index):
                temp_array[i].id = self.team_count
                self.team.push(temp_array[i])
                self.copy[self.team_count] = temp_array[i]
                self.team_count += 1
        elif battle_mode == BattleMode.ROTATE:
            temp_array = ArrayR(len(self.team) - mid_index)
            length = len(self.team)
            mid_index = length // 2
            for i in range(mid_index):
                self.team.append(self.team.pop())
            for i in range(length = mid_index):
                temp_array[i].id = self.team_count
                self.team.push(temp_array[i])
                self.copy[self.team_count] = temp_array[i]
                self.team_count += 1
        elif battle_mode == BattleMode.OPTIMISE:
            self.optimise_special *= -1
            self.assign_team()
        else:
            raise ValueError(f"Invalid battle mode")  

    # The __getitem__ function has a time complexity of O(1) as it returns the pokemon at the index of the team attribute of the PokeTeam class.
    def __getitem__(self, index: int):
        if isinstance(self.team, ArrayStack):
            return self.copy[index]
        elif isinstance(self.team, CircularQueue):
            real_index = (self.team.front + index) % len(self.copy)
            return self.copy[real_index]
        else:
            return self.team[index]

    # The __len__ function has a time complexity of O(1) as it returns the length of the team attribute of the PokeTeam class.
    def __len__(self):
        return len(self.team)

    
    def __str__(self):
        result = ""
        for i in self.copy:
            if i:
                result += f"{i}\n"
        return result

class Trainer:

    def __init__(self, name) -> None:
        self.name = name
        self.team = PokeTeam()
        # We use a BSet of length = number of Poketypes = 15 to store the pokemon types seen by the trainer, because for every type, we only need two values, 0 or 1, to represent if the type has been seen or not.
        # BSet is much cheaper than array set for this purpose, as it uses bitwise operations to store the values without having to iterate through the set, so adding a new type to the set is O(1) time.
        self.pokedex = BSet(len(PokeType))

    # choose_randomly has a time complexity of O(n), where n is the number of pokemon added in the team (assuming random.randint = O(1)). The get_all_pokemon_types function has a time complexity of O(1) as it returns a fixed list of all 77 of the pokemon types.
    # choose_manually has a time complexity of O(n) where n is the number of pokemon the user chooses to add to their team. The get_all_pokemon_types function has a time complexity of O(1) as it returns a fixed list of all 77 of the pokemon types.
    # If neither option is chosen, per the task requirements an error is printed.
    # The time complexity of the pick_team function is O(n), as either random or manual are both O(n) operations, and registering n pokemon to the pokedex is O(n), where n is the number of pokemon registered. amd register_pokemon has a time complexity of O(1).
    # The best case time complexity of the pick_team function is O(1) when the method is invalid. 
    # The worst case time complexity is O(n) when the method is valid and the user chooses to add all n Pokemon to their team, and all of n are the last pokemon in the all_pokemon_types array.
    def pick_team(self, method: str) -> None:
        if method.upper() == "RANDOM":
            self.team.choose_randomly()
        elif method.upper() == "MANUAL":
            self.team.choose_manually()
        else:
            print("Invalid method")
        for pokemon in self.team:
            if pokemon:
                self.register_pokemon(pokemon)
        
    # The get_team function has a time complexity of O(1) as it returns the team attribute of the Trainer class.
    def get_team(self) -> PokeTeam:
            return self.team

    # The get_name function has a time complexity of O(1) as it returns the name attribute of the Trainer class.
    def get_name(self) -> str:
        return self.name

    # The register_pokemon function has a time complexity of O(1) as it adds a pokemon to the pokedex attribute of the Trainer class.
    def register_pokemon(self, pokemon: Pokemon) -> None:
        """ Added the pokemon types seen to the pokedex. We add a +1 to the value because the __contains__ method in BSet only stores positive integers more than 0, and the enumerated PokeTypes start with FIRE = 0"""
        self.pokedex.add(pokemon.poketype.value + 1)

    # The get_pokedex_completion function has a time complexity of O(n), where n is the number of poketype, as it iterates through the bitwise set to find the total amount of poketypes seen to return the pokedex completion percentage.
    # However, in this instance the number of poketypes is fixed at 15, so the time complexity is O(1) as the BSet iterates through 15 bits every time to find the total amount of poketypes seen.
    def get_pokedex_completion(self) -> float:
        ans = round(len(self.pokedex) / len(PokeType.__members__), 2)
        return ans

    # The __str__ function has a time complexity of O(1) as it returns a string representation of the Trainer class.
    def __str__(self) -> str:
        return f"Trainer {self.name} Pokedex Completion: {int(self.get_pokedex_completion()*100)}%"


if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("manual")
    print(t)
    print(t.get_team())
    # print(t.get_team().assemble_team(BattleMode.SET))
    print("test")
    t.get_team().assemble_team(BattleMode.ROTATE)
    print(t.get_team()[0])
    print(t.get_team()[1])
    print(t.get_team()[2])
    print(t.get_team()[3])
    print(t.get_team()[4])