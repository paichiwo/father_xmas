import pygame
import pygame._sdl2 as pg_sdl2
import sys

from src.config import *
from pygame.locals import *
from src.camera import CameraGroup
from src.level import Level
from src.player import Player
from src.dashboard import Dashboard


class Game:
    def __init__(self):

        # Game setup
        pygame.init()
        pygame.display.set_caption('Father Xmas')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=HIDDEN | SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Scaled window setup
        self.window = pg_sdl2.Window.from_display_module()
        self.window.size = (WIDTH * SCALE, HEIGHT * SCALE)
        self.window.position = pg_sdl2.WINDOWPOS_CENTERED
        self.window.show()

        # Sprite groups
        self.player_group = pygame.sprite.GroupSingle()

        # Camera group
        self.camera_group = CameraGroup()

        # Game objects
        self.level = Level(self.screen)
        self.player = Player(100, 150, self.screen, self.level.ladders_group,
                             self.level.platforms_group, self.player_group)
        self.dashboard = Dashboard(self.screen)

        self.add_to_camera_group()

    def add_to_camera_group(self):
        self.camera_group.add(
            self.level.platforms_group,
            self.level.ladders_group,
            self.player_group
        )

    def draw_elements(self):
        self.camera_group.custom_draw(self.player)

    def update_elements(self):
        self.dashboard.update()
        self.camera_group.update()

    def run(self):
        while True:
            print(self.dashboard.game_over)

            self.screen.fill('grey15')
            can_climb, climbed_down, middle_of_ladder = self.player.check_climb()

            pygame.key.set_repeat(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.player.controls(event, can_climb, climbed_down, middle_of_ladder)

            self.draw_elements()
            self.update_elements()

            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    Game().run()
