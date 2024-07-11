from abc import ABC, abstractmethod
import math
import pygame as pg


class TargetingStrategy(ABC):
    @abstractmethod
    def pick_target(self, turret, enemy_group):
        pass


class ClosestEnemyStrategy(TargetingStrategy):
    def pick_target(self, turret, enemy_group):
        closest_enemy = None
        closest_distance = float('inf')
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - turret.x
                y_dist = enemy.pos[1] - turret.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < turret.range and dist < closest_distance:
                    closest_enemy = enemy
                    closest_distance = dist
        return closest_enemy


class WeakestEnemyStrategy(TargetingStrategy):
    def pick_target(self, turret, enemy_group):
        weakest_enemy = None
        lowest_health = float('inf')
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - turret.x
                y_dist = enemy.pos[1] - turret.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < turret.range and enemy.health < lowest_health:
                    weakest_enemy = enemy
                    lowest_health = enemy.health
        return weakest_enemy
