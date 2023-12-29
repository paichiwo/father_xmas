import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, length, height, screen, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.length = length
        self.height = height
        self.screen = screen

        # Image & Rect
        self.image = pygame.Surface((self.length, self.height))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
