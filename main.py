import pygame
import pygame._sdl2 as pg_sdl2
import sys

from src.config import *
from pygame.locals import *
from src.level import Level
from src.player import Player


class Game:
    def __init__(self):

        # Game setup
        pygame.init()
        pygame.display.set_caption('Father Xmas')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=HIDDEN | SCALED, vsync=1)
        self.clock = pygame.time.Clock()

        # Scaled window setup
        self.window = pg_sdl2.Window.from_display_module()
        self.window.size = (WIDTH * SCALE, HEIGHT * SCALE)
        self.window.position = pg_sdl2.WINDOWPOS_CENTERED
        self.window.show()

        # Sprite groups
        self.platform_group = pygame.sprite.Group()
        self.ladder_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

        # Game objects
        self.level = Level()
        self.player = Player(100, 50, self.platform_group, self.ladder_group)

        # Add sprites to the sprite groups

        self.platform_group.add(self.level.platforms.values())
        self.ladder_group.add(self.level.ladders.values())
        self.player_group.add(self.player)

    def draw_sprites(self):
        self.platform_group.draw(self.screen)
        self.ladder_group.draw(self.screen)
        self.player_group.draw(self.screen)

    def update_sprites(self, dt):
        self.platform_group.update()
        self.ladder_group.update()
        self.player_group.update(dt)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.player.controls(event)

            dt = self.clock.tick() / 1000

            self.screen.fill('black')
            self.draw_sprites()
            self.update_sprites(dt)

            pygame.display.update()


if __name__ == '__main__':
    Game().run()
