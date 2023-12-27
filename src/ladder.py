import pygame


class Ladder(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # general setup
        self.image = pygame.image.load('assets/ladder.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
