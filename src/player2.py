import pygame
from os import walk
from src.config import *
from src.sprites import Sleigh
from src.entity import Entity


class Player(Entity):
    def __init__(self, pos, screen, platformer, path, group):
        super().__init__(pos, screen, platformer, path, group)

        self.climbing = False
        self.landed = False
        self.sleigh_completed = False

    def animate(self, dt):
        if self.animation_possible:
            self.frame_index += 7 * dt
            if self.frame_index >= len(self.frames[self.status]):
                self.frame_index = 0
        else:
            self.frame_index = 1

        self.image = self.frames[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        # horizontal
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.animation_possible = True
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.animation_possible = True
            self.status = 'left'
        else:
            self.direction.x = 0

        # vertical
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.animation_possible = True
            self.status = 'climb'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.animation_possible = True
            self.status = 'climb'
        else:
            self.direction.y = 0

        if not any((keys[pygame.K_RIGHT], keys[pygame.K_LEFT], keys[pygame.K_UP], keys[pygame.K_DOWN])):
            self.animation_possible = False

    def move_between_rooms(self):
        current_room = self.platformer.current_room

        for direction, (next_room, adjustment) in ROOM_TRANSITIONS[current_room].items():
            if direction == 'left' and self.rect.left < 0:
                self.platformer.current_room = next_room
                self.pos.x = adjustment
                self.platformer.redraw_room()
            elif direction == 'right' and self.rect.right > WIDTH + 5:
                self.platformer.current_room = next_room
                self.pos.x = adjustment
                self.platformer.redraw_room()
            elif direction == 'up' and self.rect.top < -5:
                self.platformer.current_room = next_room
                self.pos.y = adjustment
                self.platformer.redraw_room()
            elif direction == 'down' and self.rect.bottom > 144:
                self.platformer.current_room = next_room
                self.pos.y = adjustment
                self.platformer.redraw_room()

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.move_between_rooms()
        pygame.draw.rect(self.screen, 'green', self.rect)
