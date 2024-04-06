from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from pokemon_base import TypeEffectiveness

class Battle:

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion: None) -> None:
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
            return self.optimise_battle()
        print(winning_team)
        if winning_team is self.trainer_1.get_team():
            return self.trainer_1
        elif winning_team is self.trainer_2.get_team():
            return self.trainer_2
        return None

    def _create_teams(self) -> Tuple[PokeTeam, PokeTeam]:
        print("test2teststart")
        print(self.trainer_1.team)
        if self.battle_mode == BattleMode.SET:
            self.team1 = self.trainer_1.get_team().assemble_team(BattleMode.SET)
            self.team2 = self.trainer_2.get_team().assemble_team(BattleMode.SET)
        elif self.battle_mode == BattleMode.ROTATE:
            self.team1 = self.trainer_1.get_team().assemble_team(BattleMode.ROTATE)
            self.team2 = self.trainer_2.get_team().assemble_team(BattleMode.ROTATE)
        elif self.battle_mode == BattleMode.OPTIMISE:
            self.team1 = self.trainer_1.get_team().assemble_team(BattleMode.OPTIMISE)
            self.team2 = self.trainer_2.get_team().assemble_team(BattleMode.OPTIMISE)
        # if self.battle_mode == BattleMode.ROTATE:
        #     team_1 = self.trainer_1.get_team().to_queue()
        #     team_2 = self.trainer_2.get_team().to_queue()
        # if self.battle_mode == BattleMode.OPTIMISE:
        #     team_1 = self.trainer_1.get_team().to_priority_queue(self.criterion)
        #     team_2 = self.trainer_2.get_team().to_priority_queue(self.criterion)
        print("test2")
        print(self.trainer_1.team)
        print("test2testend")
        return self.team1, self.team2

    def set_battle(self) -> PokeTeam | None:
        team_1, team_2 = self._create_teams()
        
        print("here")

        while len(team_1) > 0 and len(team_2) > 0:
            pokemon_1 = team_1.pop()
            pokemon_2 = team_2.pop()

            self.one_on_one(pokemon_1, pokemon_2)

            if pokemon_1.is_alive():
                team_1.push(pokemon_1)
            if pokemon_2.is_alive():
                team_2.push(pokemon_2)

        print("\n team1")
        print(team_1)
        print("\n team2")
        print(team_2)
        return self.trainer_2 if team_1.is_empty() else self.trainer_1 if team_2.is_empty() else None

    def rotate_battle(self) -> PokeTeam | None:
        team_1, team_2 = self._create_teams()

        while not team_1.is_empty() and not team_2.is_empty():
            pokemon_1 = team_1.serve()
            pokemon_2 = team_2.serve()

            self.one_on_one(pokemon_1, pokemon_2)

            if pokemon_1.is_alive():
                team_1.append(pokemon_1)
            if pokemon_2.is_alive():
                team_2.append(pokemon_2)

        return self.trainer_2 if team_1.is_empty() else self.trainer_1 if team_2.is_empty() else None


    def optimise_battle(self) -> PokeTeam | None:
        self.trainer_1.team = Battle.assign_team(self.trainer_1.team, self.criterion)
        self.trainer_2.team = Battle.assign_team(self.trainer_2.team, self.criterion)
        team_1, team_2 = self._create_teams()

        while len(team_1) > 0 and len(team_2) > 0:
            pokemon_1 = team_1.delete_at_index(0)
            pokemon_2 = team_2.delete_at_index(0)
            
            self.one_on_one(pokemon_1, pokemon_2)

            if pokemon_1.is_alive():
                team_1.add(pokemon_1)
            if pokemon_2.is_alive():
                team_2.add(pokemon_2)
        
        return self.trainer_2 if team_1.is_empty() else self.trainer_1 if team_2.is_empty() else None


    def assign_team(self, team):
        for i in range(len(team)):
            min = i
            for j in range(i+1, len(team)):
                if getattr(team[min], self.criterion) < getattr(team[j], self.criterion):
                    min = j
            team[i], team[min] = team[min], team[i]
            print("sortedlist")
            print(team[i].get_name())
        return team
    
    def one_on_one(self, pokemon_1, pokemon_2):
        faster_pokemon = pokemon_1 if pokemon_1.get_speed() >= pokemon_2.get_speed() else pokemon_2
        slower_pokemon = pokemon_2 if pokemon_2.get_speed() >= pokemon_1.get_speed() else pokemon_1
        #faster_action = input(f"{faster_pokemon.get_name()}, choose your action: 'SPECIAL' or 'ATTACK'")
        #slower_action = input(f"{slower_pokemon.get_name()}, choose your action: 'SPECIAL' or 'ATTACK'")
        faster_action = "ATTACK"
        slower_action = "ATTACK"
        if faster_action.upper() == "SPECIAL":
            self.perform_special(faster_action)
        if slower_action.upper() == "SPECIAL":
            self.perform_special(slower_action)

        print(f"{faster_pokemon.get_name()} has {faster_pokemon.health} health")
        print(f"{slower_pokemon.get_name()} has {slower_pokemon.health} health")
        if faster_action.upper() == "ATTACK":
            slower_pokemon.health -= faster_pokemon.attack(slower_pokemon)
            print(f"{faster_pokemon.get_name()} attacked {slower_pokemon.get_name()} for {faster_pokemon.attack(slower_pokemon)} damage.")
            if TypeEffectiveness.get_effectiveness(faster_pokemon.poketype, slower_pokemon.poketype) > 1:
                print("It was super effective!!!!!!!!!!!!!!!!!!")
            elif TypeEffectiveness.get_effectiveness(faster_pokemon.poketype, slower_pokemon.poketype) < 1:
                print("It was not very effective...........................")
            print(f"{slower_pokemon.get_name()} has {slower_pokemon.health} health left")
            if not slower_pokemon.is_alive():
                print(f"{slower_pokemon.get_name()} fainted")
                        
        if slower_action.upper() == "ATTACK" and (slower_pokemon.is_alive() or faster_pokemon.get_speed() == slower_pokemon.get_speed()):
            faster_pokemon.health -= slower_pokemon.attack(faster_pokemon)
            print(f"{slower_pokemon.get_name()} attacked {faster_pokemon.get_name()} for {slower_pokemon.attack(faster_pokemon)} damage")
            if TypeEffectiveness.get_effectiveness(faster_pokemon.poketype, slower_pokemon.poketype) > 1:
                print("It was super effective!!!!!!!!!!!!!!!!!!")
            elif TypeEffectiveness.get_effectiveness(faster_pokemon.poketype, slower_pokemon.poketype) < 1:
                print("It was not very effective.............................")
            print(f"{faster_pokemon.get_name()} has {faster_pokemon.health} health left")
            if not faster_pokemon.is_alive():
                print(f"{faster_pokemon.get_name()} fainted")
        
        if faster_pokemon.is_alive() and not slower_pokemon.is_alive():
            print(f"{slower_pokemon.get_name()} fainted")
            faster_pokemon.level_up()
            print(f"{faster_pokemon.get_name()} leveled up to level {faster_pokemon.get_level()}")
        elif slower_pokemon.is_alive() and not faster_pokemon.is_alive():
            print(f"{faster_pokemon.get_name()} fainted")
            slower_pokemon.level_up()
            print(f"{slower_pokemon.get_name()} leveled up to level {slower_pokemon.get_level()}")
        print("")

    def perform_special(self, pokemon):
        # Implement the special action here
        print(f"{pokemon.get_name()} performed a special action")


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
    b = Battle(t1, t2, BattleMode.OPTIMISE, "health")
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")
