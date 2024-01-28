import random
import pygame
from src.sprites import CollisionObject, Decoration, AnimatedDecoration, Snowflake, Sleigh


class Platformer:
    def __init__(self, screen):

        # General setup
        self.screen = screen
        self.tile_width = 16
        self.tile_height = 16

        self.snowflakes = []

        # Create groups
        self.platforms_group = pygame.sprite.Group()
        self.ladders_group = pygame.sprite.Group()
        self.walls_with_collision_group = pygame.sprite.Group()
        self.decorations_group = pygame.sprite.Group()
        self.sleigh_group = pygame.sprite.Group()
        self.completed_sleigh_group = pygame.sprite.Group()

        # level_images
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
            13: [pygame.image.load(img_path + 'decor/candle_1.png').convert_alpha(),
                 pygame.image.load(img_path + 'decor/candle_2.png').convert_alpha()],
            14: pygame.image.load(img_path + 'decor/painting_1.png').convert_alpha(),
            15: pygame.image.load(img_path + 'decor/painting_2.png').convert_alpha(),
            16: pygame.image.load(img_path + 'decor/table.png').convert_alpha(),
            17: pygame.image.load(img_path + 'decor/chair.png').convert_alpha(),
            18: pygame.transform.flip(pygame.image.load(img_path + 'decor/chair.png').convert_alpha(), True, False),
            19: pygame.image.load(img_path + 'decor/bed.png').convert_alpha(),
            20: pygame.image.load(img_path + 'walls/fire_wall_left.png').convert_alpha(),
            21: pygame.image.load(img_path + 'walls/fire_wall_right.png').convert_alpha(),
            22: pygame.image.load(img_path + 'walls/fire_wall_left.png').convert_alpha(),   # no collision
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

        # Refactor images (got rid of the empty block)

        # Rooms setup
        self.rooms = {
            'room_0_0': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                [7, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 21, 9, 9, 9, 9, 9, 9],
                [7, 0, 0, 0, 0, 0, 15, 0, 0, 0, 28, 0, 20, 21, 0, 0, 0, 0, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 21, 0, 0, 0, 0, 0, 0],
                [7, 0, 0, 27, 0, 0, 0, 0, 12, 0, 0, 0, 20, 21, 0, 0, 12, 0, 0, 0],
                [7, 1, 1, 1, 1, 1, 1, 1, 11, 1, 1, 1, 20, 21, 1, 1, 11, 1, 1, 31],
                [7, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 20, 21, 9, 9, 24, 0, 9, 9]
            ],

            'room_0_1': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
                [0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0],
                [0, 0, 0, 0, 0, 18, 16, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 1, 1, 31],
                [9, 9, 9, 9, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 7]
            ],

            'room_0_2': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0, 0, 0],
                [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 6, 0, 0],
                [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7, 0, 0, 0, 0, 0],
                [0, 0, 0, 13, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0, 0, 7, 0, 0, 0, 0, 0],
                [0, 27, 0, 0, 0, 0, 0, 0, 0, 33, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 31, 0, 0, 0, 0, 0],
                [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0]
            ],

            'room_1_0': [
                [7, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 20, 21, 0, 0, 10, 0, 0, 0],
                [7, 13, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 20, 21, 0, 0, 10, 0, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 20, 21, 0, 0, 10, 0, 0, 0],
                [7, 12, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 20, 21, 0, 0, 10, 0, 0, 27],
                [7, 11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 31, 31, 1, 1, 1, 1, 1, 31],
                [7, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 23, 0, 0, 0, 0, 0, 0],
                [7, 10, 0, 29, 0, 0, 0, 0, 0, 0, 18, 0, 26, 0, 0, 17, 0, 0, 0, 0],
                [7, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 31]
            ],

            'room_1_1': [
                [0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 7],
                [0, 0, 0, 0, 7, 13, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 10, 0, 0, 7],
                [0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 29, 10, 0, 0, 7],
                [0, 0, 12, 0, 7, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 7],
                [1, 1, 11, 1, 31, 1, 1, 11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 31],
                [0, 0, 10, 0, 13, 7, 0, 10, 0, 0, 13, 0, 0, 0, 13, 0, 0, 0, 0, 0],
                [0, 0, 10, 0, 0, 7, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 10, 0, 0, 7, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 31, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 31]
            ],

            'room_1_2': [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
                [0, 0, 0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 0, 32, 0, 0, 32, 0, 0, 7],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
                [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25]
            ]
        }

        self.current_room = self.rooms['room_0_2']

        self.rooms_list = ['room_0_0', 'room_0_1', 'room_0_2', 'room_1_0', 'room_1_1']
        self.random_room = self.get_random_room()
        self.sleigh_in_inventory = False
        self.completed_sleigh_pieces = []
        self.create_sleigh()

        # Populate the level with elements based on the current room layout
        self.populate_room()

    def populate_room(self):
        self.create_platforms(self.current_room)
        self.create_ladders(self.current_room)
        self.create_walls_with_collisions(self.current_room)
        self.create_decorations(self.current_room)
        self.create_animations(self.current_room)
        self.create_snow()

    def clear_room(self):
        self.platforms_group.empty()
        self.ladders_group.empty()
        self.walls_with_collision_group.empty()
        self.decorations_group.empty()

    def redraw_room(self):
        self.clear_room()
        self.populate_room()

    def create_elements(self, room_layout, valid_ids, element_type, group):
        elements = []

        for row_index, row in enumerate(room_layout):
            for col_index, tile_id in enumerate(row):
                if tile_id in valid_ids:
                    x_pos = col_index * self.tile_width
                    y_pos = row_index * self.tile_height

                    element = element_type(x_pos,
                                           y_pos,
                                           self.images[tile_id],
                                           group)
                    elements.append(element)

    def create_platforms(self, room_layout):
        return self.create_elements(room_layout, [1, 25], CollisionObject, self.platforms_group)

    def create_ladders(self, room_layout):
        return self.create_elements(room_layout, [10, 11, 24], CollisionObject, self.ladders_group)

    def create_walls_with_collisions(self, room_layout):
        return self.create_elements(room_layout, [7, 20, 21], CollisionObject, self.walls_with_collision_group)

    def create_decorations(self, room_layout):
        valid_ids = [2, 3, 4, 5, 6, 8, 9, 12, 14, 15, 16, 17, 18, 19, 22, 23, 27, 28, 29, 30, 31, 32]
        return self.create_elements(room_layout, valid_ids, Decoration, self.decorations_group)

    def create_animations(self, room_layout):
        return self.create_elements(room_layout, [13, 26], AnimatedDecoration, self.decorations_group)

    def create_snow(self):
        self.snowflakes.clear()

        snow_boundary = None
        second_boundary = None

        if self.current_room == self.rooms['room_0_0']:
            snow_boundary = pygame.Rect(0, 0, 320, 32)
        if self.current_room == self.rooms['room_0_1']:
            snow_boundary = pygame.Rect(0, 0, 320, 32)
        if self.current_room == self.rooms['room_0_2']:
            snow_boundary = pygame.Rect(0, 0, 240, 44)
            second_boundary = pygame.Rect(240, 0, 80, 144)
        if self.current_room == self.rooms['room_1_0']:
            self.snowflakes.clear()
        if self.current_room == self.rooms['room_1_1']:
            self.snowflakes.clear()
        if self.current_room == self.rooms['room_1_2']:
            snow_boundary = pygame.Rect(0, 0, 320, 144)

        for _ in range(20):
            if snow_boundary:
                x = random.randint(snow_boundary.left, snow_boundary.right)
                y = random.randint(snow_boundary.top, snow_boundary.bottom)
                self.snowflakes.append(Snowflake(x, y, self.screen, snow_boundary))

            if second_boundary:
                x_second = random.randint(second_boundary.left, second_boundary.right)
                y_second = random.randint(second_boundary.top, second_boundary.bottom)
                self.snowflakes.append(Snowflake(x_second, y_second, self.screen, second_boundary))

    def draw_snow(self):
        for snowflake in self.snowflakes:
            snowflake.draw()
            snowflake.update()

    def get_random_room(self):
        return random.choice(self.rooms_list)

    def get_platform_rects(self, room_layout):
        rects = []
        for row_index, row in enumerate(room_layout):
            for col_index, tile_id in enumerate(row):
                if tile_id == 1:
                    x_pos = col_index * self.tile_width
                    y_pos = row_index * self.tile_height
                    rects.append(pygame.Rect(x_pos, y_pos, self.tile_width, self.tile_height))
        return rects

    def create_sleigh(self):
        if not self.sleigh_in_inventory:

            # get a random room and platform
            self.random_room = self.get_random_room()
            platform_rects = self.get_platform_rects(self.rooms[self.random_room])
            random_platform_rect = random.choice(platform_rects)

            # get the position and image index based on the number of completed sleigh pieces
            pos = random_platform_rect.topleft
            image_index = len(self.completed_sleigh_pieces)

            # create a sleigh object with the appropriate image only if image_index is valid
            if image_index < 4:
                Sleigh(pos[0], pos[1], self.screen, self.images[33][image_index], self.sleigh_group)

        else:
            self.sleigh_group.empty()

    def sleigh_update(self):
        if self.current_room == self.rooms[self.random_room]:
            self.sleigh_group.update()
        else:
            self.sleigh_group.remove()

        if self.current_room == self.rooms['room_1_2']:
            self.completed_sleigh_group.update()

    def reset(self):
        self.current_room = self.rooms['room_0_2']
        self.redraw_room()
        self.sleigh_in_inventory = False
        self.completed_sleigh_pieces = []

    def update(self):
        self.draw_snow()
        self.platforms_group.draw(self.screen)
        self.ladders_group.draw(self.screen)
        self.walls_with_collision_group.draw(self.screen)
        self.decorations_group.draw(self.screen)
        self.decorations_group.update()
        self.sleigh_update()

        # for sleigh in self.sleigh_group:
        #     pygame.draw.rect(self.screen, 'red', sleigh.rect, 1)
        print(self.random_room)


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
