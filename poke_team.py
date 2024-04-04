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
        self.team = []

    def choose_manually(self, pokemon):
        if len(pokemon) <= self.TEAM_LIMIT:
            pokemon_classes = {cls.__name__: cls for cls in self.POKE_LIST}
            self.team = [pokemon_classes[name]() for name in pokemon.name if name in pokemon_classes]
        else:
            print(f"You can only have {self.TEAM_LIMIT} pokemon in your team")

    def choose_randomly(self) -> None:
        self.team = [pokemon() for pokemon in random.sample(self.POKE_LIST, self.TEAM_LIMIT)]
    
    def regenerate_team(self) -> None:
        for i in range(len(self.team)):
            pokemon = type(self.team[i])
            self.team[i].health = pokemon().health
        
    def assemble_team(self, battle_mode: BattleMode) -> None:
        team = self.team

        if battle_mode == BattleMode.SET:
            self.team = ArrayStack(team.__len__())
            for pokemon in reversed(team):
                self.team.push(pokemon)
            print(self.team)
        elif battle_mode == BattleMode.ROTATE:
            self.team = CircularQueue()
            for pokemon in team:
                self.team.append(pokemon)
        else:
            raise ValueError(f"Invalid battle mode")
        return self.team
        
    # def special(self) -> None:
    #     raise NotImplementedError

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
    t.pick_team("random")
    print(t)
    print(t.get_team())
    print(t.get_team().assemble_team(BattleMode.SET))
    print("test")