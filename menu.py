import pygame
import database  # Импорт функций из database.py

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense - Меню")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)

# Шрифты
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)


def draw_text(surface, text, pos, font, color=BLACK):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)


def draw_button(surface, rect, text, font, color, active_color, active):
    if active:
        pygame.draw.rect(surface, active_color, rect)
    else:
        pygame.draw.rect(surface, color, rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def main_menu(user_id):
    running = True
    start_game_active = False
    select_level_active = False
    sandbox_mode_active = False

    # Кнопки меню
    start_game_button = pygame.Rect(300, 200, 200, 60)
    select_level_button = pygame.Rect(300, 300, 200, 60)
    sandbox_mode_button = pygame.Rect(300, 400, 200, 60)

    while running:
        win.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_game_button.collidepoint(event.pos):
                    start_game_active = True
                elif select_level_button.collidepoint(event.pos):
                    select_level_active = True
                elif sandbox_mode_button.collidepoint(event.pos):
                    sandbox_mode_active = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if start_game_active and start_game_button.collidepoint(event.pos):
                    print(f"User {user_id} started the game")  # Запуск игры
                    # Здесь можно добавить логику для запуска игры
                elif select_level_active and select_level_button.collidepoint(event.pos):
                    print(f"User {user_id} selected a level")  # Выбор уровня
                    # Здесь можно добавить логику для выбора уровня
                elif sandbox_mode_active and sandbox_mode_button.collidepoint(event.pos):
                    print(f"User {user_id} entered sandbox mode")  # Режим песочницы
                    # Здесь можно добавить логику для режима песочницы

                start_game_active = False
                select_level_active = False
                sandbox_mode_active = False

        draw_button(win, start_game_button, "Начать игру", font, LIGHT_GRAY, DARK_GRAY, start_game_active)
        draw_button(win, select_level_button, "Выбрать уровень", font, LIGHT_GRAY, DARK_GRAY, select_level_active)
        draw_button(win, sandbox_mode_button, "Режим песочницы", font, LIGHT_GRAY, DARK_GRAY, sandbox_mode_active)

        pygame.display.flip()

    pygame.quit()


# Пример вызова меню
if __name__ == "__main__":
    main_menu(user_id=1)
