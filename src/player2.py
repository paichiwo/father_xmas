from src.config import *
from src.sprites import Sleigh
from src.entity import Entity


class Player(Entity):
    def __init__(self, pos, screen, platformer, path, group):
        super().__init__(pos, screen, platformer, path, group)

    def animate(self, dt):
        if self.animation_possible:
            self.frame_index += 7 * dt
            if self.frame_index >= len(self.frames[self.status]):
                self.frame_index = 0
        else:
            self.frame_index = 1

        self.image = self.frames[self.status][int(self.frame_index)]

    def input(self):
        can_climb, climbed_down, middle_of_ladder = self.check_climb()
        keys = pygame.key.get_pressed()

        # horizontal
        if keys[pygame.K_RIGHT] and not self.climbing:
            self.direction.x = 1
            self.animation_possible = True
            self.status = 'right'
        elif keys[pygame.K_LEFT] and not self.climbing:
            self.direction.x = -1
            self.animation_possible = True
            self.status = 'left'
        else:
            self.direction.x = 0

        # vertical
        if keys[pygame.K_UP] and middle_of_ladder:
            if can_climb:
                self.direction.y = -1
                self.animation_possible = True
                self.climbing = True
                self.status = 'climb'
        elif keys[pygame.K_DOWN] and middle_of_ladder:
            if climbed_down:
                self.direction.y = 1
                self.animation_possible = True
                self.climbing = True
                self.status = 'climb'
        else:
            self.direction.y = 0
            if self.climbing and self.landed:
                self.climbing = False

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

    def collect_sleigh(self):
        if self.platformer.current_room == self.platformer.random_room:
            for sleigh in self.platformer.sleigh_group:
                if self.rect.colliderect(sleigh.rect):
                    self.platformer.sleigh_in_inventory = True
                    sleigh.kill()

    def leave_sleigh(self):
        if self.platformer.current_room == 'room_1_2':
            if self.platformer.sleigh_in_inventory:
                if self.rect.x == 100:

                    pos = (112 - 16 * len(self.platformer.completed_sleigh_pieces), 128)
                    index = len(self.platformer.completed_sleigh_pieces)

                    Sleigh(
                        pos=(pos[0], pos[1]),
                        screen=self.screen,
                        surf=self.platformer.images[33][index],
                        group=self.platformer.completed_sleigh_group)

                    self.platformer.sleigh_in_inventory = False
                    self.platformer.completed_sleigh_pieces.append(str(index + 1))
                    self.platformer.sleigh_group.empty()
                    self.platformer.create_sleigh()

                    if len(self.platformer.completed_sleigh_pieces) == 4:
                        self.platformer.sleigh_completed = True

    def reset(self):
        self.rect.midbottom = (100, 150)
        self.status = 'left'

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)

        self.collisions()

        self.move_between_rooms()

        self.collect_sleigh()
        self.leave_sleigh()
