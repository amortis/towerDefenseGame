import pygame
import database  # Импорт функций из database.py

class Menu:
    def __init__(self, user_id):
        pygame.init()

        self.WIDTH, self.HEIGHT = 1260, 640  # Новые размеры окна
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Tower Defense - Меню")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_GRAY = (170, 170, 170)
        self.DARK_GRAY = (100, 100, 100)

        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)

        self.user_id = user_id

        button_width = 350  # Увеличенная ширина кнопок
        button_height = 60
        button_spacing = 20
        button_y_start = (self.HEIGHT - 4 * button_height - 3 * button_spacing) // 2  # Центрирование кнопок по вертикали

        self.play_button = pygame.Rect((self.WIDTH - button_width) // 2, button_y_start, button_width, button_height)
        self.records_button = pygame.Rect((self.WIDTH - button_width) // 2, button_y_start + button_height + button_spacing, button_width, button_height)
        self.help_button = pygame.Rect((self.WIDTH - button_width) // 2, button_y_start + 2 * (button_height + button_spacing), button_width, button_height)
        self.exit_button = pygame.Rect((self.WIDTH - button_width) // 2, button_y_start + 3 * (button_height + button_spacing), button_width, button_height)

        self.play_active = False
        self.records_active = False
        self.help_active = False
        self.exit_active = False

    def draw_text(self, surface, text, pos, font, color):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)

    def draw_button(self, surface, rect, text, font, color, active_color, active):
        if active:
            pygame.draw.rect(surface, active_color, rect)
        else:
            pygame.draw.rect(surface, color, rect)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def run(self):
        running = True

        while running:
            self.win.fill(self.WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.collidepoint(event.pos):
                        self.play_active = True
                    elif self.records_button.collidepoint(event.pos):
                        self.records_active = True
                    elif self.help_button.collidepoint(event.pos):
                        self.help_active = True
                    elif self.exit_button.collidepoint(event.pos):
                        self.exit_active = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.play_active and self.play_button.collidepoint(event.pos):
                        print(f"User {self.user_id} started the game")
                        # Здесь можно добавить логику для запуска игры
                    elif self.records_active and self.records_button.collidepoint(event.pos):
                        print(f"User {self.user_id} opened the records")
                        # Здесь можно добавить логику для открытия таблицы рекордов
                    elif self.help_active and self.help_button.collidepoint(event.pos):
                        print(f"User {self.user_id} opened help")
                        # Здесь можно добавить логику для открытия справки
                    elif self.exit_active and self.exit_button.collidepoint(event.pos):
                        running = False

                    self.play_active = False
                    self.records_active = False
                    self.help_active = False
                    self.exit_active = False

            self.draw_button(self.win, self.play_button, "Играть", self.font, self.LIGHT_GRAY, self.DARK_GRAY, self.play_active)
            self.draw_button(self.win, self.records_button, "Таблица рекордов", self.font, self.LIGHT_GRAY, self.DARK_GRAY, self.records_active)
            self.draw_button(self.win, self.help_button, "Справка", self.font, self.LIGHT_GRAY, self.DARK_GRAY, self.help_active)
            self.draw_button(self.win, self.exit_button, "Выход", self.font, self.LIGHT_GRAY, self.DARK_GRAY, self.exit_active)

            pygame.display.flip()

        pygame.quit()

# Пример использования:
menu = Menu(user_id=1)
menu.run()
