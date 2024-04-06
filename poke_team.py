from pokemon import *
import random
from typing import List
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.bset import BSet
from battle_mode import BattleMode


class PokeTeam:

    TEAM_LIMIT = 6
    POKE_LIST = list(get_all_pokemon_types())

    def __init__(self):
        self.team = ArrayR(self.TEAM_LIMIT)
        for i in range(self.TEAM_LIMIT):
            self.team[i] = None

    def choose_manually(self):
        i = 0
        while i < self.TEAM_LIMIT:
            name = input(f"Enter the name of Pokemon #{i+1} (or 'Done' to break): ")
            if name.lower() == 'done':
                break
            if name in [pokemon.__name__ for pokemon in self.POKE_LIST]:
                PokemonClass = next(pokemon for pokemon in self.POKE_LIST if pokemon.__name__ == name)
                self.team[i] = PokemonClass()
                self.team[i].id = i
                i += 1
            else:
                print(f"No Pokemon named {name} found.")

    def choose_randomly(self) -> None:
        for i in range(self.TEAM_LIMIT):
            self.team[i] = random.choice(self.POKE_LIST)()
            self.team[i].id = i
        # shuffled_pokemon = self.POKE_LIST[:]
        # for i in range(len(shuffled_pokemon) - 1, 0, -1):
        #     j = int(i * random.random())
        #     shuffled_pokemon[i], shuffled_pokemon[j] = shuffled_pokemon[j], shuffled_pokemon[i]
        # for i in range(self.TEAM_LIMIT):
        #     self.team[i] = shuffled_pokemon[i]()
        #     self.team[i].id = i
    
    def regenerate_team(self) -> None:
        for i in range(len(self.team)):
            print(self.team[i])
            print(self.team[i].get_health())
            pokemon = type(self.team[i])
            # self.team[i].health = pokemon().health
            print(self.team[i])
            print(self.team[i].get_health())
        
    def assemble_team(self, battle_mode: BattleMode) -> None:
        self.regenerate_team()
        team = self.team

        if battle_mode == BattleMode.SET:
            self.team = ArrayStack(team.__len__())
            for pokemon in reversed(team):
                # print(pokemon.name)
                self.team.push(pokemon)
            # print("TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
            # print(self.team)
        elif battle_mode == BattleMode.ROTATE:
            self.team = CircularQueue()
            for pokemon in team:
                self.team.append(pokemon)
        else:
            raise ValueError(f"Invalid battle mode")
        return self.team
        
    def special(self, battle_mode: BattleMode) -> None:
        if battle_mode == BattleMode.SET:
            mid_index = len(self.team) // 2
            self.team[:mid_index] = reversed(self.team[:mid_index])
        elif battle_mode == BattleMode.ROTATE:
            mid_index = len(self.team) // 2
            self.team[mid_index:] = reversed(self.team[mid_index:])
        elif battle_mode == BattleMode.OPTIMISE:
            self.team = self.team[::-1]
        else:
            raise ValueError(f"Invalid battle mode")

    def __getitem__(self, index: int):
        return self.team[index]

    def __len__(self):
        return len(self.team)

    def __str__(self):
        result = "Your team is: \n"
        for pokemon in self.team:
            result += f"{pokemon.name}\n"
        return result
        # return ', '.join(str(item) for item in reversed(self._data))

class Trainer:

    def __init__(self, name) -> None:
        self.name = name
        self.team = PokeTeam()
        self.pokedex = BSet()

    def pick_team(self, method: str) -> None:
        if method == "random":
            self.team.choose_randomly()
        elif method == "manual":
            self.team.choose_manually()
        else:
            print("Invalid method")
        for pokemon in self.team:
            self.register_pokemon(pokemon)

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
    t.pick_team("manual")
    print(t)
    print(t.get_team())
    # print(t.get_team().assemble_team(BattleMode.SET))
    print("test")