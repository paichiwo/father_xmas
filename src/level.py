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
        self.platform_group = pygame.sprite.Group()
        self.platforms = {
            'platform_1': Platform(pos=(0, 500), group=self.platform_group),
            'platform_2': Platform(pos=(0, 300), group=self.platform_group),
            'platform_3': Platform(pos=(0, 100), group=self.platform_group)

        }
        self.all_sprites.add(self.platform_group)

        # ladders
        self.ladder_group = pygame.sprite.Group()
        self.ladders = {
            'ladder_1': Ladder(pos=(800, 500), group=self.ladder_group),
            'ladder_2': Ladder(pos=(300, 300), group=self.ladder_group)
        }
        self.all_sprites.add(self.ladder_group)

        # level objects
        self.platform = self.platforms['platform_1']
        self.ladder = self.ladders['ladder_1']
        self.player = Player(pos=(640, 360),
                             group=self.all_sprites,
                             platform_group=self.platform_group,
                             ladder_group=self.ladder_group)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
