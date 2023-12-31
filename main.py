import sys
import pygame
import pygame._sdl2 as pg_sdl2

from pygame.locals import HIDDEN, SCALED
from src.config import WIDTH, HEIGHT, SCALE
from src.camera import CameraGroup
from src.level import Level
from src.player import Player
from src.dashboard import Dashboard
from src.scenes import GameOverScene


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

        # Game variables
        self.running = True
        self.game_over_scene_active = False

        # Sprite groups
        self.player_group = pygame.sprite.GroupSingle()

        # Camera group
        self.camera_group = CameraGroup()

        # Game objects
        self.level = Level(self.screen)
        self.player = Player(100, 150, self.screen, self.level.ladders_group,
                             self.level.platforms_group, self.player_group)
        self.dashboard = Dashboard(self.screen)
        self.game_over_scene = GameOverScene(self.screen, WIDTH, HEIGHT)

        self.add_to_camera_group()

    def add_to_camera_group(self):
        self.camera_group.add(
            self.level.platforms_group,
            self.level.ladders_group,
            self.player_group
        )

    def handle_game_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not self.running:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

    def draw_elements(self):
        self.camera_group.custom_draw(self.player)

    def update_elements(self):
        self.dashboard.update()
        self.camera_group.update()

    def game_over(self):
        return not self.dashboard.game_over

    def show_game_over_screen(self):
        if self.game_over_scene_active:
            self.game_over_scene.show()

    def reset_game(self):
        self.running = True
        self.game_over_scene_active = False
        self.dashboard.reset()
        self.player.reset()

    def test_map(self):
        img = pygame.image.load('assets/map.png').convert_alpha()
        img_rect = img.get_rect(topright=(320, 0))
        self.screen.blit(img, img_rect)

    def run(self):
        while True:
            self.screen.fill('grey15')
            pygame.key.set_repeat(self.fps)
            can_climb, climbed_down, middle_of_ladder = self.player.check_climb()

            for event in pygame.event.get():
                self.handle_game_events(event)
                self.player.controls(event, can_climb, climbed_down, middle_of_ladder)

            if self.running:
                self.test_map()
                self.draw_elements()
                self.update_elements()
                self.running = self.game_over()
            else:
                self.game_over_scene_active = True
                self.show_game_over_screen()

            pygame.display.update()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    Game().run()
