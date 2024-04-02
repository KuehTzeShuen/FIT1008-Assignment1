from pokemon import *
import random
from typing import List

class PokeTeam:

    TEAM_LIMIT = 6
    POKE_LIST = list(get_all_pokemon_types())

    def __init__(self):
        self.team = []

    def choose_manually(self, pokemon):
        if len(pokemon) <= self.TEAM_LIMIT:
            self.team = list(pokemon)
        else:
            print(f"You can only have {self.TEAM_LIMIT} pokemon in your team")

    def choose_randomly(self) -> None:
        self.team = [pokemon() for pokemon in random.sample(self.POKE_LIST, self.TEAM_LIMIT)]
    
    def regenerate_team(self) -> None:
        for pokemon in self.team:
            stage = self.evolution_line.index(self.name)
            pokemon.health = stage.health
        
    # def assemble_team(self) -> None:
    #     raise NotImplementedError
        
    # def special(self) -> None:
    #     raise NotImplementedError

    def __getitem__(self, index: int):
        return self.team[index]

    def len(self):
        return len(self.team)

    def __str__(self):
        result = "Your team is: \n"
        for pokemon in self.team:
            result += f"{pokemon.name}\n"
        return result

class Trainer:

    def __init__(self, name) -> None:
        self.name = name
        self.team = PokeTeam()
        self.pokedex = Pokedex()

    def pick_team(self, method: str) -> None:
        if method == "random":
            self.team.choose_randomly()
        elif method == "manual":
            self.team.choose_manually()
        else:
            print("Invalid method")

    def get_team(self) -> PokeTeam:
        return self.team

    def get_name(self) -> str:
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        self.pokedex.add(pokemon)

    def get_pokedex_completion(self) -> float:
        seen_types = set()
        for pokemon in self.team:
            seen_types.add(pokemon.poketype)
        ans = round(len(seen_types) / len(PokeType.__members__), 2)
        return ans

    def __str__(self) -> str:
        return f"Trainer {self.name} \n Pokedex Completion {self.get_pokedex_completion() * 100}%"
    
class Pokedex:
    def __init__(self):
        self.pokedex = set()

if __name__ == '__main__':
    t = Trainer('Ash')
    print("test 1")
    print(t)
    t.pick_team("random")
    print("test 2")
    print(t)
    print("test 3")
    print(t.get_team())