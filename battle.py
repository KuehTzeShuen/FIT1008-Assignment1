from math import ceil
from data_structures.referential_array import ArrayR
from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from pokemon_base import TypeEffectiveness

class Battle:

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion: str = None) -> None:
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion

    def commence_battle(self) -> Trainer | None:
        winning_team = None
        if self.battle_mode == BattleMode.SET:
            winning_team = self.set_battle()
        elif self.battle_mode == BattleMode.ROTATE:
            winning_team = self.rotate_battle()
        elif self.battle_mode == BattleMode.OPTIMISE:
            winning_team = self.optimise_battle()
        print("congrats winner")
        
        print("congrats winner")
        if winning_team == self.trainer_1.get_team():
            print(self.trainer_1)
            return self.trainer_1
        elif winning_team == self.trainer_2.get_team():
            print(self.trainer_2)
            return self.trainer_2
        return None

    def _create_teams(self) -> Tuple[PokeTeam, PokeTeam]:
        print("test2teststarttest2teststarttest2teststarttest2teststarttest2teststarttest2teststarttest2teststarttest2teststarttest2teststarttest2teststarttest2teststarttest2teststarttest2teststarttest2teststarttest2teststart")
        if self.trainer_1.team.team_count == 0:
            self.trainer_1.pick_team("random")
            print("team 1 was empty")
            print(self.trainer_1.team)
        if self.trainer_2.team.team_count == 0:
            self.trainer_2.pick_team("random")
            print("team 2 was empty")
            print(self.trainer_2.team)

        print("progress at least")
        if self.battle_mode == BattleMode.SET:
            self.trainer_1.get_team().assemble_team(BattleMode.SET)
            self.trainer_2.get_team().assemble_team(BattleMode.SET)
        elif self.battle_mode == BattleMode.ROTATE:
            self.trainer_1.get_team().assemble_team(BattleMode.ROTATE)
            self.trainer_2.get_team().assemble_team(BattleMode.ROTATE)
        elif self.battle_mode == BattleMode.OPTIMISE:
            self.trainer_1.get_team().assign_team(self.criterion)
            self.trainer_2.get_team().assign_team(self.criterion)
#        self.trainer_1.fainted_pokemon = ArrayR(self.trainer_1.get_team().team_count)
#        self.trainer_2.fainted_pokemon = ArrayR(self.trainer_2.get_team().team_count)
        # if self.battle_mode == BattleMode.ROTATE:
        #     team_1 = self.trainer_1.get_team().to_queue()
        #     team_2 = self.trainer_2.get_team().to_queue()
        # if self.battle_mode == BattleMode.OPTIMISE:
        #     team_1 = self.trainer_1.get_team().to_priority_queue(self.criterion)
        #     team_2 = self.trainer_2.get_team().to_priority_queue(self.criterion)
        print("test2")
        print("test2testend")
        return self.trainer_1, self.trainer_2

    def set_battle(self) -> PokeTeam | None:        
        print("here")

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

    def rotate_battle(self) -> PokeTeam | None:
        while self.trainer_1.get_team().team_count > 0 and self.trainer_2.get_team().team_count > 0:
            pokemon_1 = self.trainer_1.team.team.serve()
            self.trainer_1.get_team().team_count -= 1
            pokemon_2 = self.trainer_2.team.team.serve()
            self.trainer_2.get_team().team_count -= 1
            print("attacking")

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

        print("team test")
        self.trainer_1.team.team.length = 6
        print(self.trainer_1.team.team.array[0])
        print(self.trainer_1.team.team.array[1])
        print(self.trainer_1.team.team.array[2])
        return self.trainer_2.team if self.trainer_1.team.team_count == 0 else self.trainer_1.team if self.trainer_2.team.team_count == 0 else None

    def optimise_battle(self) -> PokeTeam | None:
        while self.trainer_1.get_team().team_count > 0 and self.trainer_2.get_team().team_count > 0:
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
    
    def one_on_one(self, pokemon_1, pokemon_2):
        self.trainer_1.register_pokemon(pokemon_2)
        self.trainer_2.register_pokemon(pokemon_1)
        faster_pokemon, slower_pokemon, faster_trainer, slower_trainer = (pokemon_1, pokemon_2, self.trainer_1, self.trainer_2) if pokemon_1.get_speed() >= pokemon_2.get_speed() else  (pokemon_2, pokemon_1, self.trainer_2, self.trainer_1) 

        print(f"{faster_pokemon.get_name()} has {faster_pokemon.health} health")
        print(f"{slower_pokemon.get_name()} has {slower_pokemon.health} health")
        
        faster_pokemon.calculate_damage(slower_pokemon, faster_trainer.get_pokedex_completion()/slower_trainer.get_pokedex_completion())
                # print(f"{faster_pokemon.get_name()} attacked {slower_pokemon.get_name()} for {faster_pokemon.attack(slower_pokemon)} damage.")
                # if TypeEffectiveness.get_effectiveness(faster_pokemon.poketype, slower_pokemon.poketype) > 1:
                #     print("It was super effective!!!!!!!!!!!!!!!!!!")
                # elif TypeEffectiveness.get_effectiveness(faster_pokemon.poketype, slower_pokemon.poketype) < 1:
                #     print("It was not very effective...........................")
                # print(f"{slower_pokemon.get_name()} has {slower_pokemon.health} health left")
                # if not slower_pokemon.is_alive():
                #     print(f"{slower_pokemon.get_name()} fainted")             
        if slower_pokemon.is_alive() or faster_pokemon.get_speed() == slower_pokemon.get_speed():
            slower_pokemon.calculate_damage(faster_pokemon, slower_trainer.get_pokedex_completion()/faster_trainer.get_pokedex_completion())
            # print(f"{slower_pokemon.get_name()} attacked {faster_pokemon.get_name()} for {slower_pokemon.attack(faster_pokemon)} damage")
            # if TypeEffectiveness.get_effectiveness(faster_pokemon.poketype, slower_pokemon.poketype) > 1:
            #     print("It was super effective!!!!!!!!!!!!!!!!!!")
            # elif TypeEffectiveness.get_effectiveness(faster_pokemon.poketype, slower_pokemon.poketype) < 1:
            #     print("It was not very effective.............................")
            # print(f"{faster_pokemon.get_name()} has {faster_pokemon.health} health left")
            # if not faster_pokemon.is_alive():
            #     print(f"{faster_pokemon.get_name()} fainted")
        print(f"{faster_pokemon.get_name()} has {faster_pokemon.health} health")
        print(f"{slower_pokemon.get_name()} has {slower_pokemon.health} health")
        if faster_pokemon.is_alive() and slower_pokemon.is_alive():
            faster_pokemon.health -= 1
            slower_pokemon.health -= 1
        elif faster_pokemon.is_alive() and not slower_pokemon.is_alive():
            print(f"{slower_pokemon.get_name()} fainted")
            faster_pokemon.level_up()
            print(f"{faster_pokemon.get_name()} leveled up to level {faster_pokemon.get_level()}")
        elif slower_pokemon.is_alive() and not faster_pokemon.is_alive():
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
