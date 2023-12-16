import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # general setup
        self.image = pygame.Surface((1280, 32))
        self.image.fill('white')
        self.rect = self.image.get_rect(midbottom=pos)
        print(self.rect.midtop[1])