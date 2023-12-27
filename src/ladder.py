import pygame


class Ladder(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # general setup
        self.image = pygame.Surface((16, 48))
        self.image.fill('blue')
        self.rect = self.image.get_rect(midbottom=pos)
