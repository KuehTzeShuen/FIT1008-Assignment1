# Unless otherwise stated, we assume that the time complexity of the function described takes O(1) time, and the initialisation of array ADTs that use the referrential array ArrayR take O(n) time, where n is number of elements in the array.
# ADT operations for stack and queue are also assumed take O(1) time, as push and pop, append and serve are all just accessing an element from the top, or back and front of tje arrayADT respectively, unless otherwise stated.

import random
from battle import Battle
from poke_team import Trainer, PokeTeam
from data_structures.queue_adt import CircularQueue
from typing import Tuple
from poke_team import Trainer, PokeTeam, BattleMode

class BattleTower:
    MIN_LIVES = 1
    MAX_LIVES = 3
    def __init__(self) -> None:
        self.my_trainer = None
        self.lives = 0
        self.enemy_lives_taken = 0 

    # set_my_trainer takes O(1) time as it just sets the trainer and lives, assuming random.randint takes O(1) time.
    def set_my_trainer(self, trainer: Trainer) -> None:
        self.my_trainer = trainer
        self.lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)
        
    # Initialising the enemy_trainers queue takes O(n) time, where n is the number of enemy trainers to generate.
    # Generate_enemy_trainers takes O(n) time, where n is the number of enemy trainers to generate.
    # Best case is O(1) if n = 0.
    # Worst case is O(n) if n is large.
    def generate_enemy_trainers(self, n: int) -> None:
        self.enemy_trainers = CircularQueue(n)
        for _ in range(n):
            grunt = Trainer('Rocket Grunt ' + str(_))
            grunt.pick_team("random")
            grunt.lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)
            print(grunt, grunt.get_team, grunt.lives)
            grunt.get_team().assemble_team(BattleMode.ROTATE)
            self.enemy_trainers.append((grunt))

    # Battles_remaining takes O(n) time, where n is the number of enemy trainers.
    # Best case is O(1) if n = 0.
    # Worst case is O(n) if n is large.
    def battles_remaining(self) -> bool:
        if self.lives <= 0:
            return False
        for grunt in self.enemy_trainers:
            if grunt.lives > 0:
                return True
        return False

    # Regenerate_set takes O(n) time, where n is the number of pokemon in the team.
    # Commence_battle takes O(n) time if the battle mode is set, where n is the number of pokemon in the team.
    # Commence_battle takes O(n) time if the battle mode is rotate, where n is the number of pokemon in the team.
    # Commence_battle takes O(n log n) time if the battle mode is optimise, where n is the number of pokemon in the team.
    # Next_battle takes O(m) time, where m is the number of total lives in the game.
    # Best case is O(1) if m = 0.
    # Worst case is O(m) if m is large.
    def next_battle(self) -> Tuple[Trainer, PokeTeam, int, int]:
        if len(self.enemy_trainers) == 0:
            return "Team Wipe."
        enemy_trainer = self.enemy_trainers.serve()
        self.my_trainer.get_team().regenerate_team(BattleMode.ROTATE)
        enemy_trainer.get_team().regenerate_team(BattleMode.ROTATE)
        battle = Battle(self.my_trainer, enemy_trainer, BattleMode.ROTATE)
        winner = battle.commence_battle()
        if winner == self.my_trainer:
            enemy_trainer.lives -= 1
            self.enemy_lives_taken += 1
            if enemy_trainer.lives > 0:
                self.enemy_trainers.append((enemy_trainer))
        else:
            self.lives -= 1
            self.enemy_trainers.append((enemy_trainer))
        if self.lives > 0:
            return self.my_trainer, enemy_trainer, self.lives, enemy_trainer.lives
        else:
            return self.my_trainer, enemy_trainer, self.lives, enemy_trainer.lives

    def enemies_defeated(self) -> int:
        return self.enemy_lives_taken
        
    
if __name__ == "__main__":
        tower = BattleTower()
        trainer = Trainer('Ash')
        trainer.pick_team("random")
        tower.set_my_trainer(trainer)
        tower.generate_enemy_trainers(5)
        tower.next_battle()
        # for _ in range(5):
        #     battle_result, my_trainer, enemy_trainer, my_lives, enemy_lives = tower.next_battle()
        #     print(f"Battle Result: {battle_result}, My Lives: {my_lives}, Enemy Lives: {enemy_lives}")

        # print(f"Total enemies defeated: {tower.enemies_defeated()}")