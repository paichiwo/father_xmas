import pygame
from src.config import *
from src.sprites import Sleigh


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, screen, platformer, group):
        super().__init__(group)

        # General setup
        self.screen = screen
        self.platformer = platformer

        # Image & Rect
        self.frames = {
            'walk_left':
                [pygame.transform.flip(pygame.image.load(f'assets/player/walk/santa_walk_{i}.png').convert_alpha(),
                                       True, False) for i in range(1, 5)],
            'walk_right':
                [pygame.image.load(f'assets/player/walk/santa_walk_{i}.png').convert_alpha() for i in range(1, 5)],
            'climbing':
                [pygame.image.load(f'assets/player/climb/santa_climb_{i}.png').convert_alpha() for i in range(1, 5)]
        }

        # Animation index
        self.status = 'walk_left'
        self.frame_index = 1
        self.animation_possible = False

        self.image = self.frames[self.status][self.frame_index]
        self.rect = self.image.get_rect(midbottom=pos)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom, self.rect.width, 3)

        # Movement attributes
        self.speed = 2
        self.y_change = 0
        self.x_change = 0
        self.climbing = False
        self.landed = False
        self.sleigh_completed = False

    def animate(self):
        if self.animation_possible:
            self.frame_index += 0.1
            if self.frame_index >= len(self.frames[self.status]):
                self.frame_index = 0
        else:
            self.frame_index = 1

        self.image = self.frames[self.status][int(self.frame_index)]

    def check_landed(self):
        for i in range(len(self.platformer.platforms_group)):
            for platform in self.platformer.platforms_group:
                if self.bottom.colliderect(platform.rect):
                    self.landed = True
                    if not self.climbing:
                        if self.rect.bottom != platform.rect[1]:
                            self.y_change = 0

                        self.rect.bottom = platform.rect[1]

    def check_climb(self):
        can_climb = False
        climb_down = False
        middle_of_ladder = False

        under = pygame.rect.Rect((self.rect[0], self.rect[1] + self.rect.height),
                                 (self.rect[2], self.rect[3]))
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

        if (not can_climb and (not climb_down or self.y_change < 0)) or (
                self.landed and can_climb and self.y_change > 0 and not climb_down):
            self.climbing = False

        return can_climb, climb_down, middle_of_ladder

    def check_wall_collision(self):
        for wall in self.platformer.walls_with_collision_group:

            if self.x_change > 0:
                player_hitbox = pygame.Rect(self.rect[0]+2, self.rect[1], self.rect[2], self.rect[3])
                if player_hitbox.colliderect(wall.rect):
                    self.x_change = 0

            elif self.x_change < 0:
                player_hitbox = pygame.Rect(self.rect[0]-2, self.rect[1], self.rect[2], self.rect[3])
                if player_hitbox.colliderect(wall.rect):
                    self.x_change = 0

    def move(self):
        self.rect.move_ip(self.x_change * self.speed, self.y_change)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom, self.rect.width, 3)

    def move_between_rooms(self):
        # room 0_0
        if self.platformer.current_room == self.platformer.rooms['room_0_0']:

            # move right
            if self.rect.right > WIDTH+5:
                self.platformer.current_room = self.platformer.rooms['room_0_1']
                self.rect.x = 0
                self.update_room()

            # move down
            if self.rect.bottom > 144:
                self.platformer.current_room = self.platformer.rooms['room_1_0']
                self.rect.midtop = (self.rect.midbottom[0], -5)
                self.update_room()

        # room 0_1
        elif self.platformer.current_room == self.platformer.rooms['room_0_1']:

            # move left
            if self.rect.left < 0:
                self.platformer.current_room = self.platformer.rooms['room_0_0']
                self.rect.x = WIDTH - self.rect.width
                self.update_room()

            # move right
            if self.rect.right > WIDTH+5:
                self.platformer.current_room = self.platformer.rooms['room_0_2']
                self.rect.x = 0
                self.update_room()

            # move down
            if self.rect.bottom > 144:
                self.platformer.current_room = self.platformer.rooms['room_1_1']
                self.rect.midtop = (self.rect.midbottom[0], -5)
                self.update_room()

        # room 0_2
        elif self.platformer.current_room == self.platformer.rooms['room_0_2']:

            # move left
            if self.rect.left < 0:
                self.platformer.current_room = self.platformer.rooms['room_0_1']
                self.rect.x = WIDTH - self.rect.width
                self.update_room()

        # room 1_0
        elif self.platformer.current_room == self.platformer.rooms['room_1_0']:

            # move right
            if self.rect.right > WIDTH+5:
                self.platformer.current_room = self.platformer.rooms['room_1_1']
                self.rect.x = 0
                self.update_room()

            # move up
            if self.rect.top < -5:
                self.platformer.current_room = self.platformer.rooms['room_0_0']
                self.rect.midbottom = (self.rect.midbottom[0], 144)
                self.update_room()

        # room 1_1
        elif self.platformer.current_room == self.platformer.rooms['room_1_1']:

            # move left
            if self.rect.left < 0:
                self.platformer.current_room = self.platformer.rooms['room_1_0']
                self.rect.x = WIDTH - self.rect.width
                self.update_room()

            # move right
            if self.rect.right > WIDTH:
                self.platformer.current_room = self.platformer.rooms['room_1_2']
                self.rect.x = 0
                self.update_room()

            # move up
            if self.rect.top < -5:
                self.platformer.current_room = self.platformer.rooms['room_0_1']
                self.rect.midbottom = (self.rect.midbottom[0], 144)
                self.update_room()

        # room 1_2
        elif self.platformer.current_room == self.platformer.rooms['room_1_2']:

            # move left
            if self.rect.left < 0:
                self.platformer.current_room = self.platformer.rooms['room_1_1']
                self.rect.x = WIDTH - self.rect.width
                self.update_room()

    def update_room(self):
        self.platformer.redraw_room()

    def check_sleigh_collision(self):
        if self.platformer.current_room == self.platformer.rooms[self.platformer.random_room]:
            for sleigh in self.platformer.sleigh_group:
                if self.rect.colliderect(sleigh.rect):
                    self.platformer.sleigh_in_inventory = True
                    sleigh.kill()

    def leave_sleigh(self):
        if self.platformer.current_room == self.platformer.rooms['room_1_2']:
            if self.platformer.sleigh_in_inventory:
                if self.rect.x == 100:

                    # get the position and image index based on the number of completed sleigh pieces
                    pos = (112 - 16 * len(self.platformer.completed_sleigh_pieces), 128)
                    image_index = len(self.platformer.completed_sleigh_pieces)

                    # create a sleigh object with the appropriate image
                    Sleigh((pos[0], pos[1]), self.screen, self.platformer.images[33][image_index],
                           self.platformer.completed_sleigh_group)

                    # update the sleigh status and create a new sleigh
                    self.platformer.sleigh_in_inventory = False
                    self.platformer.completed_sleigh_pieces.append(str(image_index + 1))
                    self.platformer.sleigh_group.empty()
                    self.platformer.create_sleigh()

                    # check if the sleigh is completed
                    if len(self.platformer.completed_sleigh_pieces) == 4:
                        self.sleigh_completed = True

    def controls(self, event):

        can_climb, climbed_down, middle_of_ladder = self.check_climb()

        keys = pygame.key.get_pressed()
        if not any(keys[key] for key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]):
            self.frame_index = 1
            self.animation_possible = False

        if event.type == pygame.KEYDOWN:
            if not self.animation_possible:
                self.animation_possible = True

            if self.animation_possible:

                if event.key == pygame.K_RIGHT and not self.climbing:
                    self.x_change = 1
                    self.status = 'walk_right'
                if event.key == pygame.K_LEFT and not self.climbing:
                    self.x_change = -1
                    self.status = 'walk_left'

                if event.key == pygame.K_UP and middle_of_ladder:
                    if can_climb:
                        self.y_change = -1
                        self.x_change = 0
                        self.climbing = True
                        self.status = 'climbing'
                if event.key == pygame.K_DOWN and middle_of_ladder:
                    if climbed_down:
                        self.y_change = 1
                        self.x_change = 0
                        self.climbing = True
                        self.status = 'climbing'

        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_RIGHT:
                self.x_change = 0
                self.animation_possible = False
            if event.key == pygame.K_LEFT:
                self.x_change = 0
                self.animation_possible = False

            if event.key == pygame.K_UP:
                if can_climb:
                    self.y_change = 0
                    self.animation_possible = False
                if self.climbing and self.landed:
                    self.climbing = False
            if event.key == pygame.K_DOWN:
                if climbed_down:
                    self.y_change = 0
                    self.animation_possible = False
                if self.climbing and self.landed:
                    self.climbing = False

    def reset(self):
        self.rect.midbottom = (100, 150)
        self.status = 'walk_left'
        self.sleigh_completed = False

    def update(self):

        self.landed = False
        self.check_landed()
        self.check_wall_collision()
        self.animate()
        self.move()
        self.move_between_rooms()
        self.check_sleigh_collision()
        self.leave_sleigh()
