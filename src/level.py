import pygame
from src.ladder import Ladder
from src.plaform import Platform


class Level:
    def __init__(self):

        # Platforms
        self.platforms = {
            'platform_1': Platform(pos=(0, 150)),
            'platform_2': Platform(pos=(0, 100)),
            'platform_3': Platform(pos=(0, 50))
        }

        # Ladders
        self.ladders = {
            'ladder_1': Ladder(pos=(50, 150)),
            'ladder_2': Ladder(pos=(150, 100))
        }


