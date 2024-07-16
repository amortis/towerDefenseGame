import pygame
import database  # Импорт функций из database.py
from button import Button


class Menu:
    def __init__(self, user_id):

        pygame.init()

        self.WIDTH, self.HEIGHT = 1260, 780  # Новые размеры окна
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Стражи пути - Меню")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_GRAY = (170, 170, 170)
        self.DARK_GRAY = (100, 100, 100)

        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)

        self.user_id = user_id
        self.unlocked_levels = len(database.get_level_records(self.user_id))

        button_width = 350  # Увеличенная ширина кнопок
        button_height = 60
        button_spacing = 20
        button_y_start = (
                                     self.HEIGHT - 4 * button_height - 3 * button_spacing) // 2  # Центрирование кнопок по вертикали

        self.play_button = pygame.Rect((self.WIDTH - button_width) // 2, button_y_start, button_width, button_height)
        self.records_button = pygame.Rect((self.WIDTH - button_width) // 2,
                                          button_y_start + button_height + button_spacing, button_width, button_height)
        self.help_button = pygame.Rect((self.WIDTH - button_width) // 2,
                                       button_y_start + 2 * (button_height + button_spacing), button_width,
                                       button_height)
        self.exit_button = pygame.Rect((self.WIDTH - button_width) // 2,
                                       button_y_start + 3 * (button_height + button_spacing), button_width,
                                       button_height)

        self.play_active = False
        self.records_active = False
        self.help_active = False
        self.exit_active = False
        self.main_menu_active = True
        self.level_select_active = False
        self.help_page = 1


        # Кнопка назад и кнопки уровней
        self.back_button = pygame.Rect(20, 20, 150, 50)
        self.level_buttons = [pygame.Rect((self.WIDTH - 100 * 5 - 20 * 4) // 2 + (i % 5) * (100 + 20),
                                          100 + (i // 5) * (50 + 20), 100, 50) for i in range(15)]

        # КАРТИНКИ ДЛЯ ТУТОРИАЛА
        # buttons_image
        self.buy_turret_image = pygame.image.load("assets/images/buttons_ru/buy_turret.png").convert_alpha()
        self.begin_image = pygame.image.load("assets/images/buttons_ru/begin.png").convert_alpha()
        self.cancel_image = pygame.image.load("assets/images/buttons_ru/cancel.png").convert_alpha()
        self.pause_image = pygame.image.load("assets/images/buttons_ru/pause.png").convert_alpha()
        self.play_image = pygame.image.load("assets/images/buttons_ru/play.png").convert_alpha()
        self.speed_image = pygame.image.load("assets/images/buttons_ru/fast_forward.png").convert_alpha()
        self.restart_image = pygame.image.load("assets/images/buttons_ru/restart.png").convert_alpha()
        self.menu_image = pygame.image.load("assets/images/buttons_ru/exit.png").convert_alpha()
        self.next_image = pygame.image.load("assets/images/buttons_ru/next-button-image.png").convert_alpha()
        self.prev_image = pygame.image.load("assets/images/buttons_ru/previous-button-image.png").convert_alpha()
        self.next_image = pygame.transform.scale(self.next_image, (128, 128))
        self.prev_image = pygame.transform.scale(self.prev_image, (128, 128))
        self.help_page = 1

        # Добавить кнопки для навигации по страницам справки
        self.next_button = Button(self.WIDTH - 150, 200, self.next_image, True)  # Позиция и размер кнопки "Вперед"
        self.prev_button = Button(10, 200, self.prev_image, True)  # Позиция и размер кнопки "Назад"

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

    def get_top_scores(self):
        records = database.get_top_level_records()
        top_scores = [(database.get_username(record[1]), record[2], record[3]) for record in records]
        return top_scores

    def draw_table(self, surface, data, pos, font, color):
        x, y = pos
        col_widths = [50, 300, 130, 100]  # Ширина колонок
        row_height = 40  # Высота строки
        header = ["#", "Имя пользователя", "Уровень", "Очки"]

        # Рисуем заголовки
        for i, heading in enumerate(header):
            pygame.draw.rect(surface, self.LIGHT_GRAY, (x, y, col_widths[i], row_height))
            text_surface = font.render(heading, True, self.BLACK)
            text_rect = text_surface.get_rect(center=(x + col_widths[i] // 2, y + row_height // 2))
            surface.blit(text_surface, text_rect)
            x += col_widths[i]

        # Рисуем данные
        y += row_height
        for row in data:
            x = pos[0]
            for i, item in enumerate(row):
                pygame.draw.rect(surface, self.WHITE, (x, y, col_widths[i], row_height))
                text_surface = font.render(str(item), True, color)
                text_rect = text_surface.get_rect(center=(x + col_widths[i] // 2, y + row_height // 2))
                surface.blit(text_surface, text_rect)
                x += col_widths[i]
            y += row_height

        # Рисуем границы
        for i in range(len(data) + 1):  # Включаем границы для заголовков
            pygame.draw.line(surface, self.BLACK, (pos[0], pos[1] + i * row_height),
                             (pos[0] + sum(col_widths), pos[1] + i * row_height))
        for i in range(len(header) + 1):
            pygame.draw.line(surface, self.BLACK, (pos[0] + sum(col_widths[:i]), pos[1]),
                             (pos[0] + sum(col_widths[:i]), pos[1] + (len(data) + 1) * row_height))
        # Рисуем нижнюю линию в конце таблицы
        pygame.draw.line(surface, self.BLACK, (pos[0], pos[1] + (len(data) + 1) * row_height),
                            (pos[0] + sum(col_widths), pos[1] + (len(data) + 1) * row_height))

    def draw_help_page1(self):
        # Отрисовка первой страницы справки
        self.draw_text(self.win, "Как играть:", (self.WIDTH // 2 - 600, 100), font=self.font, color=self.BLACK)
        self.draw_text(self.win, "1. Цель игры - защитить свою базу от волны врагов.", (self.WIDTH // 2 - 600, 150),
                       font=self.font, color=self.BLACK)
        self.draw_text(self.win, "2. Размещайте турели на поле, чтобы уничтожать врагов.", (self.WIDTH // 2 - 600, 200),
                       font=self.font, color=self.BLACK)
        self.draw_text(self.win, "3. Используйте деньги, чтобы покупать турели.", (self.WIDTH // 2 - 600, 250),
                       font=self.font, color=self.BLACK)
        self.draw_text(self.win, "4. Убедитесь, что враги не достигнут конца маршрута.", (self.WIDTH // 2 - 600, 300),
                       font=self.font, color=self.BLACK)
        self.draw_text(self.win, "Кнопки:", (self.WIDTH // 2 - 600, 350), font=self.font, color=self.BLACK)

        self.win.blit(self.buy_turret_image, (self.WIDTH // 2 - 600, 400))
        self.draw_text(self.win, "- Покупает новую турель для размещения на поле в кругах.",
                       (self.WIDTH // 2 - 400, 410), font=self.font, color=self.BLACK)

        self.win.blit(self.cancel_image, (self.WIDTH // 2 - 600, 450))
        self.draw_text(self.win, "- Отменяет покупку туррели.", (self.WIDTH // 2 - 400, 460), font=self.font,
                       color=self.BLACK)

        self.win.blit(self.pause_image, (self.WIDTH // 2 - 600, 500))
        self.draw_text(self.win, "- Приостанавливает игру.", (self.WIDTH // 2 - 400, 510), font=self.font,
                       color=self.BLACK)

        self.win.blit(self.play_image, (self.WIDTH // 2 - 600, 550))
        self.draw_text(self.win, "- Продолжает приостановленную игру.", (self.WIDTH // 2 - 400, 560),
                       font=self.font, color=self.BLACK)

        self.win.blit(self.speed_image, (self.WIDTH // 2 - 600, 600))
        self.draw_text(self.win, "- Увеличивает скорость игры.", (self.WIDTH // 2 - 400, 610),
                       font=self.font, color=self.BLACK)

        self.win.blit(self.menu_image, (self.WIDTH // 2 - 600, 650))
        self.draw_text(self.win, "- Возвращает в главное меню.", (self.WIDTH // 2 - 400, 660),
                       font=self.font, color=self.BLACK)

    def draw_help_page2(self):
        # Отрисовка второй страницы справки
        self.draw_text(self.win, "Типы врагов:", (self.WIDTH // 2 - 500, 100), font=self.font, color=self.BLACK)

        self.win.blit(pygame.image.load("assets/images/enemies/enemy_1.png").convert_alpha(), (self.WIDTH // 2 - 500, 130))
        self.draw_text(self.win, "Слабый - Низкое здоровье, медленная скорость.", (self.WIDTH // 2 - 400, 160),
                       font=self.font, color=self.BLACK)

        self.win.blit(pygame.image.load("assets/images/enemies/enemy_2.png").convert_alpha(), (self.WIDTH // 2 - 500, 200))
        self.draw_text(self.win, "Средний - Среднее здоровье, средняя скорость.", (self.WIDTH // 2 - 400, 230),
                       font=self.font, color=self.BLACK)

        self.win.blit(pygame.image.load("assets/images/enemies/enemy_3.png").convert_alpha(), (self.WIDTH // 2 - 500, 280))
        self.draw_text(self.win, "Сильный - Высокое здоровье, быстрая скорость.", (self.WIDTH // 2 - 400, 310),
                       font=self.font, color=self.BLACK)

        self.win.blit(pygame.image.load("assets/images/enemies/enemy_1.png").convert_alpha(), (self.WIDTH // 2 - 500, 350))
        self.draw_text(self.win, "Элитный - Очень высокое здоровье, высокая скорость.", (self.WIDTH // 2 - 400, 380),
                       font=self.font, color=self.BLACK)

    def run(self):
        running = True

        while running:
            self.win.fill(self.WHITE)

            if self.main_menu_active:
                self.draw_text(self.win, database.get_username(self.user_id), (10, 10), self.font, self.BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.main_menu_active = True
                        self.level_select_active = False
                        self.records_active = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.main_menu_active:
                        if self.play_button.collidepoint(event.pos):
                            self.main_menu_active = False
                            self.level_select_active = True
                        elif self.records_button.collidepoint(event.pos):
                            self.main_menu_active = False
                            self.records_active = True
                        elif self.help_button.collidepoint(event.pos):
                            self.main_menu_active = False
                            self.help_active = True
                        elif self.exit_button.collidepoint(event.pos):
                            running = False
                    elif self.level_select_active:
                        if self.back_button.collidepoint(event.pos):
                            self.help_page = 1
                            self.main_menu_active = True
                            self.level_select_active = False
                        else:
                            for i, button in enumerate(self.level_buttons):
                                if button.collidepoint(event.pos) and i <= self.unlocked_levels:
                                    # Запуск игры
                                    import game  # Ленивый импорт
                                    game.Game(user_id=self.user_id, level=i + 1)
                                    self.level_select_active = False
                                    self.main_menu_active = True
                    elif self.records_active or self.help_active:
                        if self.back_button.collidepoint(event.pos):
                            self.main_menu_active = True
                            self.records_active = False
                            self.help_page = 1

            if self.main_menu_active:
                self.draw_text(self.win, "Стражи пути", (self.WIDTH // 2 - 100, 20), self.font, color=self.BLACK)
                self.draw_button(self.win, self.play_button, "Играть", self.font, self.LIGHT_GRAY, self.DARK_GRAY,
                                 False)
                self.draw_button(self.win, self.records_button, "Таблица рекордов", self.font, self.LIGHT_GRAY,
                                 self.DARK_GRAY, False)
                self.draw_button(self.win, self.help_button, "Справка", self.font, self.LIGHT_GRAY, self.DARK_GRAY,
                                 False)
                self.draw_button(self.win, self.exit_button, "Выход", self.font, self.LIGHT_GRAY, self.DARK_GRAY, False)
            elif self.level_select_active:
                self.draw_text(self.win, "Выбор уровня", (self.WIDTH // 2 - 100, 20), font=self.font, color=self.BLACK)
                self.draw_button(self.win, self.back_button, "Назад", self.small_font, self.LIGHT_GRAY, self.DARK_GRAY,
                                 False)
                unlocked_levels = len(database.get_level_records(self.user_id)) + 1
                for i, button in enumerate(self.level_buttons):
                    self.draw_button(self.win, button, str(i + 1), self.small_font, self.LIGHT_GRAY, self.DARK_GRAY,
                                     i < unlocked_levels)
            elif self.records_active:
                self.draw_text(self.win, "Таблица рекордов", (self.WIDTH // 2 - 150, 20), font=self.font,
                               color=self.BLACK)
                self.draw_button(self.win, self.back_button, "Назад", self.small_font, self.LIGHT_GRAY, self.DARK_GRAY,
                                 False)
                top_scores = self.get_top_scores()
                formatted_scores = [(i + 1, username, level, score) for i, (username, level, score) in
                                    enumerate(top_scores)]
                self.draw_table(self.win, formatted_scores, ((self.WIDTH - 550) // 2, 100), self.small_font, self.BLACK)
            elif self.help_active:
                self.draw_text(self.win, "Справка", (self.WIDTH // 2 - 100, 20), font=self.font, color=self.BLACK)

                if self.help_page == 1:
                    self.draw_help_page1()
                    if self.next_button.draw(self.win):
                        self.help_page = 2
                elif self.help_page == 2:
                    self.draw_help_page2()
                    if self.prev_button.draw(self.win):
                        self.help_page = 1

                self.draw_button(self.win, self.back_button, "Назад", self.small_font, self.LIGHT_GRAY, self.DARK_GRAY,
                                 False)

            pygame.display.flip()

