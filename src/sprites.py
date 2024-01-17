import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos

        # Image & Rect
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))


class Ladder(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos

        # Image & Rect
        self.image = image
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))


class Wall(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos

        # Image & Rect
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))


class Decoration(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos

        # Image & Rect
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))


class AnimatedDecoration(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, image, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos

        # Image & Rect
        self.frames = image
        self.frames_index = 0

        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))

    def animate(self):

        self.frames_index += 0.2
        if self.frames_index >= len(self.frames):
            self.frames_index = 0

        self.image = self.frames[int(self.frames_index)]

    def update(self):
        self.animate()
