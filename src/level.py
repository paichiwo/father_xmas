from random import randint, choice
from src.config import *
from src.helpers import import_images
from src.sprites import Sprite, AnimatedSprite, Snowflake, Sleigh
from src.player import Player
from src.enemy import EnemyElf
from pytmx import load_pygame


class Platformer:
    def __init__(self, screen):

        self.screen = screen
        self.level_won = False

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.enemy_group = pygame.sprite.Group()
        self.platforms_group = pygame.sprite.Group()
        self.ladders_group = pygame.sprite.Group()
        self.collision_walls = pygame.sprite.Group()
        self.sleigh_group = pygame.sprite.Group()
        self.completed_sleigh_group = pygame.sprite.Group()

        # snow
        self.snow_images = import_images(PATHS['snow'])

        # rooms setup
        self.rooms = ['room_0_0', 'room_0_1', 'room_0_2', 'room_1_0', 'room_1_1', 'room_1_2']
        self.tmx_rooms = {room: load_pygame(f'data/levels/{room}.tmx') for room in self.rooms}
        self.current_room_key = 'room_0_2'
        self.current_room = self.tmx_rooms[self.current_room_key]
        self.create_room(self.current_room)

        # sleigh
        self.sleigh_images = import_images(PATHS['sleigh'])
        self.sleigh_in_inventory = False
        self.all_sleigh_completed = False
        self.completed_sleigh_pieces = []
        self.sleigh_spawn_room = choice(self.rooms[:5])
        self.create_sleigh()

        # player initialization
        self.player = Player((5 * TILE_SIZE, 7 * TILE_SIZE), self.screen, self, PATHS['player'], [self.player_group])

        # enemy
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = randint(2000, 5000)
        self.create_enemies()

    def create_room(self, tmx_map):
        """Creates the current room by adding objects to sprite groups."""
        self.create_snow()

        layer_groups = {
            'platforms': self.platforms_group,
            'ladders': self.ladders_group,
            'walls_with_collisions': self.collision_walls
        }
        for layer in ['platforms', 'ladders', 'walls_with_collisions', 'decorations']:
            group = layer_groups.get(layer, self.all_sprites)
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, group])

        for x, y, gid in tmx_map.get_layer_by_name('animations'):
            props = tmx_map.get_tile_properties_by_gid(gid)
            if props and 'frames' in props:
                frames = [tmx_map.get_tile_image_by_gid(frame.gid) for frame in props['frames']]
                AnimatedSprite((x * TILE_SIZE, y * TILE_SIZE), frames, [self.all_sprites])

    def clear_room(self):
        """Clears all non-player sprites from groups to prepare for a new room."""
        self.all_sprites.empty()
        self.platforms_group.empty()
        self.ladders_group.empty()
        self.collision_walls.empty()
        self.enemy_group.empty()

    def change_room(self, new_room_key):
        """Clears the old room and loads a new one"""
        if new_room_key in self.tmx_rooms and new_room_key != self.current_room_key:
            self.clear_room()
            self.current_room_key = new_room_key
            self.current_room = self.tmx_rooms[new_room_key]
            self.create_room(self.current_room)
            self.create_enemies()

    def create_snow(self):
        """Creates snowflakes based on the current room's snow boundaries."""
        if self.current_room_key in SNOW_BOUNDARIES:
            for _ in range(SNOW_AMOUNT):
                for boundary in SNOW_BOUNDARIES[self.current_room_key]:
                    pos = (randint(boundary.left, boundary.right), randint(boundary.top, boundary.bottom))
                    Snowflake(pos, choice(self.snow_images), boundary, [self.all_sprites])

    def create_sleigh(self):
        rects = []
        if not self.sleigh_in_inventory and self.sleigh_spawn_room in self.tmx_rooms:
            tmx_map = self.tmx_rooms[self.sleigh_spawn_room]
            for x, y, surf in tmx_map.get_layer_by_name('platforms').tiles():
                if 1 < x < 19:
                    rects.append((x * TILE_SIZE, y * TILE_SIZE))
            pos = choice(rects)
            index = len(self.completed_sleigh_pieces)
            if index < len(self.sleigh_images):
                Sleigh(pos, self.screen, self.sleigh_images[index], [self.sleigh_group])

    def create_enemies(self):
        self.enemy_spawn_timer += pygame.time.get_ticks()
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            enemy_spawn_data = choice(ENEMY_SPAWN_POS[self.current_room_key])
            EnemyElf(screen=self.screen,
                     platformer=self,
                     path=PATHS['elf'],
                     pos=(enemy_spawn_data[0], enemy_spawn_data[1]),
                     direction_x=enemy_spawn_data[2],
                     group=self.enemy_group)
            self.enemy_spawn_timer = 0
            self.enemy_spawn_delay = randint(2000, 5000)

    def reset(self):
        self.player.reset()
        self.current_room_key = 'room_0_2'
        self.change_room(self.current_room_key)
        self.completed_sleigh_pieces = []
        self.sleigh_in_inventory = False
        self.all_sleigh_completed = False

    def update(self, dt):
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.screen)

        self.sleigh_group.update() if self.current_room_key is self.sleigh_spawn_room else self.sleigh_group.remove()
        if self.current_room_key == 'room_1_2':
            self.completed_sleigh_group.update()

        self.player_group.update(dt)
        self.player_group.draw(self.screen)

        self.enemy_group.update(dt)
        self.enemy_group.draw(self.screen)


class XmasLetter:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.Surface((20, 20))
        pygame.draw.circle(self.image, 'blue', (self.image.get_width() // 2, self.image.get_height() // 2), 10)
        self.rect = self.image.get_rect()
        self.rect.topleft = (30, 30)

    def draw(self):
        self.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.screen, 'red', self.rect, 1)

    def update(self):
        self.rect.x += 1
