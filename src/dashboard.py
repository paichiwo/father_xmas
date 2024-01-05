import pygame
from src.config import WHITE


class Dashboard:
    """Creates the whole dashboard with scores and timer"""
    def __init__(self, screen):

        # General setup
        self.screen = screen
        self.font = pygame.font.Font('assets/font/C64_Pro_Mono-STYLE.ttf', size=8)

        # Background
        self.bg_img = pygame.image.load('assets/dashboard/dashboard.png').convert_alpha()
        self.bg_img_rect = self.bg_img.get_rect(topleft=(0, 150))

        # Timer
        self.timer_img = pygame.image.load('assets/dashboard/timer.png').convert_alpha()
        self.timer_img_rect = self.timer_img.get_rect(topleft=(31, 153))

        # Timer animation variables
        self.timer_start_time = pygame.time.get_ticks()
        self.timer_duration = 15 * 60 * 10  # * 1000 = 15 mins

        # Score
        self.score = 0
        self.scores_y_pos = 157

        # Game Over
        self.game_over = False

    def draw_dashboard_bg(self):
        """Display the dashboard background"""

        self.screen.blit(self.bg_img, self.bg_img_rect)

    def draw_score(self):
        """Display current score"""

        score_text = self.font.render("SCORE", False, WHITE)
        score_value = self.font.render("{:07}".format(self.score), False, WHITE)
        score_text_rect = score_text.get_rect()
        score_value_rect = score_value.get_rect()

        score_text_rect.topleft = (201, self.scores_y_pos)
        score_value_rect.topleft = (243, self.scores_y_pos)
        self.screen.blit(score_text, score_text_rect)
        self.screen.blit(score_value, score_value_rect)

    def draw_timer(self):
        """Move timer_img to the left accordingly to the time set in the self.timer_duration"""

        if not self.game_over:
            elapsed_time = pygame.time.get_ticks() - self.timer_start_time
            displacement = (elapsed_time / self.timer_duration) * (96 - 24)
            self.timer_img_rect.topleft = (31 - displacement, 153)
            self.screen.blit(self.timer_img, self.timer_img_rect)

            # Set game_over to True if time is over
            if elapsed_time / self.timer_duration >= 1:
                self.game_over = True
        else:
            self.timer_img_rect.topright = (55, 153)
            self.screen.blit(self.timer_img, self.timer_img_rect)

    def reset(self):
        self.game_over = False
        self.timer_start_time = pygame.time.get_ticks()
        self.timer_img_rect.topleft = (31, 153)

    def update(self):
        self.draw_timer()
        self.draw_dashboard_bg()
        self.draw_score()
        print(self.game_over)
