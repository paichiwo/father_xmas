# GAME CONSTANTS
import pygame

FPS = 60
WIDTH = 320
HEIGHT = 180
TILE_SIZE = 16
SCALE = 3

# COLORS
BLACK  = (0, 0 ,0)
WHITE = 'grey80'
YELLOW = 'yellow'
ORANGE = 'orange'
GREEN = (19, 211, 24)
DK_GREEN = (29, 53, 29)
RED = (139, 24, 29)
DK_RED = (111, 15, 17)
TAN = (230, 190, 154)


PATHS = {
    'player': 'assets/player',
    'elf': 'assets/enemy/elf',
    'snow': 'assets/level/snow',
    'sleigh': 'assets/level/sleigh'
}

# ASSETS
pygame.init()
FONT_8 = pygame.font.Font('assets/font/C64_Pro_Mono-STYLE.ttf', size=8)
FONT_DEBUG = pygame.font.Font('assets/font/debug_font.ttf', size=10)

# start room: {enemy facing, dest room, trigger pos}
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
# pos_x, pos_y, direction_x
ENEMY_SPAWN_POS = {
    'room_0_0': [(360, 112, -1)],
    'room_0_1': [(-40, 112, 1), (360, 112, -1)],
    'room_0_2': [(-40, 112, 1)],
    'room_1_0': [(30, 128, 1), (30, 64, 1), (360, 128, -1),
                 (360, 64, -1)],
    'room_1_1': [(-40, 128, 1), (-40, 64, 1),
                 (360, 128, -1)],
    'room_1_2': [(-40, 128, 1), (290, 128, -1)],
}
# snow
SNOW_AMOUNT = 20
SNOW_BOUNDARIES = {
    'room_0_0': [pygame.Rect(0, 0, 320, 32)],
    'room_0_1': [pygame.Rect(0, 0, 320, 32)],
    'room_0_2': [pygame.Rect(0, 0, 230, 32), pygame.Rect(230, 0, 100, 144)],
    'room_1_2': [pygame.Rect(0, 0, 320, 144)]
}