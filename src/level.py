import pygame
from src.sprites import Platform, Ladder, Wall, Decoration


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
        self.walls_group = pygame.sprite.Group()
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
            11: pygame.image.load(img_path + 'ladders/ladder_floor_tile_32.png').convert_alpha(),
            12: pygame.image.load(img_path + 'ladders/ladder_top_32.png').convert_alpha()
        }

        # Rooms setup
        self.room_0_2 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 11, 1, 1, 1],
            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 7],
            [0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 7],
        ]

        self.room_0_3 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0, 0, 0],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 6, 0, 0],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 7, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        ]

        self.current_room = self.room_0_3

        # Populate the level with elements based on the current room layout
        self.populate_room()

    def populate_room(self):
        self.create_platforms(self.current_room)
        self.create_walls(self.current_room)
        self.create_ladders(self.current_room)
        self.create_walls_with_collisions(self.current_room)
        self.draw_decorations(self.current_room)

    def clear_room(self):
        self.platforms_group.empty()
        self.walls_group.empty()
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
                                           self.tile_width,
                                           self.tile_height,
                                           self.images[tile_id],
                                           self.screen,
                                           group)
                    elements.append(element)

    def create_platforms(self, room_layout):
        return self.create_elements(room_layout, [1], Platform, self.platforms_group)

    def create_ladders(self, room_layout):
        return self.create_elements(room_layout, [10, 11], Ladder, self.ladders_group)

    def create_walls(self, room_layout):
        return self.create_elements(room_layout, [8], Wall, self.walls_group)

    def create_walls_with_collisions(self, room_layout):
        return self.create_elements(room_layout, [7], Wall, self.walls_with_collision_group)

    def draw_decorations(self, room_layout):
        return self.create_elements(room_layout, [0, 2, 3, 4, 5, 6, 9, 12], Decoration, self.decorations_group)

    def draw(self):
        self.platforms_group.draw(self.screen)
        self.ladders_group.draw(self.screen)
        self.walls_group.draw(self.screen)
        self.walls_with_collision_group.draw(self.screen)
        self.decorations_group.draw(self.screen)