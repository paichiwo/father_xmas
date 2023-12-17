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

        # platforms
        self.platforms = {
            'platform_1': Platform(pos=(0, 500), group=self.all_sprites)
        }

        # ladders
        self.ladders = {
            'ladder_1': Ladder(pos=(800, 500), group=self.all_sprites)
        }

        # level objects
        self.platform = self.platforms['platform_1']
        self.ladder = self.ladders['ladder_1']
        self.player = Player(pos=(640, 360), platform_y_pos=500, group=self.all_sprites)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
