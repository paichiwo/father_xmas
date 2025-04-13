from src.config import *
from src.helpers import import_gifts
from src.sprites import Sprite, AnimatedSprite, Snowflake, Sleigh
from src.player import Player
from src.enemy import EnemyElf
from src.timer import Timer
from pytmx import load_pygame


class LevelTwo:
    def __init__(self, screen):
        self.screen = screen
        self.level_won = False
        self.all_sprites = pygame.sprite.Group()
        self.create_level(load_pygame('data/levels/level_2.tmx'))

        # Image browser setup
        path = 'assets/level/level_2_gifts/'
        self.gifts = import_gifts(path)
        self.gift_keys = list(self.gifts.keys())

        self.image_index = 0
        self.selected_gifts = []

        self.image_switch_timer = Timer(80)
        self.image_switch_timer.activate()

    def create_level(self, tmx_map):
        """Creates the current room by adding objects to sprite groups."""
        for x, y, surf in tmx_map.get_layer_by_name('letter').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites])

        for x, y, gid in tmx_map.get_layer_by_name('animations'):
            props = tmx_map.get_tile_properties_by_gid(gid)
            if props and 'frames' in props:
                frames = [tmx_map.get_tile_image_by_gid(frame.gid) for frame in props['frames']]
                AnimatedSprite((x * TILE_SIZE, y * TILE_SIZE), frames, [self.all_sprites])

    def input(self):
        keys = pygame.key.get_pressed()
        self.image_switch_timer.update()

        if not self.image_switch_timer.active:
            if keys[pygame.K_LEFT]:
                self.image_index = (self.image_index - 1) % len(self.gift_keys)
            elif keys[pygame.K_RIGHT]:
                self.image_index = (self.image_index + 1) % len(self.gift_keys)
            elif keys[pygame.K_RETURN]:
                selected_key = self.gift_keys[self.image_index]
                self.selected_gifts.append(selected_key)
                print(self.selected_gifts)
                del self.gifts[selected_key]
                self.gift_keys.pop(self.image_index)


            self.image_switch_timer.activate()

    def display_image(self):
        key = self.gift_keys[self.image_index]
        original_image = self.gifts[key]
        scaled_image = pygame.transform.scale(original_image,
                                              (original_image.get_width() * 2, original_image.get_height() * 2))
        rect = scaled_image.get_rect(topleft=(WIDTH / 3 - 35, HEIGHT / 2 - 20))
        self.screen.blit(scaled_image, rect)

    def update(self, dt):
        self.input()
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.screen)
        self.display_image()