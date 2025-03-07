from src.config import *
from src.helpers import import_assets

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, level, path, group):
        super().__init__(group)
        self.level = level

        self.frames = import_assets(path)
        self.frame_index = 0
        self.image = self.frames['idle'][self.frame_index]
        self.rect = self.image.get_frect(midbottom=pos)
        self.animation_speed = 6

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.last_direction = 1
        self.speed = 120

        self.bottom_rect = pygame.rect.Rect()
        self.under_rect = pygame.rect.Rect()
        self.landed = False
        self.climbing = False

    def move(self, dt):
        """Moves the player based on direction and speed."""
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

    def input(self):
        """Handles user input for movement and climbing."""
        can_climb_up, can_climb_down = self.check_climb()
        keys = pygame.key.get_pressed()

        if self.climbing:
            self.direction.x = 0
        else:
            self.direction.y = 0

        # horizontal
        if not self.climbing and self.landed:
            self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]

        # update last direction
        if self.direction.x != 0:
            self.last_direction = self.direction.x

        # vertical
        if keys[pygame.K_UP] and can_climb_up:
            self.direction.y = -1
            self.climbing = True
        elif keys[pygame.K_DOWN] and can_climb_down:
            self.direction.y = 1
            self.climbing = True
        else:
            self.direction.y = 0
            if self.climbing and self.landed:
                self.climbing = False

    def animate(self, dt):
        """Handles sprite animation based on movement."""
        state = 'walk' if self.direction.x else 'climb' if self.direction.y else 'idle'

        if state != 'idle':
            self.frame_index = (self.frame_index + self.animation_speed * dt) % len(self.frames[state])
            self.image = self.frames[state][int(self.frame_index)]
        else:
            self.image = self.frames['idle'][0]

        if self.direction.x == 1 or (state == 'idle' and self.last_direction == 1):
            self.image = pygame.transform.flip(self.image, True, False)

    def animatea(self, dt):
        """Handles sprite animation based on movement."""
        if self.direction.x != 0:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.frames['walk']):
                self.frame_index = 0

            self.image = self.frames['walk'][int(self.frame_index)]
            if self.direction.x == 1:
                self.image = pygame.transform.flip(self.image, True, False)

        elif self.direction.y != 0:
            self.frame_index += self.animation_speed * dt
            if self.frame_index >= len(self.frames['climb']):
                self.frame_index = 0

            self.image = self.frames['climb'][int(self.frame_index)]

        else:  # Not moving -> use idle frame, but keep facing last direction
            self.image = self.frames['idle'][0]
            if self.last_direction == 1:
                self.image = pygame.transform.flip(self.image, True, False)

    def collisions_with_platforms(self):
        self.landed = False
        self.bottom_rect.update(self.rect.left - TILE_SIZE / 2, self.rect.bottom, self.rect.width + TILE_SIZE, 3)
        for platform in self.level.platforms_group:
            if self.bottom_rect.colliderect(platform.rect):
                self.landed = True
                if not self.climbing:
                    self.rect.bottom = platform.rect.top
                    self.pos.y = self.rect.y

    def collisions_with_walls(self):
        """Checks for collisions with walls and prevents movement through them."""
        for wall in self.level.collision_walls:
            if self.rect.colliderect(wall.rect):
                if self.direction.x > 0:
                    self.rect.right = wall.rect.left if self.direction.x > 0 else self.rect.left
                else:
                    self.rect.left = wall.rect.right
                self.pos.x = self.rect.x

    def check_climb(self):
        """Determines whether the player can climb up or down a ladder."""
        offset = 1
        can_climb_up = can_climb_down = middle_of_ladder = False
        self.under_rect.update(self.rect.centerx - self.rect.width // 6, self.rect.bottom,
                               self.rect.width // 3, self.rect.height // 3)

        for ladder in self.level.ladders_group:
            if self.rect.colliderect(ladder.rect):  # going up
                middle_of_ladder = abs(ladder.rect.centerx - self.under_rect.centerx) <= offset
                can_climb_up = True if middle_of_ladder else False
            if self.under_rect.colliderect(ladder.rect):   # going down
                middle_of_ladder = abs(ladder.rect.centerx - self.under_rect.centerx) <= offset
                can_climb_down = True if middle_of_ladder else False

        if (not can_climb_up and (not can_climb_down or self.direction.y < 0)) or (
                self.landed and can_climb_up and self.direction.y > 0 and not can_climb_down):
            self.climbing = False

        return can_climb_up, can_climb_down

    def move_between_rooms(self):
        """Handles transitioning the player between rooms."""
        for direction, (next_room, adjustment) in ROOM_TRANSITIONS[self.level.current_room_key].items():
            if (
                    (direction == 'left' and self.rect.left < -5) or
                    (direction == 'right' and self.rect.right > WIDTH + 5) or
                    (direction == 'up' and self.rect.top < -5) or
                    (direction == 'down' and self.rect.bottom > 149)
            ):
                self.pos.x, self.pos.y = (adjustment, self.pos.y) if direction in ['left', 'right'] else (self.pos.x, adjustment)
                self.level.change_room(next_room)

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.collisions_with_platforms()
        self.collisions_with_walls()
        self.move_between_rooms()
