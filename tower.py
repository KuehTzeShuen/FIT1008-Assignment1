import random
from battle import Battle
from poke_team import Trainer, PokeTeam
from enum import Enum
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from typing import Tuple
from poke_team import Trainer, PokeTeam, BattleMode

class BattleTower:
    MIN_LIVES = 1
    MAX_LIVES = 3
    def __init__(self) -> None:
        self.my_trainer = None
        self.lives = 0
        self.enemy_lives_taken = 0 

    def set_my_trainer(self, trainer: Trainer) -> None:
        self.my_trainer = trainer
        self.lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)
        
    def generate_enemy_trainers(self, n: int) -> None:
        self.enemy_trainers = CircularQueue(n)
        for _ in range(n):
            trainer = Trainer('Rocket Grunt ' + str(_))
            trainer.pick_team("random")
            trainer.lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)
            # print(trainer, team, trainer.lives)
            self.enemy_trainers.append((trainer))

    def battles_remaining(self) -> bool:
        if self.lives <= 0:
            return False
        for _, _, lives in self.enemy_trainers:
            if lives > 0:
                return True
        return False

    def next_battle(self) -> Tuple[Trainer, PokeTeam, int, int]:
        if len(self.enemy_trainers) == 0:
            return "Team Wipe."

        enemy_trainer = self.enemy_trainers.serve()
        battle = Battle(self.my_trainer, enemy_trainer, BattleMode.SET)

        winner = battle.commence_battle()
        if winner == self.my_trainer:
            enemy_trainer.lives -= 1
            if enemy_trainer.lives > 0:
                self.enemy_trainers.append((enemy_trainer))
        else:
            self.lives -= 1
            self.enemy_trainers.append((enemy_trainer))

        if self.lives > 0:
            print("You won")
            return self.my_trainer, enemy_trainer, self.lives, enemy_trainer.lives
        else:
            print("Ya lost, bub")
            return self.my_trainer, enemy_trainer, self.lives, enemy_trainer.lives

    def enemies_defeated(self) -> int:
        return self.enemy_lives_taken
        
    
if __name__ == "__main__":
        tower = BattleTower()
        trainer = Trainer('Ash')
        trainer.pick_team("random")
        tower.set_my_trainer(trainer)
        tower.generate_enemy_trainers(5)
        print("here")
        tower.next_battle()
        # for _ in range(5):
        #     battle_result, my_trainer, enemy_trainer, my_lives, enemy_lives = tower.next_battle()
        #     print(f"Battle Result: {battle_result}, My Lives: {my_lives}, Enemy Lives: {enemy_lives}")

        # print(f"Total enemies defeated: {tower.enemies_defeated()}")