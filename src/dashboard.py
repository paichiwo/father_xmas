import pygame
from src.config import *


class Dashboard:
    def __init__(self, screen):

        self.screen = screen
        self.font = pygame.font.Font('assets/font/C64_Pro_Mono-STYLE.ttf', size=8)

        # Background
        self.bg_rect = pygame.Rect((0, 150, 320, 30))

        # Score
        self.score = 0
        self.scores_y_pos = 160

    def draw_dashboard_bg(self):
        pygame.draw.rect(self.screen, BLACK, self.bg_rect)

    def draw_score(self):
        score_text = self.font.render("SCORE", False, WHITE)
        score_value = self.font.render("{:07}".format(self.score), False, WHITE)
        score_text_rect = score_text.get_rect()
        score_value_rect = score_value.get_rect()

        score_text_rect.topleft = (160, self.scores_y_pos)
        score_value_rect.topleft = (210, self.scores_y_pos)
        self.screen.blit(score_text, score_text_rect)
        self.screen.blit(score_value, score_value_rect)

    def update(self):
        self.draw_dashboard_bg()
        self.draw_score()
