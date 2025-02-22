import random
from os import walk

from src.sprites import SimpleSprite, AnimatedSprite, Snowflake, Sleigh
from src.player import Player
from src.enemy import EnemyElf
from src.config import *


class Platformer:
    def __init__(self, screen):

        # General setup
        self.screen = screen

        # sleigh
        self.completed_sleigh_pieces = []
        self.sleigh_in_inventory = False
        self.sleigh_completed = False

        # snow
        self.snowflakes = []

        # Create groups
        self.player_group = pygame.sprite.GroupSingle()
        self.platforms_group = pygame.sprite.Group()
        self.ladders_group = pygame.sprite.Group()
        self.collision_walls = pygame.sprite.Group()
        self.decorations_group = pygame.sprite.Group()
        self.sleigh_group = pygame.sprite.Group()
        self.completed_sleigh_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.frames = {}

        img_path = 'assets/level/'
        self.images = {
            0: pygame.image.load(img_path + 'empty/empty.png').convert_alpha(),
            1: pygame.image.load(img_path + 'floor/floor.png').convert_alpha(),
            2: pygame.image.load(img_path + 'roof/roof_top_.png').convert_alpha(),
            3: pygame.image.load(img_path + 'roof/roof_bottom.png').convert_alpha(),
            4: pygame.image.load(img_path + 'roof/roof_end_top.png').convert_alpha(),
            5: pygame.image.load(img_path + 'roof/roof_end_bottom_left.png').convert_alpha(),
            6: pygame.image.load(img_path + 'roof/roof_end_bottom_right.png').convert_alpha(),
            7: pygame.image.load(img_path + 'walls/wall.png').convert_alpha(),
            8: pygame.image.load(img_path + 'walls/wall_top.png').convert_alpha(),
            9: pygame.image.load(img_path + 'decor/girland.png').convert_alpha(),
            10: pygame.image.load(img_path + 'ladders/ladder_tile_32.png').convert_alpha(),
            11: pygame.image.load(img_path + 'ladders/ladder_floor_32.png').convert_alpha(),
            12: pygame.image.load(img_path + 'ladders/ladder_top_32.png').convert_alpha(),
            13: [pygame.image.load(img_path + f'decor/candle_{i}.png').convert_alpha() for i in range(1, 3)],
            14: pygame.image.load(img_path + 'decor/painting_1.png').convert_alpha(),
            15: pygame.image.load(img_path + 'decor/painting_2.png').convert_alpha(),
            16: pygame.image.load(img_path + 'decor/table.png').convert_alpha(),
            17: pygame.image.load(img_path + 'decor/chair.png').convert_alpha(),
            18: pygame.transform.flip(pygame.image.load(img_path + 'decor/chair.png').convert_alpha(), True, False),
            19: pygame.image.load(img_path + 'decor/bed.png').convert_alpha(),
            20: pygame.image.load(img_path + 'walls/fire_wall_left.png').convert_alpha(),
            21: pygame.image.load(img_path + 'walls/fire_wall_right.png').convert_alpha(),
            22: pygame.image.load(img_path + 'walls/fire_wall_left.png').convert_alpha(),  # no collision
            23: pygame.image.load(img_path + 'walls/fire_wall_right.png').convert_alpha(),  # no collision
            24: pygame.image.load(img_path + 'ladders/ladder_girland_32.png').convert_alpha(),
            25: pygame.image.load(img_path + 'floor/floor_snow.png').convert_alpha(),
            26: [pygame.image.load(img_path + f'decor/fire_place_{i}.png').convert_alpha() for i in range(1, 5)],
            27: pygame.image.load(img_path + 'decor/stool.png').convert_alpha(),
            28: pygame.image.load(img_path + 'decor/bookcase.png').convert_alpha(),
            29: pygame.image.load(img_path + 'decor/plant.png').convert_alpha(),
            30: pygame.image.load(img_path + 'sleigh/raindeer.png').convert_alpha(),
            31: pygame.image.load(img_path + 'floor/floor.png').convert_alpha(),  # no collision
            32: pygame.image.load(img_path + 'decor/xmas_tree.png').convert_alpha(),
            33: [pygame.image.load(img_path + f'sleigh/sleigh_{i}.png').convert_alpha() for i in range(1, 5)]
        }

        # Rooms setup
        self.rooms = ROOMS

        # Rooms setup
        self.current_room = 'room_0_2'
        self.rooms_list = ['room_0_0', 'room_0_1', 'room_0_2', 'room_1_0', 'room_1_1']
        self.random_room = self.get_random_room()

        # Populate the level with elements based on the current room layout
        self.player = Player(
            pos=(100, 112),
            screen=self.screen,
            platformer=self,
            path=PATHS['player'],
            group=self.player_group)
        self.populate_room()
        self.create_sleigh()

        # timers
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = random.randint(2000, 5000)
        self.create_enemies()

    def populate_room(self):
        self.create_platforms(self.rooms[self.current_room])
        self.create_ladders(self.rooms[self.current_room])
        self.create_walls_with_collisions(self.rooms[self.current_room])
        self.create_decorations(self.rooms[self.current_room])
        self.create_animations(self.rooms[self.current_room])
        self.create_snow()

    def clear_room(self):
        self.platforms_group.empty()
        self.ladders_group.empty()
        self.collision_walls.empty()
        self.decorations_group.empty()
        self.enemy_group.empty()

    def redraw_room(self):
        self.clear_room()
        self.enemy_group.empty()
        self.populate_room()
        self.create_enemies()

    def create_elements(self, room_layout, valid_ids, element_type, group):
        elements = []

        for row_index, row in enumerate(room_layout):
            for col_index, tile_id in enumerate(row):
                if tile_id in valid_ids:
                    x_pos = col_index * TILE_SIZE
                    y_pos = row_index * TILE_SIZE

                    element = element_type((x_pos, y_pos),
                                           self.images[tile_id],
                                           group)
                    elements.append(element)

    def create_platforms(self, room_layout):
        return self.create_elements(room_layout, [1, 25], SimpleSprite, self.platforms_group)

    def create_ladders(self, room_layout):
        return self.create_elements(room_layout, [10, 11, 24], SimpleSprite, self.ladders_group)

    def create_walls_with_collisions(self, room_layout):
        return self.create_elements(room_layout, [7, 20, 21], SimpleSprite, self.collision_walls)

    def create_decorations(self, room_layout):
        valid_ids = [2, 3, 4, 5, 6, 8, 9, 12, 14, 15, 16, 17, 18, 19, 22, 23, 27, 28, 29, 30, 31, 32]
        return self.create_elements(room_layout, valid_ids, SimpleSprite, self.decorations_group)

    def create_animations(self, room_layout):
        return self.create_elements(room_layout, [13, 26], AnimatedSprite, self.decorations_group)

    def create_snow(self):
        self.snowflakes.clear()
        snow_boundary = None
        second_boundary = None

        if self.current_room == 'room_0_0' or self.current_room == 'room_0_1':
            snow_boundary = pygame.Rect(0, 0, 320, 32)
        if self.current_room == 'room_0_2':
            snow_boundary, second_boundary = pygame.Rect(0, 0, 240, 44), pygame.Rect(240, 0, 80, 144)
        if self.current_room == 'room_1_0' or self.current_room == 'room_1_1':
            self.snowflakes.clear()
        if self.current_room == 'room_1_2':
            snow_boundary = pygame.Rect(0, 0, 320, 144)

        for _ in range(20):
            if snow_boundary:
                self.snow_fall(snow_boundary)
            if second_boundary:
                self.snow_fall(second_boundary)

    def snow_fall(self, boundary):
        x = random.randint(boundary.left, boundary.right)
        y = random.randint(boundary.top, boundary.bottom)
        self.snowflakes.append(Snowflake(x, y, self.screen, boundary))

    def draw_snow(self):
        for snowflake in self.snowflakes:
            snowflake.draw()
            snowflake.update()

    def get_random_room(self):
        return random.choice(self.rooms_list)

    @ staticmethod
    def get_platform_rects(room_layout):
        rects = []
        for row_index, row in enumerate(room_layout):
            for col_index, tile_id in enumerate(row):
                if tile_id == 1:
                    x_pos = col_index * TILE_SIZE
                    y_pos = row_index * TILE_SIZE
                    rects.append(pygame.Rect(x_pos, y_pos, TILE_SIZE, TILE_SIZE))
        return rects

    def create_sleigh(self):
        if not self.sleigh_in_inventory:

            self.random_room = self.get_random_room()
            platform_rects = self.get_platform_rects(self.rooms[self.random_room])
            random_platform_rect = random.choice(platform_rects)

            pos = random_platform_rect.topleft
            image_index = len(self.completed_sleigh_pieces)

            if image_index < 4:
                Sleigh((pos[0], pos[1]), self.screen, self.images[33][image_index], self.sleigh_group)

        else:
            self.sleigh_group.empty()

    def sleigh_update(self):
        if self.current_room == self.random_room:
            self.sleigh_group.update()
        else:
            self.sleigh_group.remove()

        if self.current_room == 'room_1_2':
            self.completed_sleigh_group.update()

    def create_enemies(self):
        self.enemy_spawn_timer += pygame.time.get_ticks()
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            enemy_spawn_data = random.choice(ENEMY_SPAWN_POS[self.current_room])
            EnemyElf(pos=(enemy_spawn_data[0], enemy_spawn_data[1]),
                     direction_x=enemy_spawn_data[2],
                     screen=self.screen,
                     platformer=self,
                     path=PATHS['elf'],
                     group=self.enemy_group)

            self.enemy_spawn_timer = 0
            self.enemy_spawn_delay = random.randint(2000, 5000)

    def reset(self):
        self.player.reset()
        self.current_room = 'room_0_2'
        self.redraw_room()
        self.completed_sleigh_pieces = []
        self.sleigh_in_inventory = False
        self.sleigh_completed = False

    def update(self, dt):
        self.draw_snow()

        self.platforms_group.draw(self.screen)
        self.ladders_group.draw(self.screen)
        self.collision_walls.draw(self.screen)

        self.decorations_group.draw(self.screen)
        self.player_group.draw(self.screen)
        self.enemy_group.draw(self.screen)

        self.decorations_group.update(dt)
        self.player_group.update(dt)
        self.enemy_group.update(dt)

        self.sleigh_update()


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
