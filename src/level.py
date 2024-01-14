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
        self.walls_group = pygame.sprite.Group()
        self.walls_with_collision_group = pygame.sprite.Group()
        self.decorations_group = pygame.sprite.Group()

        # Ladders
        self.ladders_group = pygame.sprite.Group()
        self.ladders = {
            'ladder_1': Ladder(50, 150, 16, 50, self.screen, self.ladders_group),
            'ladder_2': Ladder(150, 100, 16, 50, self.screen, self.ladders_group)
        }

        # level_images
        img_path = 'assets/level/'
        self.images = [

            # empty
            pygame.image.load(img_path + 'empty/empty.png').convert_alpha(),

            # floor
            pygame.image.load(img_path + 'floor/floor.png').convert_alpha(),

            # roof
            pygame.image.load(img_path + 'roof/roof_top.png').convert_alpha(),
            pygame.image.load(img_path + 'roof/roof_bottom.png').convert_alpha(),
            pygame.image.load(img_path + 'roof/roof_end_top.png').convert_alpha(),
            pygame.image.load(img_path + 'roof/roof_end_bottom_left.png').convert_alpha(),
            pygame.image.load(img_path + 'roof/roof_end_bottom_right.png'),

            # walls
            pygame.image.load(img_path + 'walls/wall_left.png').convert_alpha(),
            pygame.image.load(img_path + 'walls/wall_right.png').convert_alpha(),
            pygame.image.load(img_path + 'walls/wall_top.png').convert_alpha(),
            pygame.image.load(img_path + 'walls/wall_top_right.png').convert_alpha(),

        ]

        # Rooms setup
        self.room_0_3 = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 0, 0, 0],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 5, 6, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],

        ]

        self.current_room = self.room_0_3

        # Create elements
        self.create_platforms(self.room_0_3)
        self.create_walls(self.room_0_3)
        self.create_walls_with_collisions(self.room_0_3)
        self.draw_decorations(self.room_0_3)

    def create_platforms(self, room_layout):
        platforms = []

        for row_index, row in enumerate(room_layout):
            for col_index, tile_id in enumerate(row):
                if tile_id == 1:
                    x_pos = col_index * self.tile_width
                    y_pos = row_index * self.tile_height

                    platform = Platform(x_pos,
                                        y_pos,
                                        self.tile_width,
                                        self.tile_height,
                                        self.images[1],
                                        self.screen,
                                        self.platforms_group)
                    platforms.append(platform)

        return platforms

    def create_walls(self, room_layout):
        walls = []

        for row_index, row in enumerate(room_layout):
            for col_index, tile_id in enumerate(row):
                if tile_id == 9:
                    x_pos = col_index * self.tile_width
                    y_pos = row_index * self.tile_height

                    top_walls = Wall(x_pos,
                                     y_pos,
                                     self.tile_width,
                                     self.tile_height,
                                     self.images[9],
                                     self.screen,
                                     self.walls_group)
                    walls.append(top_walls)

    def create_walls_with_collisions(self, room_layout):
        walls_with_collisions = []

        for row_index, row in enumerate(room_layout):
            for col_index, tile_id in enumerate(row):
                if tile_id == 8:
                    x_pos = col_index * self.tile_width
                    y_pos = row_index * self.tile_height

                    wall_with_collisions = Wall(x_pos,
                                                y_pos,
                                                self.tile_width,
                                                self.tile_height,
                                                self.images[8],
                                                self.screen,
                                                self.walls_with_collision_group)
                    walls_with_collisions.append(wall_with_collisions)

    def draw_decorations(self, room_layout):
        decorations = []

        for row_index, row in enumerate(room_layout):
            for col_index, tile_id in enumerate(row):
                if tile_id in [0, 2, 3, 4, 5, 6]:
                    x_pos = col_index * self.tile_width
                    y_pos = row_index * self.tile_height

                    decoration = Decoration(x_pos,
                                            y_pos,
                                            self.tile_width,
                                            self.tile_height,
                                            self.images[tile_id],
                                            self.screen,
                                            self.decorations_group)
                    decorations.append(decoration)
