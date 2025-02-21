from src.config import *
from src.sprites import Sleigh
from src.helpers import import_assets


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, screen, platformer, path, group):
        super().__init__(group)

        # General setup
        self.screen = screen
        self.platformer = platformer

        # Image, Rect, Animation
        self.frames = import_assets(path)
        self.frame_index = 1

        self.image = self.frames['walk'][self.frame_index]
        self.rect = self.image.get_rect(midbottom=pos)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom, self.rect.width, 3)
        self.under = self.rect

        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 120

        self.climbing = False
        self.landed = False

        self.under = None

    def animate(self, dt):
            self.frame_index += 7 * dt
            if self.frame_index >= len(self.frames['walk']):
                self.frame_index = 0

    def input(self):
        can_climb_up, can_climb_down, middle_of_ladder = self.check_climb()
        keys = pygame.key.get_pressed()

        # horizontal
        if not self.climbing and self.landed:
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.image = self.frames['walk'][int(self.frame_index)]
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.image = pygame.transform.flip(self.frames['walk'][int(self.frame_index)], True, False)
            else:
                self.direction.x = 0

        # vertical
        if keys[pygame.K_UP] and can_climb_up and middle_of_ladder:
                self.direction.y = -1
                self.climbing = True
                self.image = self.frames['climb'][int(self.frame_index)]
        elif keys[pygame.K_DOWN] and can_climb_down and middle_of_ladder:
                self.direction.y = 1
                self.climbing = True
                self.image = self.frames['climb'][int(self.frame_index)]
        else:
            self.direction.y = 0
            if self.climbing and self.landed:
                self.climbing = False

        if not any((keys[pygame.K_RIGHT], keys[pygame.K_LEFT], keys[pygame.K_UP], keys[pygame.K_DOWN])):
            if self.direction.x == -1:
                self.image = self.frames['walk'][1]
            elif self.direction.x == 1:
                self.image = pygame.transform.flip(self.frames['walk'][1], True, False)

    def move(self, dt):
        if self.climbing:
            self.direction.x = 0

        # horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)

        # horizontal
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)

    def collisions(self):
        # platform collision
        self.landed = False
        for platform in self.platformer.platforms_group:
            if self.bottom.colliderect(platform.rect):
                self.landed = True
                if not self.climbing:
                    self.direction.y = 0
                    self.rect.bottom = platform.rect[1]

        # wall collision
        for wall in self.platformer.collision_walls:
            if self.rect.colliderect(wall.rect):
                if self.direction.x > 0:
                    self.rect.right = wall.rect.left
                else:
                    self.rect.left = wall.rect.right

                self.pos.x = self.rect[0]

        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom, self.rect.width, 3)

    def check_climb(self):
        can_climb_up = False
        can_climb_down = False
        middle_of_ladder = False

        self.under = pygame.rect.Rect(
            (self.rect.centerx - self.rect.width // 6, self.rect.bottom),
            (self.rect.width // 3, self.rect.height // 3)
        )
        pygame.draw.rect(self.screen, 'yellow', self.under)

        offset = 3

        for ladder in self.platformer.ladders_group:
            # going up
            if self.rect.colliderect(ladder.rect) and not can_climb_up:
                can_climb_up = True
                middle_of_ladder = abs(ladder.rect.centerx - self.under.centerx) <= offset

            # going down
            if self.under.colliderect(ladder.rect):
                can_climb_down = True
                middle_of_ladder = abs(ladder.rect.centerx - self.under.centerx) <= offset

        if (not can_climb_up and (not can_climb_down or self.direction.y < 0)) or (
                self.landed and can_climb_up and self.direction.y > 0 and not can_climb_down):
            self.climbing = False

        return can_climb_up, can_climb_down, middle_of_ladder

    def move_between_rooms(self):
        for direction, (next_room, adjustment) in ROOM_TRANSITIONS[self.platformer.current_room].items():
            if (direction == 'left' and self.rect.left < -5) or \
                    (direction == 'right' and self.rect.right > WIDTH + 5) or \
                    (direction == 'up' and self.rect.top < -5) or \
                    (direction == 'down' and self.rect.bottom > 149):

                self.platformer.current_room = next_room
                if direction in ['left', 'right']:
                    self.pos.x = adjustment
                else:
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

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.collisions()
        self.move_between_rooms()
        self.collect_sleigh()
        self.leave_sleigh()
