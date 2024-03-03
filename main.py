import sys
import pygame._sdl2 as sdl2
from src.config import *
from src.level import Platformer, XmasLetter
from src.player import Player
from src.dashboard import Dashboard
from src.scenes import MainMenuScene, GameOverScene


class Game:
    def __init__(self):

        # Game setup
        self.clock = pygame.time.Clock()

        # Scaled window setup
        self.window = pygame.Window(size=(WIDTH * SCALE, HEIGHT * SCALE), title="Father Xmas")
        self.window.resizable = True
        self.renderer = sdl2.Renderer(self.window, vsync=True)
        self.renderer.logical_size = (WIDTH, HEIGHT)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.window.get_surface()

        self.states = {
            'main_menu_running': True,
            'platformer_running': False,
            'xmas_letter_running': False,
            'gift_rain_running': False,
            'gift_delivery_running': False,
            'congratulations_running': False,
            'game_over_scene_running': False
        }

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
        self.player = Player(
            pos=(100, 112),
            screen=self.screen,
            platformer=self.platformer,
            path=PATHS['player'],
            group=self.player_group)

    def handle_game_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not self.running:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

    def check_game_start(self):
        self.states['platformer_running'] = self.main_menu_scene.start_game
        if self.states['platformer_running']:
            self.states['main_menu_running'] = False
            self.dashboard.timer_start_time = pygame.time.get_ticks()

    def draw_platformer_elements(self):
        self.player_group.draw(self.screen)

    def update_platformer_elements(self, dt):
        self.dashboard.update()
        self.player_group.update(dt)
        self.platformer.update()

    def platformer_check_win(self):
        if self.platformer.sleigh_completed:
            self.states['platformer_running'] = False
            self.states['xmas_letter_running'] = True

    def draw_xmas_letter_elements(self):
        self.xmas_letter.draw()

    def update_xmas_letter_elements(self):
        self.dashboard.update()
        self.xmas_letter.update()

    def game_over(self):
        return not self.dashboard.game_over

    def show_game_over_screen(self):
        if self.states['game_over_scene_active']:
            self.game_over_scene.show()

    def reset_game(self):
        self.running = True
        self.states['game_over_scene_running'] = False
        self.platformer.reset()
        self.player.reset()
        self.dashboard.reset()
        self.main_menu_scene.reset()

        self.states['platformer_running'] = False
        self.states['xmas_letter_running'] = False
        self.states['gift_rain_running'] = False
        self.states['gift_delivery_running'] = False
        self.states['main_menu_running'] = True

    def run(self):
        while True:
            self.screen.fill(BLACK)
            self.renderer.clear()

            for event in pygame.event.get():
                self.handle_game_events(event)

                if self.states['main_menu_running']:
                    self.main_menu_scene.handle_input(event)

            dt = self.clock.tick() / 1000
            if self.running:
                if self.states['main_menu_running']:
                    self.main_menu_scene.update()
                    self.check_game_start()

                if self.states['platformer_running']:
                    self.update_platformer_elements(dt)
                    self.draw_platformer_elements()
                    self.platformer_check_win()

                if self.states['xmas_letter_running']:
                    pygame.key.set_repeat(FPS)
                    self.update_xmas_letter_elements()
                    self.draw_xmas_letter_elements()

                self.running = self.game_over()
            else:
                self.states['game_over_scene_running'] = True
                self.states['platformer_running'] = False
                self.show_game_over_screen()

            sdl2.Texture.from_surface(self.renderer, self.screen).draw()
            self.renderer.present()


if __name__ == '__main__':
    Game().run()
