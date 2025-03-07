import sys
import pygame._sdl2 as sdl2
from src.config import *
from src.level_pytmx import Platformer

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
        }

        # Game variables
        self.running = True

        # Game objects
        self.platformer = Platformer(self.screen)

    def handle_game_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            pygame.quit()
            sys.exit()

    def run(self):
        event = None
        while True:
            self.screen.fill('black')
            self.renderer.clear()
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                self.handle_game_events(event)


            if self.running:
                self.platformer.update(dt)

            sdl2.Texture.from_surface(self.renderer, self.screen).draw()
            self.renderer.present()
