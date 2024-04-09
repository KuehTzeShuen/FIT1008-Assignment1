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
        self.team_count = 0
        self.fainted_pokemon = ArrayR(self.TEAM_LIMIT)

    def choose_manually(self):
        self.team = ArrayR(self.TEAM_LIMIT)
        print(f"Choose your team of {self.TEAM_LIMIT} Pokemon.")
        self.team_count = 0
        i = 0
        while i < self.TEAM_LIMIT:
            name = input(f"Enter the name of Pokemon #{i+1}: ")
            if name in [pokemon.__name__ for pokemon in self.POKE_LIST]:
                PokemonClass = next(pokemon for pokemon in self.POKE_LIST if pokemon.__name__ == name)
                self.team[i] = PokemonClass()
                self.team[i].id = i
                self.team_count += 1
                i += 1
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
        
        # self.team = ArrayR(PokeTeam.TEAM_LIMIT)
        # for i in range(PokeTeam.TEAM_LIMIT):
        #     self.team[i] = random.choice(self.POKE_LIST)()
        #     self.team[i].id = i

        # shuffled_pokemon = self.POKE_LIST[:]
        # for i in range(len(shuffled_pokemon) - 1, 0, -1):
        #     j = int(i * random.random())
        #     shuffled_pokemon[i], shuffled_pokemon[j] = shuffled_pokemon[j], shuffled_pokemon[i]
        # for i in range(self.TEAM_LIMIT):
        #     self.team[i] = shuffled_pokemon[i]()
        #     self.team[i].id = i
    
    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        team_length = len(self.copy)
        self.team.length= team_length
        temp_team = ArrayR(team_length)
        print("heal!!!")
        print(self.fainted_pokemon)
        print(self.team)
        print("heal!!")

        # for pokemon in self.fainted_pokemon:
        #     pokemon_type = type(pokemon)
        #     current_stage_index = pokemon.get_evolution().index(pokemon.name) - 1
        #     health_multiplier = 1.5 ** current_stage_index
        #     pokemon.health = int(pokemon_type().health * health_multiplier)
        #     temp_team[pokemon.id] = pokemon

        for pokemon in self.fainted_pokemon:
            if pokemon:
                pokemon_type = type(pokemon)
                current_stage_index = pokemon.get_evolution().index(pokemon.name)
                print(f"current stage index: {current_stage_index}")
                health_multiplier = 1.5 ** current_stage_index
                pokemon.health = int(pokemon_type().health * health_multiplier)
                print(pokemon.name, pokemon_type().health, health_multiplier, pokemon.health)
                print(f"idididid{pokemon.id}")
                temp_team[pokemon.id] = pokemon
        for pokemon in self.team:
            if pokemon:
                print(f"pokemon: {pokemon}")
                pokemon_type = type(pokemon)
                current_stage_index = pokemon.get_evolution().index(pokemon.name)
                health_multiplier = 1.5 ** current_stage_index
                pokemon.health = int(pokemon_type().health * health_multiplier)
                temp_team[pokemon.id] = pokemon
        self.fainted_pokemon = ArrayR(self.team.length)
        self.team = ArrayR(team_length)
        print(temp_team)
        for i in range(len(temp_team)):
            self.team[i] = temp_team[i]
        print(self.team)
        print("done healing")
        self.team_count = len(self.team)
        if battle_mode == BattleMode.OPTIMISE:
            self.assign_team(criterion)
        else:
            self.assemble_team(battle_mode)

    def assemble_team(self, battle_mode: BattleMode) -> None:
        #self.regenerate_team()
        #team = self.team.copy()
        print("assembling team")
        # for i in range(len(team)):
        #     print(team[i])

        if battle_mode == BattleMode.SET:
            team = ArrayStack(self.team.__len__())
            self.copy = ArrayR(self.team.__len__())
            for i in range(len(self.team)):
                pokemon = self.team[i]
                pokemon.id = i
                print(f"pushing {pokemon}")
                team.push(pokemon)
                self.copy[i] = pokemon

            print("assemble set success")
            self.team = team
            self.team.team_count = self.team.__len__()

        elif battle_mode == BattleMode.ROTATE:
            team = CircularQueue(self.team.__len__())
            self.copy = ArrayR(self.team.__len__())
            for i in range(len(self.team)):
                pokemon = self.team[i]
                pokemon.id = i
                print(f"pushing {pokemon}")
                team.append(pokemon)
                self.copy[i] = pokemon
            self.team = CircularQueue(self.team.__len__())
            self.team = team
            self.team.team_count = self.team.__len__()

        else:
            raise ValueError(f"Invalid battle mode")
        
    def assign_team(self, criterion: str) -> None:
        print(f"{self.team_count} in team")
        team = ArraySortedList(self.team_count)
        self.copy = ArrayR(self.team_count)
        print("assigning team")
        print(self.team)
        for i in range(self.team_count):
            pokemon = self.team[i]
            pokemon.id = i
            if pokemon:
                print("assigning next")
                pokemon.key = getattr(pokemon, criterion)
                team.add(pokemon)
                self.copy[i] = pokemon
        print("assign team success")
        self.team = team
        
    def special(self, battle_mode: BattleMode) -> None:
        if battle_mode == BattleMode.SET:
            mid_index = len(self.team) // 2
            temp_array = ArrayR(mid_index)
            for i in range(mid_index):
                temp_array[i] = self.team.pop()
                self.team_count -= 1
            for i in range(mid_index - 1, -1, -1):
                temp_array[i].id = self.team_count
                self.team.push(temp_array[i])
                self.copy[self.team_count] = temp_array[i]
                self.team_count += 1

        elif battle_mode == BattleMode.ROTATE:
            mid_index = len(self.team) // 2
            for i in range(mid_index):
                self.team.append(self.team.pop())

        elif battle_mode == BattleMode.OPTIMISE:
            print("special optimise")
        else:
            raise ValueError(f"Invalid battle mode")

    def __getitem__(self, index: int):
        print(self.team)
        print(f"index: {index}")
        if isinstance(self.team, ArrayStack):
            print(f"set mon: {self.copy[index]}")
            return self.copy[index]
        elif isinstance(self.team, CircularQueue):
            real_index = (self.team.front + index) % len(self.copy)
            print(f"real index: {real_index}")
            return self.copy[real_index]
        else:
            return self.team[index]

    def __len__(self):
        return len(self.team)

    def __str__(self):
        result = ""
        if isinstance(self.team, CircularQueue):
            for i in range(len(self.team)):
                real_index = (self.team.front + i) % len(self.team)
                result += str(self.copy[real_index]) + "\n"
        else:
            for i in range(len(self.team)):
                result += str(self.team[i]) + "\n"
        return result

class Trainer:

    def __init__(self, name) -> None:
        self.name = name
        self.team = PokeTeam()
        self.pokedex = BSet(len(PokeType))

    def pick_team(self, method: str) -> None:
        if method.upper() == "RANDOM":
            self.team.choose_randomly()
        elif method.upper() == "MANUAL":
            self.team.choose_manually()
        for pokemon in self.team:
            self.register_pokemon(pokemon)
        else:
            print("Invalid method")
        

    def get_team(self) -> PokeTeam:
        return self.team

    def get_name(self) -> str:
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        """ Added the pokemon types seen to the pokedex. We add a +1 to the value because the __contains__ method in BSet only stores positive integers more than 0, and the enumerated PokeTypes start with FIRE = 0"""
        self.pokedex.add(pokemon.poketype.value + 1)

    def get_pokedex_completion(self) -> float:
        ans = round(len(self.pokedex) / len(PokeType.__members__), 2)
        return ans

    def __str__(self) -> str:
        return f"Trainer {self.name} Pokedex Completion: {int(self.get_pokedex_completion()*100)}%"
    
# class Pokedex:
#     def __init__(self):
#         self.pokedex = set()

if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("random")
    print(t)
    print(t.get_team())
    # print(t.get_team().assemble_team(BattleMode.SET))
    print("test")
    t.get_team().assemble_team(BattleMode.ROTATE)
    print(t.get_team()[0])
    print(t.get_team()[1])