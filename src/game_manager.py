import sys
import pygame._sdl2 as sdl2
from src.config import *
from src.debug import DebugMenu
from src.level import Platformer, XmasLetter
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
            'game_over_scene_running': False,
            'debug_visible': False
        }

        # Game variables
        self.running = True

        # Game objects
        self.main_menu_scene = MainMenuScene(self.screen, self.window)
        self.dashboard = Dashboard(self.screen)
        self.platformer = Platformer(self.screen)
        self.xmas_letter = XmasLetter(self.screen)
        self.game_over_scene = GameOverScene(self.screen)
        self.debug_menu = DebugMenu(self.screen, self.clock, self.platformer, self.states)

    def handle_game_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if self.running:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LALT:
                self.states['debug_visible'] = not self.states['debug_visible']
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

    def activate_game_state(self, new_state):
        for key in self.states.keys():
            if key.endswith('_running'):
                self.states[key] = False
        self.states[new_state] = True

        if new_state == 'platformer_running':
            self.dashboard.timer_start_time = pygame.time.get_ticks()

    def check_game_start(self):
        if self.main_menu_scene.start_game:
            self.activate_game_state('platformer_running')

    def update_platformer_elements(self, dt):
        self.platformer.update(dt)
        self.dashboard.update()

    def platformer_check_win(self):
        if self.platformer.sleigh_completed:
            self.activate_game_state('xmas_letter_running')

    def update_xmas_letter_elements(self):
        self.dashboard.update()
        self.xmas_letter.draw()
        self.xmas_letter.update()

    def game_over(self):
        return not self.dashboard.game_over

    def show_game_over_screen(self):
        if self.states['game_over_scene_running']:
            self.game_over_scene.draw()

    def reset_game(self):
        self.running = True
        self.platformer.reset()
        self.dashboard.reset()
        self.main_menu_scene.reset()
        self.activate_game_state('main_menu_running')

    def run(self):
        while True:
            self.screen.fill(BLACK)
            self.renderer.clear()

            for event in pygame.event.get():
                self.handle_game_events(event)
                if self.states['main_menu_running']:
                    self.main_menu_scene.input(event)

            dt = self.clock.tick() / 1000

            if self.running:
                if self.states['main_menu_running']:
                    self.main_menu_scene.update()
                    self.check_game_start()

                if self.states['platformer_running']:
                    self.update_platformer_elements(dt)
                    self.platformer_check_win()

                if self.states['xmas_letter_running']:
                    self.update_xmas_letter_elements()

                self.running = self.game_over()
            else:
                self.activate_game_state('game_over_scene_running')
                self.show_game_over_screen()

            if self.states['debug_visible']:
                self.debug_menu.update()

            sdl2.Texture.from_surface(self.renderer, self.screen).draw()
            self.renderer.present()
