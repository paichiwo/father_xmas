from src.config import *
from src.sprites import Sprite, AnimatedSprite
from src.player_pytmx import Player
from pytmx import load_pygame


class Platformer:
    def __init__(self, screen):
        self.screen = screen

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms_group = pygame.sprite.Group()
        self.ladders_group = pygame.sprite.Group()
        self.collision_walls = pygame.sprite.Group()

        # rooms setup
        self.rooms = ['room_0_0', 'room_0_1', 'room_0_2', 'room_1_0', 'room_1_1', 'room_1_2']
        self.tmx_rooms = {room: load_pygame(f'data/levels/{room}.tmx') for room in self.rooms}
        self.current_room_key = 'room_0_2'
        self.current_room = self.tmx_rooms[self.current_room_key]
        self.create_room(self.current_room)

        # player initialization
        self.player = Player((5 * TILE_SIZE, 7 * TILE_SIZE), PATHS['player'], [self.all_sprites])

    def create_room(self, tmx_map):
        """Creates the current room by adding objects to sprite groups."""
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
        for sprite in self.all_sprites.sprites():
            if sprite is not self.player:
                sprite.kill()

    def change_room(self, new_room_key):
        """Clears the old room and loads a new one"""
        if new_room_key in self.tmx_rooms and new_room_key != self.current_room_key:
            self.clear_room()
            self.current_room_key = new_room_key
            self.current_room = self.tmx_rooms[new_room_key]
            self.create_room(self.current_room)

    def update(self, dt):
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.screen)
        pygame.draw.rect(self.screen, 'white', self.player.rect, 1)
