from random import shuffle

import pygame as pg
from enemy_data import ENEMY_SPAWN_DATA
import constants as c

class World():
	def __init__(self, map_image):
		self.image = map_image
		self.health = c.HEALTH
		self.money = c.MONEY
		self.clicks = []
		self.enemy_list = []
		self.spawned_enemies = 0
		self.level = 1

	def draw(self, surface):
		surface.blit(self.image, (0,0))

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