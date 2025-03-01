from src.config import *
from src.sprites import Sleigh
from src.helpers import import_assets


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, screen, platformer, path, group):
        super().__init__(group)

        self.screen = screen
        self.platformer = platformer

        self.frames = import_assets(path)
        self.frame_index = 1
        self.image = self.frames['walk'][self.frame_index]
        self.rect = self.image.get_rect(midbottom=pos)

        self.bottom_rect = pygame.rect.Rect()
        self.under_rect = pygame.rect.Rect()

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 120
        self.climbing = False
        self.landed = False

    def animate(self, dt):
        """Handles sprite animation based on movement."""
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.frames['walk']):
            self.frame_index = 0

        if self.direction.x == -1:
            self.image = self.frames['walk'][int(self.frame_index)]
        elif self.direction.x == 1:
            self.image = pygame.transform.flip(self.frames['walk'][int(self.frame_index)], True, False)
        elif self.direction.x == 0 and (self.direction.y in [-1, 1]):
            self.image = self.frames['climb'][int(self.frame_index)]

    def input(self):
        """Handles user input for movement and climbing."""
        can_climb_up, can_climb_down, middle_of_ladder = self.check_climb()
        keys = pygame.key.get_pressed()

        if self.climbing:
            self.direction.x = 0

        # horizontal
        if not self.climbing and self.landed:
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
            else:
                self.direction.x = 0

        # vertical
        if keys[pygame.K_UP] and can_climb_up and middle_of_ladder:
                self.direction.y = -1
                self.climbing = True
        elif keys[pygame.K_DOWN] and can_climb_down and middle_of_ladder:
                self.direction.y = 1
                self.climbing = True
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
        """Moves the player based on direction and speed."""
        # horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)

        # horizontal
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)

    def collisions_with_platforms(self):
        """Checks for collisions with platforms and adjusts position."""
        self.landed = False
        self.bottom_rect.update(self.rect.left, self.rect.bottom, self.rect.width, 3)

        for platform in self.platformer.platforms_group:
            if self.bottom_rect.colliderect(platform.rect):
                self.landed = True
                if not self.climbing:
                    self.direction.y = 0
                    self.rect.bottom = platform.rect.top
                    self.pos.y = self.rect.y

    def collisions_with_walls(self):
        """Checks for collisions with walls and prevents movement through them."""
        for wall in self.platformer.collision_walls:
            if self.rect.colliderect(wall.rect):
                if self.direction.x > 0:
                    self.rect.right = wall.rect.left
                else:
                    self.rect.left = wall.rect.right
                self.pos.x = self.rect.x

    def check_climb(self):
        """Determines whether the player can climb up or down a ladder."""
        can_climb_up = can_climb_down = middle_of_ladder = False
        self.under_rect.update(self.rect.centerx - self.rect.width // 6, self.rect.bottom,
                               self.rect.width // 3, self.rect.height // 3)
        offset = 3

        for ladder in self.platformer.ladders_group:
            # going up
            if self.rect.colliderect(ladder.rect):
                can_climb_up = True
                middle_of_ladder = abs(ladder.rect.centerx - self.under_rect.centerx) <= offset
            # going down
            if self.under_rect.colliderect(ladder.rect):
                can_climb_down = True
                middle_of_ladder = abs(ladder.rect.centerx - self.under_rect.centerx) <= offset

        if (not can_climb_up and (not can_climb_down or self.direction.y < 0)) or (
                self.landed and can_climb_up and self.direction.y > 0 and not can_climb_down):
            self.climbing = False

        return can_climb_up, can_climb_down, middle_of_ladder

    def move_between_rooms(self):
        """Handles transitioning the player between rooms."""
        for direction, (next_room, adjustment) in ROOM_TRANSITIONS[self.platformer.current_room].items():
            if (
                    (direction == 'left' and self.rect.left < -5) or
                    (direction == 'right' and self.rect.right > WIDTH + 5) or
                    (direction == 'up' and self.rect.top < -5) or
                    (direction == 'down' and self.rect.bottom > 149)
            ):

                self.platformer.current_room = next_room
                self.pos.x, self.pos.y = (adjustment, self.pos.y) if direction in ['left', 'right'] else (self.pos.x, adjustment)
                self.platformer.redraw_room()

    def collect_sleigh(self):
        """Checks if the player is in the correct room and collects the sleigh."""
        if self.platformer.current_room == self.platformer.random_room:
            for sleigh in self.platformer.sleigh_group:
                if self.rect.colliderect(sleigh.rect):
                    self.platformer.sleigh_in_inventory = True
                    sleigh.kill()

    def leave_sleigh(self):
        """Handles placing the sleigh in the designated area."""
        if self.platformer.current_room == 'room_1_2' and self.platformer.sleigh_in_inventory and self.rect.x == 100:
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
        """Resets the player to a starting position."""
        self.rect.midbottom = (100, 150)
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        """Updates the player state each frame."""
        self.input()
        self.move(dt)
        self.animate(dt)
        self.collisions_with_platforms()
        self.collisions_with_walls()
        self.move_between_rooms()
        self.collect_sleigh()
        self.leave_sleigh()
