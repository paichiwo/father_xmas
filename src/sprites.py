import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, length, height, image, screen, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.length = length
        self.height = height
        self.screen = screen

        # Image & Rect
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))


class Ladder(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, length, height, image, screen, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.length = length
        self.height = height
        self.screen = screen

        # Image & Rect
        self.image = image
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))


class Wall(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, length, height, image, screen, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.length = length
        self.height = height
        self.screen = screen

        # Image & Rect
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))


class Decoration(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, length, height, image, screen, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.length = length
        self.height = height
        self.screen = screen

        # Image & Rect
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
