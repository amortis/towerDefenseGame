import pygame as pg
import constants as c
from enemy import EnemyFactory
from world import World
from random import choice
from turret import Turret
from button import Button
from database import get_level_record, save_level_record


class Game:
    def __init__(self, level, user_id):
        # Initialize Pygame
        pg.init()

        self.user_id = user_id

        # Create clock
        self.clock = pg.time.Clock()

        # Create window
        self.screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGTH))
        pg.display.set_caption("Tower Defense")

        # Gaming variables
        self.last_enemy_spawn = pg.time.get_ticks()
        self.placing_turrets = False
        self.selected_turret = None
        self.game_paused = False
        self.level_started = False
        self.game_over = False
        self.game_speed = 1
        self.game_outcome = 0
        self.level = level

        # Load images
        self.map_image = pg.image.load("bg.png").convert_alpha()
        self.map_image2 = pg.image.load("bg1.png").convert_alpha()
        self.turret_sheets = pg.image.load("assets/images/turrets/turret_1.png").convert_alpha()
        self.cursor_turret = pg.image.load("assets/images/turrets/cursor_turret.png").convert_alpha()
        self.enemy_images = {
            "weak": pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
            "medium": pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(),
            "strong": pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(),
            "elite": pg.image.load('assets/images/enemies/enemy_4.png').convert_alpha()
        }
        # buttons_image
        self.buy_turret_image = pg.image.load("assets/images/buttons_ru/buy_turret.png").convert_alpha()
        self.begin_image = pg.image.load("assets/images/buttons_ru/begin.png").convert_alpha()
        self.cancel_image = pg.image.load("assets/images/buttons_ru/cancel.png").convert_alpha()
        self.pause_image = pg.image.load("assets/images/buttons_ru/pause.png").convert_alpha()
        self.play_image = pg.image.load("assets/images/buttons_ru/play.png").convert_alpha()
        self.speed_image = pg.image.load("assets/images/buttons_ru/fast_forward.png").convert_alpha()
        self.restart_image = pg.image.load("assets/images/buttons_ru/restart.png").convert_alpha()
        self.menu_image = pg.image.load("assets/images/buttons_ru/exit.png").convert_alpha()


        # Create world
        self.world = World(self.map_image, self.level, self.map_image2)
        self.world.process_enemies()

        # переменная для туреллей
        self.opt = 0

        # Create groups
        self.enemy_group = pg.sprite.Group()
        self.turret_group = pg.sprite.Group()

        # Create buttons
        self.turret_button = Button(c.SCREEN_WIDTH + 30, 120, self.buy_turret_image, True)
        self.cancel_button = Button(c.SCREEN_WIDTH + 30, 180, self.cancel_image, True)
        self.pause_button = Button(c.SCREEN_WIDTH + 30, 240, self.pause_image, True)
        self.begin_button = Button(c.SCREEN_WIDTH + 60, 450, self.begin_image, True)
        self.play_button = Button(c.SCREEN_WIDTH + 30, 300, self.play_image, True)
        self.speed_button = Button(c.SCREEN_WIDTH + 30, 360, self.speed_image, True)
        self.restart_button = Button(310, 340, self.restart_image, True)
        self.menu_button = Button(310, 410, self.menu_image, True)
        self.right_menu_button = Button(c.SCREEN_WIDTH + 30, 550, self.menu_image, True)

        # Load fonts for displaying text on the screen
        self.text_font = pg.font.SysFont("Consolas", 24, bold=True)
        self.large_font = pg.font.SysFont("Consolas", 36)

        self.clicks = []
        self.run_game()

    def create_turret(self, mouse_pos):
        if self.world.money < c.BUY_COST: return
        fl = False
        x, y = mouse_pos
        for pos in c.TURRETS_POINTS:
            x_t, y_t = pos
            if x_t - 20 <= x <= x_t + 20 and y_t - 20 <= y <= y_t + 20:
                fl = True
                mouse_pos = pos
                break
        if not fl: return
        turret = Turret(self.turret_sheets, mouse_pos)
        self.turret_group.add(turret)
        self.world.money -= c.BUY_COST

    def select_turret(self, mouse_pos):
        fl = False
        x, y = mouse_pos
        for pos in c.TURRETS_POINTS:
            x_t, y_t = pos
            if x_t - 20 <= x <= x_t + 20 and y_t - 20 <= y <= y_t + 20:
                fl = True
                mouse_pos = pos
        if fl:
            for turret in self.turret_group:
                x, y = mouse_pos
                if (turret.x == x) and (turret.y == y):
                    return turret

    def clear_selection(self):
        for turret in self.turret_group:
            turret.selected = False

    def draw_text(self, text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    def display_game_over_message(self, message):
        overlay = pg.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGTH))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        font = pg.font.SysFont("Consolas", 48)
        text_surface = font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(c.SCREEN_WIDTH // 2, c.SCREEN_HEIGTH // 2))
        self.screen.blit(text_surface, text_rect)

    def put_record(self, score):
        save_level_record(self.user_id, self.level, score)

    def run_game(self):
        run = True
        while run:
            self.clock.tick(c.FPS * self.game_speed)

            #################
            # UPDATING SECTION
            ################
            if not self.game_paused:
                # Update groups
                self.enemy_group.update(self.world)
                self.turret_group.update(self.enemy_group)

                # Highlight selected turret
                if self.selected_turret:
                    self.selected_turret.selected = True

            #################
            # DRAWING SECTION
            ################
            self.screen.fill("grey")
            # Draw level
            self.world.draw(self.screen, self.opt)
            # Draw groups
            self.enemy_group.draw(self.screen)
            for turret in self.turret_group:
                turret.draw(self.screen)
            self.draw_text("Здоровье: " + str(self.world.health), self.text_font, "grey100", 0, 0)
            self.draw_text("Деньги: " + str(self.world.money), self.text_font, "grey100", 0, 30)
            self.draw_text("Счет: " + str(self.world.score), self.text_font, "grey100", 0, 60)

            # Draw buttons
            if self.turret_button.draw(self.screen):
                self.placing_turrets = True
                self.opt = 1
            if self.placing_turrets:
                if self.cancel_button.draw(self.screen):
                    self.placing_turrets = False
                    self.opt = 0
            if self.pause_button.draw(self.screen):
                self.game_paused = not self.game_paused
            if self.play_button.draw(self.screen):
                self.game_paused = False
            if self.speed_button.draw(self.screen):
                self.game_speed = 2 if self.game_speed == 1 else 1
            if self.right_menu_button.draw(self.screen):
                import menu
                m = menu.Menu(self.user_id)
                run = False

            if not self.game_over:
                # check if level has started
                if not self.level_started:
                    if self.begin_button.draw(self.screen):
                        self.level_started = True
                else:
                    # Spawning enemies
                    if not self.game_paused and pg.time.get_ticks() - self.last_enemy_spawn > c.SPAWN_COOLDOWN:
                        if self.world.spawned_enemies < len(self.world.enemy_list):
                            enemy_type = self.world.enemy_list[self.world.spawned_enemies]
                            enemy = EnemyFactory.create_enemy(enemy_type)
                            self.enemy_group.add(enemy)
                            self.world.spawned_enemies += 1
                            self.last_enemy_spawn = pg.time.get_ticks()
            else:
                pg.draw.rect(self.screen, "dodgerblue", (200, 200, 400, 300), border_radius=30)
                if self.game_outcome == -1:
                    self.draw_text("ИГРА ОКОНЧЕНА", self.large_font, "grey0", 250, 230)
                elif self.game_outcome == 1:
                    self.draw_text("УРОВЕНЬ ЗАВЕРШЕН", self.large_font, "grey0", 250, 230)
                self.draw_text(f"ВАШ СЧЕТ:{self.world.score}", self.large_font, "grey0", 290, 280)

                # put record
                self.put_record(self.world.score)

                # restart button
                if self.restart_button.draw(self.screen):
                    self.game_over = False
                    self.level_started = False
                    self.placing_turrets = False
                    self.selected_turret = None
                    self.game_outcome = 0
                    self.last_enemy_spawn = pg.time.get_ticks()
                    self.world = World(self.map_image, 1)
                    self.world.process_enemies()
                    # empty groups
                    self.enemy_group.empty()
                    self.turret_group.empty()
                if self.menu_button.draw(self.screen):
                    import menu
                    m = menu.Menu(self.user_id)
                    run = False

            # check if the level finished
            if self.world.check_level_complete() and not self.game_over:
                self.level_started = False
                self.game_over = True
                self.game_outcome = 1

            # check if player lost
            if self.world.health <= 0 and not self.game_over:
                self.level_started = False
                self.game_paused = True
                self.game_over = True
                self.game_outcome = -1

            # Event handler
            for event in pg.event.get():
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pg.mouse.get_pos()
                    if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGTH:
                        self.selected_turret = None
                        self.clear_selection()
                        if self.placing_turrets:
                            self.create_turret(mouse_pos)
                        else:
                            self.selected_turret = self.select_turret(mouse_pos)

                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    self.clicks.append(mouse_pos)
                    pass

            # Update display
            pg.display.flip()

