from src.config import *
from src.helpers import import_assets
from src.sprites import Sleigh

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, screen, level_1, path, group):
        super().__init__(group)
        self.screen = screen
        self.level_1 = level_1

        self.frames = import_assets(path)
        self.frame_index = 0
        self.image = self.frames['idle'][self.frame_index]
        self.animation_speed = 6

        self.rect = self.image.get_frect(midbottom=pos)
        self.bottom_rect = pygame.rect.Rect()
        self.under_rect = pygame.rect.Rect()

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.last_direction = -1
        self.speed = 120
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
        elif self.climbing and self.direction.y == 0:
            self.image = self.frames['climb'][0]
        elif not self.climbing:
                self.image = self.frames['idle'][0]

        if self.direction.x == 1 or (state == 'idle' and self.last_direction == 1):
            self.image = pygame.transform.flip(self.image, True, False)

    def collisions_with_platforms(self):
        """Handles collision with platforms"""
        self.landed = False
        self.bottom_rect.update(self.rect.left - TILE_SIZE / 2, self.rect.bottom, self.rect.width + TILE_SIZE, 3)
        for platform in self.level_1.platforms_group:
            if self.bottom_rect.colliderect(platform.rect):
                self.landed = True
                if not self.climbing:
                    self.rect.bottom = platform.rect.top
                    self.pos.y = self.rect.y

    def collisions_with_walls(self):
        """Checks for collisions with walls and prevents movement through them."""
        for wall in self.level_1.collision_walls:
            if self.rect.colliderect(wall.rect):
                if self.direction.x > 0:
                    self.rect.right = wall.rect.left if self.direction.x > 0 else self.rect.left
                else:
                    self.rect.left = wall.rect.right
                self.pos.x = self.rect.x

    def check_climb(self):
        """Determines whether the player can climb up or down a ladder."""
        offset = 2
        can_climb_up = can_climb_down = False
        self.under_rect.update(self.rect.centerx - self.rect.width // 6, self.rect.bottom,
                               self.rect.width // 3, self.rect.height // 3)

        for ladder in self.level_1.ladders_group:
            if self.rect.colliderect(ladder.rect):  # going up
                can_climb_up = abs(ladder.rect.centerx - self.under_rect.centerx) <= offset # middle of ladder
            if self.under_rect.colliderect(ladder.rect):   # going down
                can_climb_down = abs(ladder.rect.centerx - self.under_rect.centerx) <= offset # middle of ladder

        cannot_climb = not can_climb_up and (not can_climb_down or self.direction.y < 0)
        stuck_on_ladder = self.landed and can_climb_up and self.direction.y > 0 and not can_climb_down

        if cannot_climb or stuck_on_ladder:
            self.climbing = False

        return can_climb_up, can_climb_down

    def move_between_rooms(self):
        """Handles transitioning the player between rooms."""
        for direction, (next_room, adjustment) in ROOM_TRANSITIONS[self.level_1.current_room_key].items():
            if (
                    (direction == 'left' and self.rect.left < -5) or
                    (direction == 'right' and self.rect.right > WIDTH + 5) or
                    (direction == 'up' and self.rect.top < -5) or
                    (direction == 'down' and self.rect.bottom > 149)
            ):
                self.pos.x, self.pos.y = (adjustment, self.pos.y) if direction in ['left', 'right'] else (self.pos.x, adjustment)
                self.level_1.change_room(next_room)

    def collect_sleigh(self):
        """Handles collecting sleigh mechanism"""
        if self.level_1.current_room_key == self.level_1.sleigh_spawn_room:
            for sleigh in self.level_1.sleigh_group:
                if self.rect.colliderect(sleigh.rect):
                    self.level_1.sleigh_in_inventory = True
                    sleigh.kill()

        elif self.level_1.current_room_key == 'room_1_2' and self.level_1.sleigh_in_inventory and self.rect.x == 100:
            index = len(self.level_1.completed_sleigh_pieces)
            if index < len(self.level_1.sleigh_images):
                pos = (TILE_SIZE * 7 - TILE_SIZE * index, TILE_SIZE * 8)
                Sleigh(pos, self.screen, self.level_1.sleigh_images[index], self.level_1.completed_sleigh_group)

                self.level_1.sleigh_in_inventory = False
                self.level_1.completed_sleigh_pieces.append(str(index + 1))
                self.level_1.sleigh_group.empty()
                self.level_1.create_sleigh()

                self.level_1.all_sleigh_completed = True if len(self.level_1.completed_sleigh_pieces) == 4 else False

    def reset(self):
        """Resets player's class"""
        self.rect.midbottom = (5 * TILE_SIZE, 7 * TILE_SIZE)
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        self.collisions_with_platforms()
        self.collisions_with_walls()
        self.move_between_rooms()
        self.collect_sleigh()
