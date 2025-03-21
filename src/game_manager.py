import sys
import pygame._sdl2 as sdl2
from src.config import *
from src.debug import DebugMenu
from src.level_1 import LevelOne
from src.level_2 import LevelTwo
from src.dashboard import Dashboard
from src.menu_scenes import MainMenuScene, GameOverScene
from src.helpers import activate_state

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
            'level_1_running': False,
            'level_2_running': False,
            'level_3_running': False,
            'level_4_running': False,
            'congratulations_running': False,
            'game_over_scene_running': False
        }


        # Game variables
        self.running = True
        self.debug_visible = False

        # Game objects
        self.main_menu_scene = MainMenuScene(self.screen, self.window)
        self.dashboard = Dashboard(self.screen)
        self.level_1 = LevelOne(self.screen)
        self.level_2 = LevelTwo(self.screen)
        self.game_over_scene = GameOverScene(self.screen)
        self.debug_menu = DebugMenu(self.screen, self.clock, self.level_1, self.states)

    def handle_game_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            pygame.quit()
            sys.exit()
        if self.running:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LALT:
                self.debug_visible = not self.debug_visible
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset_game()

    def check_game_start(self):
        if self.main_menu_scene.states['START']:
            activate_state(self.states, 'level_1_running')
            self.dashboard.timer_start_time = pygame.time.get_ticks()

    def update_level_1_elements(self, dt):
        self.level_1.update(dt)
        self.dashboard.update()

    def platformer_check_win(self):
        if self.level_1.all_sleigh_completed:
            activate_state(self.states, 'level_2_running')

    def update_xmas_letter_elements(self):
        self.dashboard.update()
        self.level_2.update()
        self.level_2.draw()

    def game_over(self):
        return not self.dashboard.game_over

    def show_game_over_screen(self):
        if self.states['game_over_scene_running']:
            self.game_over_scene.draw()

    def reset_game(self):
        self.running = True
        self.level_1.reset()
        self.dashboard.reset()
        self.main_menu_scene.reset()
        activate_state(self.states, 'main_menu_running')

    def run(self):
        event = None
        while True:
            self.screen.fill(BLACK)
            self.renderer.clear()
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                self.handle_game_events(event)

            if self.running:
                if self.states['main_menu_running']:
                    self.main_menu_scene.update(event)
                    self.check_game_start()
                if self.states['level_1_running']:
                    self.update_level_1_elements(dt)
                    self.platformer_check_win()
                if self.states['level_2_running']:
                    self.update_xmas_letter_elements()

                self.running = self.game_over()

            else:
                activate_state(self.states, 'game_over_scene_running')
                self.show_game_over_screen()

            if self.debug_visible:
                self.debug_menu.update(event)

            sdl2.Texture.from_surface(self.renderer, self.screen).draw()
            self.renderer.present()
