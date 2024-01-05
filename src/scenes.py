import pygame
from src.config import WHITE, BLACK


class GameOverScene:
    def __init__(self, screen, screen_width, screen_height):

        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font('assets/font/C64_Pro_Mono-STYLE.ttf', size=8)

    def show(self):
        self.screen.fill(BLACK)

        game_over_text = self.font.render("GAME OVER", True, WHITE)
        restart_text = self.font.render("Press 'R' TO RESTART", True, WHITE)

        game_over_rect = game_over_text.get_rect()
        restart_rect = restart_text.get_rect()

        game_over_rect.center = (self.screen_width // 2, self.screen_height // 2)
        restart_rect.center = (self.screen_width // 2, self.screen_height // 2 + 10)

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)
