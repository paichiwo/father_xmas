import pygame


class Ladder(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, length, height, screen, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.length = length
        self.height = height
        self.screen = screen

        self.image = pygame.image.load('assets/ladder.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))

