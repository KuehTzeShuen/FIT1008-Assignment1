# Unless otherwise stated, we assume that the time complexity of the function described takes O(1) time, and the initialisation of array ADTs that use the referrential array ArrayR take O(n) time, where n is number of elements in the array.
# ADT operations for stack and queue are also assumed take O(1) time, as push and pop, append and serve are all just accessing an element from the top, or back and front of tje arrayADT respectively, unless otherwise stated.

from math import ceil
from data_structures.referential_array import ArrayR
from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode

class Battle:

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion: str = None) -> None:
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion

    # Commence_battle() is the main function that starts the battle between the two trainers.
    # The function initialises a winning_team variable to None for the winner.
    # The function then checks the battle mode and calls the appropriate battle function.
    # If the battle mode is SET, it calls the set_battle() function, which has a time complexity of O(n) where n is the number of battles played.
    # If the battle mode is ROTATE, it calls the rotate_battle() function, which has a time complexity of O(n) where n is the number of battles played.
    # If the battle mode is OPTIMISE, it calls the optimise_battle() function, which has a time complexity of O(n log n) where n is the number of pokemon in the team.
    # We then check if the winning_team is the same as the trainer's team, and return the winner trainner.
    # The function has a time complexity of O(n) if the battle mode is SET or ROTATE, and O(n log n) if the battle mode is OPTIMISE, where n is the number of pokemon in the team.
    # The best case time complexity is O(1) if the teams only have one pokemon and they both faint immedieately after the first battle.
    # The worst case time complexity is O(n log n) if the teams have n pokemon and they all faint after m optimise battles.
    def commence_battle(self) -> Trainer | None:
        winning_team = None
        if self.battle_mode == BattleMode.SET:
            winning_team = self.set_battle()
            temp_array = ArrayR(winning_team.team_count)
            for i in range(winning_team.team_count):
                temp_array[i] = winning_team.team.pop()
            for i in range(winning_team.team_count):
                winning_team.team = temp_array
        elif self.battle_mode == BattleMode.ROTATE:
            winning_team = self.rotate_battle()
            temp_array = ArrayR(winning_team.team_count)
            for i in range(winning_team.team_count):
                temp_array[i] = winning_team.team.serve()
            for i in range(winning_team.team_count):
                winning_team.team = temp_array
        elif self.battle_mode == BattleMode.OPTIMISE:
            winning_team = self.optimise_battle()
        if winning_team == self.trainer_1.get_team():
            print(self.trainer_1)
            #print(self.trainer_1.get_team())
            return self.trainer_1
        elif winning_team == self.trainer_2.get_team():
            print(self.trainer_2)
            #print(self.trainer_2.get_team())
            return self.trainer_2
        return None

    # The function first determines if the teams are empty, if they are, it will randomly pick a team for the trainer.
    # It then assembles the team based on the battle mode. If the battle mode is SET, it will assemble the team in the order they were picked etc.
    # The pick_team("random") function has a time complexity of O(n) where n is the number of pokemon in the TEAM_LIMIT.
    # The assemble_team function has a time complexity of O(n) where n is the number of pokemon in the team.
    # The assign_team function has a time complexity of O(n) where n is the number of pokemon in the team.
    # Creating the teams has a time complexity of O(n) where n is the number of pokemon in the team.
    # The best case time complexity is O(1) if the teams only have one pokemon and the battle mode is SET.
    # The worst case time complexity is O(n) if the teams have n pokemon or if team count is 0.
    def _create_teams(self) -> Tuple[PokeTeam, PokeTeam]:
        if self.trainer_1.team.team_count == 0:
            self.trainer_1.pick_team("random")
            print("team 1 was empty")
            print(self.trainer_1.team)
        if self.trainer_2.team.team_count == 0:
            self.trainer_2.pick_team("random")
            print("team 2 was empty")
            print(self.trainer_2.team)

        if self.battle_mode == BattleMode.SET:
            self.trainer_1.get_team().assemble_team(BattleMode.SET)
            self.trainer_2.get_team().assemble_team(BattleMode.SET)
        elif self.battle_mode == BattleMode.ROTATE:
            self.trainer_1.get_team().assemble_team(BattleMode.ROTATE)
            self.trainer_2.get_team().assemble_team(BattleMode.ROTATE)
        elif self.battle_mode == BattleMode.OPTIMISE:
            self.trainer_1.get_team().assign_team(self.criterion)
            self.trainer_2.get_team().assign_team(self.criterion)
        return self.trainer_1, self.trainer_2

    # The function pops the top pokemon from each team pokemon_1 and pokemon_2 and has them battle each other.
    # We then call one_on_one() to simulate the battle between the two pokemon, which has a time complexity of O(1).
    # The function then checks if the pokemon is_alive(), if it is, it pushes the pokemon back into the team, if it is not, it adds the pokemon to the fainted_pokemon array.
    # The function then repeats the process n times where n is the number of battles played, until one of the teams has no more pokemon.
    # The function has a time complexity of O(n) where n is the number of battles played.
    # The best case time complexity is O(1) if the teams only have one pokemon and they both faint immedieately after the first battle.
    # The worst case time complexity is O(n) if the teams have n pokemon and they all faint after n battles.
    def set_battle(self) -> PokeTeam | None:        
        while self.trainer_1.team.team_count > 0 and self.trainer_2.team.team_count > 0:
            pokemon_1 = self.trainer_1.team.team.pop()
            self.trainer_1.team.team_count -= 1
            pokemon_2 = self.trainer_2.team.team.pop()
            self.trainer_2.team.team_count -= 1
            self.one_on_one(pokemon_1, pokemon_2)
            if pokemon_1.is_alive():
                self.trainer_1.team.team.push(pokemon_1)
                self.trainer_1.team.team_count += 1
            else:
                self.trainer_1.team.fainted_pokemon[pokemon_1.id] = pokemon_1
            if pokemon_2.is_alive():
                self.trainer_2.team.team.push(pokemon_2)
                self.trainer_2.team.team_count += 1
            else:
                self.trainer_2.team.fainted_pokemon[pokemon_2.id] = pokemon_2
        return self.trainer_2.team if self.trainer_1.team.team_count == 0 else self.trainer_1.team if self.trainer_2.team.team_count == 0 else None

    # The function serves the front pokemon from each team pokemon_1 and pokemon_2 and has them battle each other.
    # We then call one_on_one() to simulate the battle between the two pokemon, which has a time complexity of O(1).
    # The function then checks if the pokemon is_alive(), if it is, it appends the pokemon back into the team, if it is not, it adds the pokemon to the fainted_pokemon array.
    # The function then repeats the process n times where n is the number of battles played, until one of the teams has no more pokemon.
    # The function has a time complexity of O(n) where n is the number of battles played.
    # The best case time complexity is O(1) if the teams only have one pokemon and they both faint immedieately after the first battle.
    # The worst case time complexity is O(n) if the teams have n pokemon and they all faint after n battles.
    def rotate_battle(self) -> PokeTeam | None:
        while self.trainer_1.team.team_count > 0 and self.trainer_2.team.team_count > 0:
            pokemon_1 = self.trainer_1.team.team.serve()
            self.trainer_1.team.team_count -= 1
            pokemon_2 = self.trainer_2.team.team.serve()
            self.trainer_2.team.team_count -= 1
            self.one_on_one(pokemon_1, pokemon_2)
            if pokemon_1.is_alive():
                self.trainer_1.team.team.append(pokemon_1)
                self.trainer_1.get_team().team_count += 1
            else:
                self.trainer_1.team.fainted_pokemon[pokemon_1.id] = pokemon_1
            if pokemon_2.is_alive():
                self.trainer_2.team.team.append(pokemon_2)
                self.trainer_2.get_team().team_count += 1
            else:
                self.trainer_2.team.fainted_pokemon[pokemon_2.id] = pokemon_2
        return self.trainer_2.team if self.trainer_1.team.team_count == 0 else self.trainer_1.team if self.trainer_2.team.team_count == 0 else None

    # The function assigns the team based on the criterion given. If the criterion is "health", the team is assigned in ascending order of health.
    # The function then gets the pokemon with the lowest attribute from the front of each team pokemon_1 and pokemon_2 and has them battle each other.
    # We then call one_on_one() to simulate the battle between the two pokemon, which has a time complexity of O(1).
    # The function then checks if the pokemon is_alive(), if it is, it arranges the order of the team in case the criterion attribute of the pokemon changed, which takes O(n log n) time
    # Otherwise, it adds the pokemon to the fainted_pokemon array, and calls delete_at_index() which takes O(n) time to shuffle all the pokemon leftwards into the deleted index.
    # The function then repeats the process m times for O(m) where m is the number of battles played, until one of the teams has no more pokemon.
    # The function has a time complexity of O(n log n) where n is the number of pokemon in the team.
    # The best case time complexity is O(1) if the teams only have one pokemon and they both faint immedieately after the first battle.
    # The worst case time complexity is O(m * (n log n)) if the teams have n pokemon and they all faint after m battles, as we have to rearrange after each battle as well.
    def optimise_battle(self) -> PokeTeam | None:
        while self.trainer_1.team.team_count > 0 and self.trainer_2.team.team_count > 0:
            pokemon_1 = self.trainer_1.team.team.__getitem__(0)
            pokemon_2 = self.trainer_2.team.team.__getitem__(0)
            self.one_on_one(pokemon_1, pokemon_2)
            if pokemon_1.is_alive():
                self.trainer_1.team.assign_team(self.criterion)
            else:
                self.trainer_1.team.fainted_pokemon[pokemon_1.id] = self.trainer_1.team.team.delete_at_index(0)
                print(f"{self.trainer_1.team.fainted_pokemon[pokemon_1.id]} has fainted")
                self.trainer_1.team.team_count -= 1
            if pokemon_2.is_alive():
                self.trainer_2.team.assign_team(self.criterion)
            else:
                self.trainer_2.team.fainted_pokemon[pokemon_2.id] = self.trainer_2.team.team.delete_at_index(0)
                print(f"{self.trainer_2.team.fainted_pokemon[pokemon_2.id]} has fainted")
                self.trainer_2.team.team_count -= 1
        return self.trainer_2.team if self.trainer_1.team.team_count == 0 else self.trainer_1.team if self.trainer_2.team.team_count == 0 else None
    
    # We have a one on one battle between two pokemon. When they meet, the two trainers register their opponent's pokemons, which takes O(1) time in the BSet data structure.
    # The faster_pokemon and faster_trainer attack first and the slower_pokemon and slower_trainer attack second if they are still alive.
    # The faster pokemon calculates the damage it will do to the slower pokemon and the slower pokemon calculates the damage it will do to the faster pokemon. (The type effectiveness and ppokedex completion ratio multipliers were calculated with the attack() function in the calculate_damage() function)
    # attack(), calculate_damage() and defend() are all arithmetic operations that take O(1) time.
    # The program then checks if both pokemon have 1 or more health, if they do, they both lose 1 health by calling their health attribute with O(1) time.
    # If the slower pokemon is still alive, the alive pokemon levels up and potentially evolves, and the fainted pokemon does not gain anything.
    # The function has a time complexity of O(1) as it only performs a constant number of operations.
    def one_on_one(self, pokemon_1, pokemon_2):
        self.trainer_1.register_pokemon(pokemon_2)
        self.trainer_2.register_pokemon(pokemon_1)
        faster_pokemon, slower_pokemon, faster_trainer, slower_trainer = (pokemon_1, pokemon_2, self.trainer_1, self.trainer_2) if pokemon_1.get_speed() >= pokemon_2.get_speed() else  (pokemon_2, pokemon_1, self.trainer_2, self.trainer_1) 
        faster_pokemon.calculate_damage(slower_pokemon, faster_trainer.get_pokedex_completion()/slower_trainer.get_pokedex_completion()) 
        if slower_pokemon.is_alive() or faster_pokemon.get_speed() == slower_pokemon.get_speed():
            slower_pokemon.calculate_damage(faster_pokemon, slower_trainer.get_pokedex_completion()/faster_trainer.get_pokedex_completion())
        #print(f"{faster_pokemon.get_name()} has {faster_pokemon.get_health()} health left")
        #print(f"{slower_pokemon.get_name()} has {slower_pokemon.get_health()} health left")
        if faster_pokemon.is_alive() and slower_pokemon.is_alive():
            faster_pokemon.health -= 1
            slower_pokemon.health -= 1
        if faster_pokemon.is_alive() and not slower_pokemon.is_alive():
            print(f"{slower_pokemon.get_name()} fainted")
            faster_pokemon.level_up()
            print(f"{faster_pokemon.get_name()} leveled up to level {faster_pokemon.get_level()}")
        if slower_pokemon.is_alive() and not faster_pokemon.is_alive():
            print(f"{faster_pokemon.get_name()} fainted")
            slower_pokemon.level_up()
            print(f"{slower_pokemon.get_name()} leveled up to level {slower_pokemon.get_level()}")
        print("")

if __name__ == '__main__':
    t1 = Trainer('Ash')
    t1.pick_team("random")

    t2 = Trainer('Gary')
    t2.pick_team('random')

    print(t1)
    print(t1.get_team())
    print(t2)
    print(t2.get_team())
    print("test")
    b = Battle(t1, t2, BattleMode.SET, "health")
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")
