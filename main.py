import sys
import pygame
from pygame.locals import SCALED, RESIZABLE, WINDOWPOS_CENTERED
from src.config import FPS, WIDTH, HEIGHT, SCALE
from src.level import Level
from src.player import Player
from src.dashboard import Dashboard
from src.scenes import GameOverScene


class Game:
    def __init__(self):

        # Game setup
        pygame.init()
        pygame.display.set_caption('Father Xmas')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), SCALED | RESIZABLE, vsync=1)
        self.clock = pygame.time.Clock()

        self.window = pygame.Window.from_display_module()
        self.window.size = (WIDTH * SCALE, HEIGHT * SCALE)
        self.window.position = WINDOWPOS_CENTERED
        self.window.show()

        # Game variables
        self.running = True
        self.game_over_scene_active = False

        # Sprite groups
        self.player_group = pygame.sprite.GroupSingle()

        # Game objects
        self.level = Level(self.screen)
        self.player = Player(100, 112, self.screen, self.level.ladders_group,
                             self.level.platforms_group, self.player_group)
        self.dashboard = Dashboard(self.screen)
        self.game_over_scene = GameOverScene(self.screen, WIDTH, HEIGHT)

    def handle_game_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not self.running:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

    def draw_elements(self):
        self.level.platforms_group.draw(self.screen)
        self.level.ladders_group.draw(self.screen)
        self.level.walls_group.draw(self.screen)
        self.level.walls_with_collision_group.draw(self.screen)
        self.level.decorations_group.draw(self.screen)

        self.player_group.draw(self.screen)

    def update_elements(self):
        self.dashboard.update()

        self.level.platforms_group.update()
        self.level.ladders_group.update()
        self.level.walls_group.update()
        self.level.walls_with_collision_group.update()
        self.level.decorations_group.update()

        self.player_group.update()

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

    def change_res(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f]:
            SCALE = 2
            self.window.size = (WIDTH * SCALE, HEIGHT * SCALE)
        elif keys[pygame.K_d]:
            SCALE = 4
            self.window.size = (WIDTH * SCALE, HEIGHT * SCALE)

    def run(self):
        while True:
            self.screen.fill('grey15')
            pygame.key.set_repeat(FPS)
            can_climb, climbed_down, middle_of_ladder = self.player.check_climb()

            for event in pygame.event.get():
                self.handle_game_events(event)
                self.player.controls(event, can_climb, climbed_down, middle_of_ladder)

            if self.running:
                self.update_elements()
                self.draw_elements()
                self.change_res()

                self.running = self.game_over()
            else:
                self.game_over_scene_active = True
                self.show_game_over_screen()

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    Game().run()
