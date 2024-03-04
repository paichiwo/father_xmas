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

        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 120

        self.climbing = False
        self.landed = False

    def animate(self, dt):
        if self.animation_possible:
            self.frame_index += 7 * dt
            if self.frame_index >= len(self.frames[self.status]):
                self.frame_index = 0
        else:
            self.frame_index = 1

        self.image = self.frames[self.status][int(self.frame_index)]

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
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)

        pygame.draw.rect(self.screen, 'orange', self.bottom)

    def collisions(self):
        # platform collision
        self.landed = False
        for i in range(len(self.platformer.platforms_group)):
            for platform in self.platformer.platforms_group:
                if self.bottom.colliderect(platform.rect):
                    self.landed = True
                    if not self.climbing:
                        self.direction.y = 0
                        self.rect.bottom = platform.rect[1]

        # wall collision
        for wall in self.platformer.collision_walls:
            hitbox = pygame.Rect(
                self.rect[0] + (2 if self.direction.x > 0 else -2), self.rect[1], self.rect[2],self.rect[3])

            if hitbox.colliderect(wall.rect):
                if self.direction.x > 0:
                    self.rect.right = wall.rect.left
                else:
                    self.rect.left = wall.rect.right
                self.pos.x = hitbox[0]

        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom, self.rect.width, 3)

    def check_climb(self):
        can_climb = False
        climb_down = False
        middle_of_ladder = False

        under = pygame.rect.Rect((self.rect[0], self.rect[1] + self.rect.height),
                                 (self.rect[2], self.rect[3] //3))
        pygame.draw.rect(self.screen, 'yellow', under)
        offset = 3

        for ladder in self.platformer.ladders_group:
            # going up
            if self.rect.colliderect(ladder.rect) and not can_climb:
                can_climb = True
                ladder_middle_x = ladder.rect.centerx
                player_middle_x = under.centerx
                middle_of_ladder = abs(player_middle_x - ladder_middle_x) <= offset

            # going down
            if under.colliderect(ladder.rect):
                climb_down = True
                ladder_middle_x = ladder.rect.centerx
                player_middle_x = under.centerx
                middle_of_ladder = abs(player_middle_x - ladder_middle_x) <= offset

        if (not can_climb and (not climb_down or self.direction.y < 0)) or (
                self.landed and can_climb and self.direction.y > 0 and not climb_down):
            self.climbing = False

        return can_climb, climb_down, middle_of_ladder
