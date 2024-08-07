import pygame as pg
from pygame.math import Vector2
import math
from constants import KILL_REWARD, WAY_S, WAY_M, WAY_L, WORLD_DAMAGE
from enemy_data import ENEMY_DATA


class Enemy(pg.sprite.Sprite):
	def __init__(self, waypoints, image, health, speed, reward):
		pg.sprite.Sprite.__init__(self)
		self.waypoints = waypoints
		self.pos = Vector2(self.waypoints[0])
		self.target_waypoint = 1
		self.angle = 0
		self.original_image = image
		self.image = pg.transform.rotate(self.original_image, self.angle)
		self.rect = self.image.get_rect()
		self.rect.center = (int(self.pos.x), int(self.pos.y))

		# game charecteristics
		self.health = health
		self.damage = 0
		self.speed = speed

		self.reward_score = reward


	def update(self, world):
		self.move(world)
		self.rotate()
		self.check_alive(world)

	def move(self, world):
		# определить целевую контрольную точку
		if self.target_waypoint < len(self.waypoints):
			self.target = Vector2(self.waypoints[self.target_waypoint])
			self.movement = self.target - self.pos
		else:
			# враг достиг конца пути
			self.kill()
			world.health -= WORLD_DAMAGE
			world.missed_enemies += 1
			world.score -= 1

		# рассчитать расстояние до цели
		dist = self.movement.length()
		# проверка расстояния и переход к следующей контрольной точке
		if dist >= self.speed:
			self.pos += self.movement.normalize() * self.speed
			self.rect.center = (int(self.pos.x), int(self.pos.y))
		else:
			if dist != 0:
				self.pos += self.movement.normalize() * dist
			self.target_waypoint += 1

	def rotate(self):
		#calculate distance to next waypoint
		dist = self.target - self.pos
		#use dist to calculate angle
		self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
		#rotate image and rotate tect
		self.image = pg.transform.rotate(self.original_image, self.angle)
		self.rect = self.image.get_rect()
		self.rect.center = (int(self.pos.x), int(self.pos.y))

	def check_alive(self, world):
		if self.health <= 0:
			world.money += KILL_REWARD
			world.score += self.reward_score
			world.killed_enemies += 1
			self.kill()

class Weak(Enemy):
	enemy_image = None
	way = WAY_S


	def __init__(self):
		if Weak.enemy_image is None:
			Weak.enemy_image = pg.image.load("assets/images/enemies/enemy_1.png").convert_alpha()
		super().__init__(self.way, self.enemy_image, int(ENEMY_DATA["weak"]["health"]), int(ENEMY_DATA["weak"]["speed"]), 1)


class Medium(Enemy):
	enemy_image = None
	way = WAY_M

	def __init__(self):
		Medium.enemy_image = pg.image.load("assets/images/enemies/enemy_2.png").convert_alpha()
		super().__init__(self.way, self.enemy_image, int(ENEMY_DATA["medium"]["health"]), int(ENEMY_DATA["medium"]["speed"]), 3)


class Strong(Enemy):
	enemy_image = None
	way = WAY_L

	def __init__(self):
		Strong.enemy_image = pg.image.load("assets/images/enemies/enemy_3.png").convert_alpha()
		super().__init__(self.way, self.enemy_image, int(ENEMY_DATA["strong"]["health"]), int(ENEMY_DATA["strong"]["speed"]), 5)


class Elite(Enemy):
	enemy_image = None
	way = WAY_L

	def __init__(self):
		Elite.enemy_image = pg.image.load("assets/images/enemies/enemy_4.png").convert_alpha()
		super().__init__(self.way, self.enemy_image, int(ENEMY_DATA["elite"]["health"]), int(ENEMY_DATA["elite"]["speed"]), 10)


class EnemyFactory():
	@staticmethod
	def create_enemy(enemy_type):
		if enemy_type == "medium":
			return Medium()
		elif enemy_type == "weak":
			return Weak()
		elif enemy_type == "strong":
			return Strong()
		elif enemy_type == "elite":
			return Elite()
		else: raise ValueError("Unknown class type")


