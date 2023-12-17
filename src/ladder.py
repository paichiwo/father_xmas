import pygame


class Ladder(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # general setup
        self.image = pygame.Surface((64, 210))
        self.image.fill('blue')
        self.rect = self.image.get_rect(midbottom=pos)
