import random
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
        self.enemy_trainers = []
        for _ in range(n):
            trainer = Trainer('Enemy Trainer')
            trainer.pick_team("random")
            team = trainer.get_team()
            team.assemble_team(BattleMode.ROTATE)
            lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)
            self.enemy_trainers.append((trainer, team, lives))

    def battles_remaining(self) -> bool:
        if self.lives <= 0:
            return False
        for _, _, lives in self.enemy_trainers:
            if lives > 0:
                return True
        return False

    def next_battle(self) -> Tuple[Trainer, PokeTeam, int, int]:
        # Get the next enemy trainer
        enemy_trainer, enemy_team, enemy_lives = self.enemy_trainers.pop(0)

        # Simulate the battle
        battle_result = self.my_trainer.battle(enemy_trainer)

        # Update lives based on the battle result
        if battle_result == BattleResult.PLAYER_WIN:
            enemy_lives -= 1
            self.enemy_lives_taken += 1  # Add this line
        elif battle_result == BattleResult.ENEMY_WIN:
            self.lives -= 1

        # Return the battle result and the remaining lives
        return battle_result, self.my_trainer, enemy_trainer, self.lives, enemy_lives

    def enemies_defeated(self) -> int:
        return self.enemy_lives_taken
        
    
if __name__ == "__main__":
        tower = BattleTower()
        trainer = Trainer('Ash')
        tower.set_my_trainer(trainer)
        tower.generate_enemy_trainers(5)
        print(tower.generate_enemy_trainers(5))
        # for _ in range(5):
        #     battle_result, my_trainer, enemy_trainer, my_lives, enemy_lives = tower.next_battle()
        #     print(f"Battle Result: {battle_result}, My Lives: {my_lives}, Enemy Lives: {enemy_lives}")

        # print(f"Total enemies defeated: {tower.enemies_defeated()}")