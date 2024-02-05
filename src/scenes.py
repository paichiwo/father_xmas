import pygame
from src.config import WHITE, GREEN, WIDTH, HEIGHT, FONT_8


class MainMenuScene:
    def __init__(self, screen, window):

        # General setup
        self.screen = screen
        self.window = window

        self.start_game = False

        self.main_menu = True
        self.options_menu = False
        self.scores_screen = False
        self.credits_screen = False

        # Main menu
        self.menu_items = ['START', 'OPTIONS', 'SCORES', 'CREDITS']
        self.selected_option = 0

        # Options
        self.options = OptionsScene(self.screen, self.window)

    def draw_menu(self):
        if self.main_menu:
            for idx, item in enumerate(self.menu_items):
                color = GREEN if idx == self.selected_option else WHITE
                text = FONT_8.render(item, True, color)
                rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50 + idx * 10))
                self.screen.blit(text, rect)

        if self.options_menu:
            self.options.draw()

    def handle_input(self, event):
        if self.main_menu:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    self.perform_action()

        elif self.options_menu:
            self.options.handle_input(event)
            if self.options.finished:
                self.options_menu = False
                self.main_menu = True

    def perform_action(self):
        selected_item = self.menu_items[self.selected_option]
        if selected_item == 'START':
            self.start_game = True
            self.main_menu = False
            self.options_menu = False
            self.scores_screen = False
            self.credits_screen = False

        elif selected_item == 'OPTIONS':
            self.options_menu = True
            self.main_menu = False
            self.scores_screen = False
            self.credits_screen = False

        elif selected_item == 'SCORES':
            self.scores_screen = True
        elif selected_item == 'CREDITS':
            self.credits_screen = True

    def reset(self):
        self.start_game = False
        self.main_menu = True

    def update(self):
        self.draw_menu()


class OptionsScene:
    def __init__(self, screen, window):

        # General setup
        self.screen = screen
        self.window = window

        # Options menu
        self.menu_items = ['RESOLUTION', 'SOUND', 'ACCEPT']
        self.current_option = 0

        self.selecting_resolution = True
        self.selecting_sound = False
        self.selecting_accept = False
        self.finished = False

        # Options submenus
        self.resolution_items = ['320x180', '640x320', '960x540', '1280x720']
        self.scale = 3
        self.current_chosen_scale = self.resolution_items[self.scale-1]

        self.sound_volume = 100
        self.sound_slider_rect = pygame.Rect(WIDTH // 2-50, HEIGHT // 2 + 10, 100, 10)

    def draw(self):
        # display options menu
        for idx, item in enumerate(self.menu_items):
            color = GREEN if idx == self.current_option else WHITE
            text = FONT_8.render(item, True, color)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70 + idx * 70))
            self.screen.blit(text, rect)

        # display resolution
        text = FONT_8.render(self.current_chosen_scale, True, WHITE)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2-50))
        self.screen.blit(text, rect)

        # display sound slider
        pygame.draw.rect(self.screen, WHITE, self.sound_slider_rect)
        full_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 10, 100, 10)
        pygame.draw.rect(self.screen, GREEN, full_rect, 1)

    def handle_scaling_options(self):
        self.scale = min(max(self.scale, 1), 4)
        self.current_chosen_scale = self.resolution_items[self.scale-1]
        self.window.size = (WIDTH * self.scale, HEIGHT * self.scale)

    def handle_sound_options(self):
        self.sound_volume = min(max(self.sound_volume, 0), 100)
        self.sound_slider_rect = pygame.Rect(WIDTH // 2-50, HEIGHT // 2 + 10, self.sound_volume-1, 10)

    def handle_input(self, event):
        self.finished = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                if self.selecting_resolution:
                    self.scale -= 1
                    self.handle_scaling_options()
                if self.selecting_sound:
                    self.sound_volume -= 1
                    self.handle_sound_options()

            elif event.key == pygame.K_RIGHT:
                if self.selecting_resolution:
                    self.scale += 1
                    self.handle_scaling_options()
                if self.selecting_sound:
                    self.sound_volume += 1
                    self.handle_sound_options()

            elif event.key == pygame.K_UP:
                self.current_option = (self.current_option - 1) % len(self.menu_items)

            elif event.key == pygame.K_DOWN:
                self.current_option = (self.current_option + 1) % len(self.menu_items)

            elif event.key == pygame.K_RETURN:
                if self.selecting_accept:
                    self.finished = True

        self.perform_action()
        print(self.sound_volume)

    def perform_action(self):
        selected_item = self.menu_items[self.current_option]
        if selected_item == 'RESOLUTION':
            pygame.key.set_repeat()
            self.selecting_resolution = True
            self.selecting_sound = False
            self.selecting_accept = False

        elif selected_item == 'SOUND':
            self.selecting_resolution = False
            self.selecting_sound = True
            self.selecting_accept = False

        elif selected_item == 'ACCEPT':
            self.selecting_resolution = False
            self.selecting_sound = False
            self.selecting_accept = True


class GameOverScene:
    def __init__(self, screen):
        self.screen = screen

    def show(self):

        game_over_text = FONT_8.render("GAME OVER", True, WHITE)
        restart_text = FONT_8.render("Press 'R' TO RESTART", True, WHITE)

        game_over_rect = game_over_text.get_rect()
        restart_rect = restart_text.get_rect()

        game_over_rect.center = (WIDTH // 2, HEIGHT // 2)
        restart_rect.center = (WIDTH // 2, HEIGHT // 2 + 10)

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)
