import pygame
from src.config import WHITE, BLACK, WIDTH, HEIGHT


class MainMenuScene:
    def __init__(self, screen, window):

        self.screen = screen
        self.window = window

        self.font = pygame.font.Font('assets/font/C64_Pro_Mono-STYLE.ttf', size=8)

    def show(self):
        title_text = self.font.render("Official Father Christmas remake", True, WHITE)
        start_game_text = self.font.render("Press 'S' to start", True, WHITE)

        title_text_rect = title_text.get_rect()
        start_game_text_rect = start_game_text.get_rect()

        title_text_rect.center = (WIDTH // 2, HEIGHT // 2)
        start_game_text_rect.center = (WIDTH // 2, HEIGHT // 2 + 10)

        self.screen.blit(title_text, title_text_rect)
        self.screen.blit(start_game_text, start_game_text_rect)

    def change_res(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            scale = 2
            self.window.size = (WIDTH * scale, HEIGHT * scale)
        elif keys[pygame.K_d]:
            scale = 4
            self.window.size = (WIDTH * scale, HEIGHT * scale)
        elif keys[pygame.K_g]:
            scale = 3
            self.window.size = (WIDTH * scale, HEIGHT * scale)

class GameOverScene:
    def __init__(self, screen):

        self.screen = screen
        self.font = pygame.font.Font('assets/font/C64_Pro_Mono-STYLE.ttf', size=8)

    def show(self):
        self.screen.fill(BLACK)

        game_over_text = self.font.render("GAME OVER", True, WHITE)
        restart_text = self.font.render("Press 'R' TO RESTART", True, WHITE)

        game_over_rect = game_over_text.get_rect()
        restart_rect = restart_text.get_rect()

        game_over_rect.center = (WIDTH // 2, HEIGHT // 2)
        restart_rect.center = (WIDTH // 2, HEIGHT // 2 + 10)

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)
