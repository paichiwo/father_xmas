import sys
import pygame
import pygame._sdl2 as sdl2
from src.config import *
from src.level import Platformer, XmasLetter
from src.player import Player
from src.dashboard import Dashboard
from src.scenes import MainMenuScene, GameOverScene


class Game:
    def __init__(self):

        # Game setup
        pygame.init()
        pygame.display.set_caption('Father Xmas')
        self.clock = pygame.time.Clock()

        # Scaled window setup
        self.window = pygame.Window(size=(WIDTH * SCALE, HEIGHT * SCALE), title="Father Xmas")
        self.window.resizable = True
        self.renderer = sdl2.Renderer(self.window, vsync=True)
        self.renderer.logical_size = (WIDTH, HEIGHT)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.window.get_surface()

        self.main_menu_running = True
        self.platformer_running = False
        self.xmas_letter_running = False
        self.gift_rain_running = False
        self.gift_delivery_running = False
        self.congratulations_running = False
        self.game_over_scene_active = False

        # Game variables
        self.running = True

        # Sprite groups
        self.player_group = pygame.sprite.GroupSingle()

        # Game objects
        self.main_menu_scene = MainMenuScene(self.screen, self.window)
        self.dashboard = Dashboard(self.screen)
        self.platformer = Platformer(self.screen)
        self.xmas_letter = XmasLetter(self.screen)
        self.game_over_scene = GameOverScene(self.screen)
        self.player = Player(100, 112, self.screen, self.platformer, self.player_group)

    def handle_game_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not self.running:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

    def check_game_start(self):
        self.platformer_running = self.main_menu_scene.start_game
        if self.platformer_running:
            self.main_menu_running = False

    def draw_platformer_elements(self):
        self.player_group.draw(self.screen)

    def update_platformer_elements(self):
        self.dashboard.update()
        self.player_group.update()
        self.platformer.update()

    def platformer_check_win(self):
        if self.player.sleigh_completed:
            self.platformer_running = False
            self.xmas_letter_running = True

    def draw_xmas_letter_elements(self):
        self.xmas_letter.draw()

    def update_xmas_letter_elements(self):
        self.dashboard.update()
        self.xmas_letter.update()

    def game_over(self):
        return not self.dashboard.game_over

    def show_game_over_screen(self):
        if self.game_over_scene_active:
            self.game_over_scene.show()

    def reset_game(self):
        self.running = True
        self.game_over_scene_active = False
        self.dashboard.reset()
        self.platformer.reset()
        self.player.reset()

        self.platformer_running = False
        self.xmas_letter_running = False
        self.gift_rain_running = False
        self.gift_delivery_running = False
        self.main_menu_running = True

    def run(self):
        while True:
            self.screen.fill(BLACK)
            self.renderer.clear()
            pygame.key.set_repeat(FPS * 4)

            can_climb, climbed_down, middle_of_ladder = self.player.check_climb()

            for event in pygame.event.get():
                self.handle_game_events(event)

                if self.main_menu_running:
                    self.main_menu_scene.handle_input(event)

                if self.platformer_running:
                    self.player.controls(event, can_climb, climbed_down, middle_of_ladder)

            if self.running:
                if self.main_menu_running:
                    self.main_menu_scene.update()
                    self.check_game_start()

                if self.platformer_running:
                    self.update_platformer_elements()
                    self.draw_platformer_elements()
                    self.platformer_check_win()

                if self.xmas_letter_running:
                    self.update_xmas_letter_elements()
                    self.draw_xmas_letter_elements()

                self.running = self.game_over()
            else:
                self.game_over_scene_active = True
                self.show_game_over_screen()

            self.clock.tick(FPS)
            sdl2.Texture.from_surface(self.renderer, self.screen).draw()
            self.renderer.present()


if __name__ == '__main__':
    Game().run()
