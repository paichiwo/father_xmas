import pygame
from src.sprites import Platform, Ladder, Wall, Decoration, AnimatedDecoration


class Level:
    def __init__(self, screen):

        # General setup
        self.screen = screen
        self.tile_width = 16
        self.tile_height = 16

        # Create groups
        self.platforms_group = pygame.sprite.Group()
        self.ladders_group = pygame.sprite.Group()
        self.walls_with_collision_group = pygame.sprite.Group()
        self.decorations_group = pygame.sprite.Group()

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
            14: pygame.image.load(img_path + 'decor/girland_left.png').convert_alpha(),
            15: pygame.image.load(img_path + 'decor/girland_right.png').convert_alpha(),
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
            26: [pygame.image.load(img_path + f'decor/fireplace_{i}.png').convert_alpha() for i in range(1, 5)],
        }

        # Rooms setup
        self.room_0_0 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [7, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 21, 9, 9, 9, 9, 9, 9],
            [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 21, 0, 0, 0, 0, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 21, 0, 0, 0, 0, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 20, 21, 0, 0, 12, 0, 0, 0],
            [7, 1, 1, 1, 1, 1, 1, 1, 11, 1, 1, 1, 20, 21, 1, 1, 11, 1, 1, 1],
            [7, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 20, 21, 9, 9, 24, 0, 9, 9]
        ]

        self.room_0_1 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 18, 16, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 1, 1, 1],
            [9, 9, 9, 9, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 7]
        ]

        self.room_0_2 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0, 0, 0],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 6, 0, 0],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7, 0, 0, 0, 0, 0],
            [0, 0, 0, 13, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0, 0, 7, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0]
        ]

        self.room_1_0 = [
            [7, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 20, 21, 0, 0, 10, 0, 0, 0],
            [7, 13, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 20, 21, 0, 0, 10, 0, 0, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 20, 21, 0, 0, 10, 0, 0, 0],
            [7, 12, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 20, 21, 0, 0, 10, 0, 0, 0],
            [7, 11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [7, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 23, 0, 0, 0, 0, 0, 0],
            [7, 10, 0, 0, 0, 0, 0, 0, 0, 0, 18, 0, 22, 23, 0, 17, 0, 0, 0, 0],
            [7, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 0, 0, 0, 0, 0, 0, 0],
            [7, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.room_1_1 = [
            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 7],
            [0, 0, 0, 0, 7, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 7],
            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 7],
            [0, 0, 12, 0, 7, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 7],
            [1, 1, 11, 1, 1, 1, 1, 11, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 10, 0, 13, 7, 0, 10, 0, 13, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0],
            [0, 0, 10, 0, 0, 7, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 10, 0, 0, 7, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.room_1_2 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
            [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25]
        ]

        self.current_room = self.room_1_0

        # Populate the level with elements based on the current room layout
        self.populate_room()

    def populate_room(self):
        self.create_platforms(self.current_room)
        self.create_ladders(self.current_room)
        self.create_walls_with_collisions(self.current_room)
        self.draw_decorations(self.current_room)
        self.draw_animations(self.current_room)

    def clear_room(self):
        self.platforms_group.empty()
        self.ladders_group.empty()
        self.walls_with_collision_group.empty()
        self.decorations_group.empty()

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
        return self.create_elements(room_layout, [1, 25], Platform, self.platforms_group)

    def create_ladders(self, room_layout):
        return self.create_elements(room_layout, [10, 11, 24], Ladder, self.ladders_group)

    def create_walls_with_collisions(self, room_layout):
        return self.create_elements(room_layout, [7, 20, 21], Wall, self.walls_with_collision_group)

    def draw_decorations(self, room_layout):
        valid_ids = [0, 2, 3, 4, 5, 6, 8, 9, 12, 14, 15, 16, 17, 18, 19, 22, 23]
        return self.create_elements(room_layout, valid_ids, Decoration, self.decorations_group)

    def draw_animations(self, room_layout):
        return self.create_elements(room_layout, [13, 26], AnimatedDecoration, self.decorations_group)

    def redraw_room(self):
        self.clear_room()
        self.populate_room()

    def reset(self):
        self.current_room = self.room_0_2
        self.redraw_room()

    def draw(self):
        self.platforms_group.draw(self.screen)
        self.ladders_group.draw(self.screen)
        self.walls_with_collision_group.draw(self.screen)
        self.decorations_group.draw(self.screen)
        self.decorations_group.update()
