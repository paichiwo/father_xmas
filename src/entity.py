import pygame
from os import walk


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, screen, platformer, path, group):
        super().__init__(group)

        # General setup
        self.screen = screen
        self.platformer = platformer

        # Image, Rect, Animation
        self.frames = {}
        self.import_assets(path)
        self.frame_index = 1
        self.status = 'left'

        self.image = self.frames[self.status][self.frame_index]
        self.rect = self.image.get_rect(midbottom=pos)
        self.animation_possible = True

        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom, self.rect.width, 3)
        self.hitbox = pygame.Rect(self.rect[0], self.rect[1], self.rect[2] - 4, self.rect[3])

        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 120

        self.climbing = False
        self.landed = False

    def import_assets(self, path):
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.frames[name] = []
            else:
                for file_name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                    path = folder[0].replace('\\', '/') + '/' + file_name
                    surf = pygame.image.load(path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.frames[key].append(surf)

    def move(self, dt):
        # horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)

        # horizontal
        if self.climbing:
            self.pos.y += self.direction.y * self.speed * dt
            self.rect.y = round(self.pos.y)

