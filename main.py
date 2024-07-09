import pygame as pg

import constants as c
from enemy import EnemyFactory
from world import World
from random import choice
from turret import Turret
from button import Button

# Initialize Pygame
pg.init()

def create_turret(mouse_pos):
    if world.money < c.BUY_COST: return
    fl = False
    x, y = mouse_pos
    for pos in c.TURRETS_POINTS:
        x_t, y_t = pos
        if x_t - 20 <= x <= x_t + 20 and y_t - 20 <= y <= y_t + 20:
            fl = True
            mouse_pos = pos
            break
    if not fl: return
    turret = Turret(turret_sheets, mouse_pos)
    turret_group.add(turret)
    world.money -= c.BUY_COST

def select_turret(mouse_pos):
    fl = False
    x, y = mouse_pos
    for pos in c.TURRETS_POINTS:
        x_t, y_t = pos
        if x_t - 20 <= x <= x_t + 20 and y_t - 20 <= y <= y_t + 20:
            fl = True
            mouse_pos = pos
    if fl:
        for turret in turret_group:
            x, y = mouse_pos
            if (turret.x == x) and (turret.y == y):
                return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False

# Create clock
clock = pg.time.Clock()

# Create window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGTH))
pg.display.set_caption("Tower Defense")

# Gaming variables
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None
game_paused = False
game_speed = 1

# Load images
map_image = pg.image.load("bg1.png").convert_alpha()
turret_sheets = pg.image.load("assets/images/turrets/turret_1.png").convert_alpha()
cursor_turret = pg.image.load("assets/images/turrets/cursor_turret.png").convert_alpha()
enemy_images = {
    "weak": pg.image.load('assets/images/enemies/enemy_1.png').convert_alpha(),
    "medium": pg.image.load('assets/images/enemies/enemy_2.png').convert_alpha(),
    "strong": pg.image.load('assets/images/enemies/enemy_3.png').convert_alpha(),
    "elite": pg.image.load('assets/images/enemies/enemy_4.png').convert_alpha()
}
buy_turret_image = pg.image.load("assets/images/buttons/buy_turret.png").convert_alpha()
cancel_image = pg.image.load("assets/images/buttons/cancel.png").convert_alpha()
pause_image = pg.image.load("assets/images/buttons/pause.png").convert_alpha()
play_image = pg.image.load("assets/images/buttons/play.png").convert_alpha()
speed_image = pg.image.load("assets/images/buttons/fast_forward.png").convert_alpha()

# Create world
world = World(map_image)
world.process_enemies()

# Create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Create buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, buy_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 30, 180, cancel_image, True)
pause_button = Button(c.SCREEN_WIDTH + 30, 240, pause_image, True)
play_button = Button(c.SCREEN_WIDTH + 30, 300, play_image, True)
speed_button = Button(c.SCREEN_WIDTH + 50, 360, speed_image, True)

# Load fonts for displaying text on the screen
text_font = pg.font.SysFont("Consolas", 24, bold=True)
large_font = pg.font.SysFont("Consolas", 36)

# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

clicks = []
# Game loop
run = True
while run:
    clock.tick(c.FPS * game_speed)

    #################
    # UPDATING SECTION
    ################
    if not game_paused:
        # Update groups
        enemy_group.update(world)
        turret_group.update(enemy_group)

        # Highlight selected turret
        if selected_turret:
            selected_turret.selected = True

    #################
    # DRAWING SECTION
    ################
    screen.fill("grey")
    # Draw level
    world.draw(screen)
    # Draw groups
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)
    draw_text("Health: " + str(world.health), text_font, "grey100", 0, 0)
    draw_text("Money: " + str(world.money), text_font, "grey100", 0, 30)

    # Draw buttons
    if turret_button.draw(screen):
        placing_turrets = True
    if placing_turrets:
        if cancel_button.draw(screen):
            placing_turrets = False
    if pause_button.draw(screen):
        game_paused = not game_paused
    if play_button.draw(screen):
        game_paused = False
    if speed_button.draw(screen):
        game_speed = 2 if game_speed == 1 else 1

    # Spawning enemies
    if not game_paused and pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
        if world.spawned_enemies < len(world.enemy_list):
            enemy_type = world.enemy_list[world.spawned_enemies]
            enemy = EnemyFactory.create_enemy(enemy_type)
            enemy_group.add(enemy)
            world.spawned_enemies += 1
            last_enemy_spawn = pg.time.get_ticks()

    # Event handler
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGTH:
                selected_turret = None
                clear_selection()
                if placing_turrets:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            clicks.append(mouse_pos)
            pass

    # Update display
    pg.display.flip()

pg.quit()
