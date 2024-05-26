import math

import pygame as pg
import constants as c

from TargetingStrategy import ClosestEnemyStrategy, WeakestEnemyStrategy


class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheet, pos, targeting_strategy=ClosestEnemyStrategy()):
        pg.sprite.Sprite.__init__(self)
        self.cooldown = 100
        self.range = 90
        self.last_shot = pg.time.get_ticks()
        self.selected = False
        self.target = None
        self.targeting_strategy = targeting_strategy
        #animations vars
        self.sprite_sheet = sprite_sheet
        self.animation_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()

        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.x, self.y = pos

        # update image
        self.angle = 90
        self.original_image = self.animation_list[self.frame_index]
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # create transparent circle showing range
        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center


    def load_images(self):
        # extract images from spritesheet
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self, enemy_group):
        # if target picked, play firing animation
        if self.target:
            self.play_animation()
        else:
            # search for new target once turret has cooled down
            if pg.time.get_ticks() - self.last_shot > self.cooldown:
                self.pick_target(enemy_group)

    def pick_target(self, enemy_group):
        self.target = self.targeting_strategy.pick_target(self, enemy_group)
        if self.target:
            x_dist = self.target.pos[0] - self.x
            y_dist = self.target.pos[1] - self.y
            self.angle = math.degrees(math.atan2(-y_dist, x_dist))
            self.target.health -= c.DAMAGE

    def play_animation(self):
        # update image
        self.original_image = self.animation_list[self.frame_index]
        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            # check if the animation has finished and reset to idle
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
                # record completed time and clear target so cooldown can begin
                self.last_shot = pg.time.get_ticks()
                self.target = None

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)