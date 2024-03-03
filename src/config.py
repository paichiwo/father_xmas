# GAME CONSTANTS
import pygame

FPS = 60
WIDTH = 320
HEIGHT = 180
TILE_SIZE = 16
SCALE = 3

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 250, 0)

# ASSETS
pygame.init()
FONT_8 = pygame.font.Font('assets/font/C64_Pro_Mono-STYLE.ttf', size=8)

ROOM_TRANSITIONS = {
    'room_0_0': {'right': ('room_0_1', 0),
                 'down': ('room_1_0', -5)},

    'room_0_1': {'left': ('room_0_0', 302),
                 'right': ('room_0_2', 0),
                 'down': ('room_1_1', -5)},
    'room_0_2': {'left': ('room_0_1', 302)},
    'room_1_0': {'right': ('room_1_1', 0),
                 'up': ('room_0_0', 100)},
    'room_1_1': {'left': ('room_1_0', 302),
                 'right': ('room_1_2', 0),
                 'up': ('room_0_1', 100)},
    'room_1_2': {'left': ('room_1_1', 302)}
}

ENEMY_SPAWN_POS = {
    'room_0_0': [(360, 112, -1, 'walk_left', True)],
    'room_0_1': [(-40, 112, 1, 'walk_right', True), (360, 112, -1, 'walk_left', True)],
    'room_0_2': [(-40, 112, 1, 'walk_right', True)],
    'room_1_0': [(20, 128, 1, 'walk_right', False), (20, 64, 1, 'walk_right', False), (360, 128, -1, 'walk_left', True),
                 (360, 64, -1, 'walk_left', True)],
    'room_1_1': [(-40, 128, 1, 'walk_right', True), (-40, 64, 1, 'walk_right', False),
                 (360, 128, -1, 'walk_left', False)],
    'room_1_2': [(-40, 128, 1, 'walk_right', True), (300, 128, -1, 'walk_left', False)],
}

PATHS = {
    'player': 'assets/player'
}
