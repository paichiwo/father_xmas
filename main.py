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

        self.timer = pygame.time.Clock()
        self.fps = 60

        # Sprite groups
        self.player_group = pygame.sprite.GroupSingle()

        # Game objects
        self.level = Level(self.screen)
        self.player = Player(100, 150, self.screen, self.level.ladders_group,
                             self.level.platforms_group, self.player_group)

        # Add sprites to the sprite groups


    def draw_sprites(self):
        self.level.platforms_group.draw(self.screen)
        self.level.ladders_group.draw(self.screen)
        self.player_group.draw(self.screen)

    def update_sprites(self):
        self.level.platforms_group.update()
        self.level.ladders_group.update()
        self.player_group.update()

    def run(self):
        while True:
            self.screen.fill('black')
            can_climb, climbed_down = self.player.check_climb()

            self.draw_sprites()
            self.update_sprites()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.player.controls(event, can_climb, climbed_down)

            pygame.display.update()
            self.timer.tick(self.fps)


if __name__ == '__main__':
    Game().run()
