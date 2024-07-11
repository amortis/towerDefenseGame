from random import shuffle

import pygame as pg
from enemy_data import ENEMY_SPAWN_DATA, STARTING_MONEY
import constants as c


class World():
	def __init__(self, map_image, level, map_image2=None):
		self.image = map_image
		self.map_image2 = map_image2
		self.health = c.HEALTH
		self.money = STARTING_MONEY[level-1]
		self.clicks = []
		self.enemy_list = []
		self.spawned_enemies = 0

		self.killed_enemies = 0
		self.missed_enemies = 0

		self.level = level
		self.score = 0

	def draw(self, surface, opt=0):
		if opt== 0:
			surface.blit(self.image, (0,0))
		elif opt==1:
			surface.blit(self.map_image2, (0, 0))

	def draw_clicks(self, surface):
		for click in self.clicks:
			pg.draw.circle(surface, "red", click, 5)

	def process_enemies(self):
		enemies = ENEMY_SPAWN_DATA[self.level - 1]
		for enemy_type in enemies:
			enemies_to_spawn = enemies[enemy_type]
			for enemy in range(enemies_to_spawn):
				self.enemy_list.append(enemy_type)
		# now randomize the list to shuffle the enemies
		shuffle(self.enemy_list)

	def check_level_complete(self):
		if self.killed_enemies + self.missed_enemies == len(self.enemy_list):
			return True
		else:
			return False