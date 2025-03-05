from src.config import *
from src.sprites import Sprite, AnimatedSprite
from src.player_pytmx import Player
from pytmx import load_pygame


class Platformer:
    def __init__(self, screen):
        self.screen = screen

        # rooms data
        self.tmx_rooms = {
            'room_0_0': load_pygame('data/levels/room_0_0.tmx'),
            'room_0_1': load_pygame('data/levels/room_0_1.tmx'),
            'room_0_2': load_pygame('data/levels/room_0_2.tmx'),
            'room_1_0': load_pygame('data/levels/room_1_0.tmx'),
            'room_1_1': load_pygame('data/levels/room_1_1.tmx'),
            'room_1_2': load_pygame('data/levels/room_1_2.tmx')
        }
        self.current_room = self.tmx_rooms['room_1_0']

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms_group = pygame.sprite.Group()
        self.ladders_group = pygame.sprite.Group()
        self.collision_walls = pygame.sprite.Group()

        # placeholder for player initialization
        self.player = None

        # setup environment objects
        self.setup(self.current_room)

    def setup(self, tmx_map):
        layer_groups = {
            'platforms': self.platforms_group,
            'ladders': self.ladders_group,
            'walls_with_collisions': self.collision_walls
}
        for layer in ['platforms', 'ladders', 'walls_with_collisions', 'decorations']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                if layer == 'decorations':
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites])
                else:
                    Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, layer_groups[layer]])

        for x, y, gid in tmx_map.get_layer_by_name('animations'):
            props = tmx_map.get_tile_properties_by_gid(gid)
            if props and 'frames' in props:
                frames = [tmx_map.get_tile_image_by_gid(frame.gid) for frame in props['frames']]
                AnimatedSprite((x * TILE_SIZE, y * TILE_SIZE), frames, [self.all_sprites])

        self.player = Player(
            pos=(100, 112),
            path=PATHS['player'],
            group=self.all_sprites)

    def update(self, dt):
        self.all_sprites.draw(self.screen)
        self.all_sprites.update(dt)
        pygame.draw.rect(self.screen, 'white', self.player.rect, 1)

