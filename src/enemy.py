import random

import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, platformer, group):
        super().__init__(group)

        self.screen = screen
        self.platformer = platformer

        self.frames = {
            'walk_right':
                [pygame.transform.flip(pygame.image.load(f'assets/enemy/elf/walk/elf_walk_{i}.png').convert_alpha(),
                                       True, False) for i in range(1, 5)],
            'walk_left':
                [pygame.image.load(f'assets/enemy/elf/walk/elf_walk_{i}.png').convert_alpha() for i in range(1, 5)],
            'climbing':
                [pygame.image.load(f'assets/enemy/elf/climb/elf_climb_{i}.png').convert_alpha() for i in range(1, 5)]
        }

        self.frame_index = 0
        self.status = 'walk_left'
        self.animation_possible = True

        self.image = self.frames[self.status][self.frame_index]
        self.rect = self.image.get_rect()

        # Movement attributes
        self.speed = 1
        self.spawn_position = (-20, -20)

        self.spawn()

        # create spawning position for each room
        # create probability to go left or right
        # create functionality what happens when off-screen
        # create player response when collided with player (flash player, steal a sleigh piece)

    spawn_positions = {
        'room_0_0': [(20, 112)],
        'room_0_1': [(20, 112), (340, 112)],
        'room_0_2': [(-20, 112)],
    }

    def animate(self):
        if self.animation_possible:
            self.frame_index += 0.2
            if self.frame_index >= len(self.frames[self.status]):
                self.frame_index = 0
        else:
            self.frame_index = 1

        self.image = self.frames[self.status][int(self.frame_index)]

    def get_current_room(self):
        for key, value in self.platformer.rooms.items():
            if self.platformer.current_room == value:
                return key

    def spawn(self):
        self.spawn_position = random.choice(self.spawn_positions[self.get_current_room()])
        self.rect.midbottom = (self.spawn_position[0], self.spawn_position[1])

    def move(self):
        if self.spawn_position[0] < 0:
            self.status = 'walk_right'
            self.rect.x += 1

    def update(self):
        self.animate()
        self.move()
