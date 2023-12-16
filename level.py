import pygame

from ladder import Ladder
from plaform import Platform
from player import Player


class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = pygame.sprite.Group()

        self.platform = Platform((640, 500), self.all_sprites)
        self.ladder = Ladder((800, 500-16), self.all_sprites)
        self.player = Player((640, 360), self.platform.rect.midtop[1], self.all_sprites)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
