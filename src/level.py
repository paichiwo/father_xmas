import pygame
from src.ladder import Ladder
from src.plaform import Platform


class Level:
    def __init__(self, screen):

        # General setup
        self.screen = screen

        # Platforms
        self.platforms_group = pygame.sprite.Group()
        self.platforms = {
            'platform_1': Platform(0, 150, 500, 5, self.screen, self.platforms_group),
            'platform_2': Platform(0, 100, 500, 5, self.screen, self.platforms_group),
            'platform_3': Platform(0, 50, 500, 5, self.screen, self.platforms_group)
        }

        # Ladders
        self.ladders_group = pygame.sprite.Group()
        self.ladders = {
            'ladder_1': Ladder(50, 150, 16, 50, self.screen, self.ladders_group),
            'ladder_2': Ladder(150, 100, 16, 50, self.screen, self.ladders_group)
        }
