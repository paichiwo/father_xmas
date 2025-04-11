from random import randint, choice
from src.config import *
from src.helpers import import_images
from src.sprites import Sprite, AnimatedSprite, Snowflake, Sleigh
from src.player import Player
from src.enemy import EnemyElf
from src.timer import Timer
from pytmx import load_pygame


class LevelTwo:
    def __init__(self, screen):
        self.screen = screen
        self.level_won = False

        # sprite groups
        self.all_sprites = pygame.sprite.Group()

        # snow
        self.snow_images = import_images(PATHS['snow'])

        self.create_room(load_pygame('data/levels/level_2.tmx'))

    def create_room(self, tmx_map):
        """Creates the current room by adding objects to sprite groups."""

        for x, y, surf in tmx_map.get_layer_by_name('letter').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites])

        for x, y, gid in tmx_map.get_layer_by_name('animations'):
            props = tmx_map.get_tile_properties_by_gid(gid)
            if props and 'frames' in props:
                frames = [tmx_map.get_tile_image_by_gid(frame.gid) for frame in props['frames']]
                AnimatedSprite((x * TILE_SIZE, y * TILE_SIZE), frames, [self.all_sprites])

    def update(self, dt):
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.screen)
        print(len(self.all_sprites))
