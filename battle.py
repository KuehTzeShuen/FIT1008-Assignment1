from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode
from data_structures.stack_adt import ArrayStack


class Battle:

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion

    def commence_battle(self) -> Trainer | None:
        if self.battle_mode == BattleMode.SET:
            return self.set_battle()
        elif self.battle_mode == BattleMode.ROTATE:
            return self.rotate_battle()
        elif self.battle_mode == BattleMode.OPTIMISE:
            return self.optimise_battle()

    def _create_teams(self) -> Tuple[PokeTeam, PokeTeam]:
        print("test2teststart")
        if self.battle_mode == BattleMode.SET:
            self.team1 = self.trainer_1.get_team().assemble_team(BattleMode.SET)
            self.team2 = self.trainer_2.get_team().assemble_team(BattleMode.SET)
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
        pokemon_1 = team_1.pop()
        pokemon_2 = team_2.pop()
        print(pokemon_1)
        print(pokemon_2)
        while len(team_1) > 0 and len(team_2) > 0:
            while pokemon_1.get_health() > 0 and pokemon_2.get_health() > 0:
                if pokemon_1.get_speed() > pokemon_2.speed():
                    pokemon_2.health -= pokemon_1.attack(pokemon_2)
                    if pokemon_2.get_health() > 0:
                        pokemon_1.health -= pokemon_2.attack(pokemon_1)
                elif pokemon_1.get_speed() < pokemon_2.speed():
                    pokemon_1.health -= pokemon_2.attack(pokemon_1)
                    if pokemon_1.get_health() > 0:
                        pokemon_2.health -= pokemon_1.attack(pokemon_2)
                elif pokemon_1.get_speed() == pokemon_2.speed():
                    pokemon_2.health -= pokemon_1.attack(pokemon_2)
                    pokemon_1.health -= pokemon_2.attack(pokemon_1)
            if pokemon_1.get_health() > 0 and len(team_1) > 0:
                pokemon_1 = team_1.pop()
            elif pokemon_2.get_health() > 0 and len(team_2) > 0:
                pokemon_2 = team_2.pop()
        if len(team_1) > 0:
            return self.trainer_1
        elif len(team_2) > 0:
            return self.trainer_2
        else:
            return None

    def rotate_battle(self) -> PokeTeam | None:
        team_1, team_2 = self._create_teams()
        while len(team_1) > 0 and len(team_2) > 0:
            pokemon_1 = team_1.pop()
            pokemon_2 = team_2.pop()
            while pokemon_1.get_health() > 0 and pokemon_2.get_health() > 0:
                pokemon_1.attack(pokemon_2)
                pokemon_2.attack(pokemon_1)
                team_1.push(pokemon_1)
                team_2.push(pokemon_2)
                pokemon_1 = team_1.pop()
                pokemon_2 = team_2.pop()
            if pokemon_1.get_health() > 0:
                return self.trainer_1
            elif pokemon_2.get_health() > 0:
                return self.trainer_2
        return None

    def optimise_battle(self) -> PokeTeam | None:
        team_1, team_2 = self._create_teams()
        while len(team_1) > 0 and len(team_2) > 0:
            pokemon_1 = team_1.pop()
            pokemon_2 = team_2.pop()
            while pokemon_1.get_health() > 0 and pokemon_2.get_health() > 0:
                if pokemon_1.get_speed() > pokemon_2.speed():
                    pokemon_2.health -= pokemon_1.attack(pokemon_2)
                    if pokemon_2.get_health() > 0:
                        pokemon_1.health -= pokemon_2.attack(pokemon_1)
                elif pokemon_1.get_speed() < pokemon_2.speed():
                    pokemon_1.health -= pokemon_2.attack(pokemon_1)
                    if pokemon_1.get_health() > 0:
                        pokemon_2.health -= pokemon_1.attack(pokemon_2)
                elif pokemon_1.get_speed() == pokemon_2.speed():
                    pokemon_2.health -= pokemon_1.attack(pokemon_2)
                    pokemon_1.health -= pokemon_2.attack(pokemon_1)

                team_1.push(pokemon_1)
                team_2.push(pokemon_2)
                pokemon_1 = team_1.pop()
                pokemon_2 = team_2.pop()
            if pokemon_1.get_health() > 0:
                return self.trainer_1
            elif pokemon_2.get_health() > 0:
                return self.trainer_2
        return None


if __name__ == '__main__':
    t1 = Trainer('Ash')
    t1.pick_team("random")

    t2 = Trainer('Gary')
    t2.pick_team('random')

    print(t1)
    print(t1.get_team())
    print(t2)
    print("test")
    b = Battle(t1, t2, BattleMode.SET)
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")
