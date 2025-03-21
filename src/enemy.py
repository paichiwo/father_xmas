from random import choice, randint
from src.helpers import import_assets
from src.config import *

class EnemyElf(pygame.sprite.Sprite):
    def __init__(self, pos, direction_x, screen, platformer, path, group):
        super().__init__(group)
        self.screen = screen
        self.platformer = platformer

        self.frames = import_assets(path)
        self.frame_index = 0
        self.image = self.frames['walk'][self.frame_index]
        self.animation_speed = 7

        self.rect = self.image.get_rect(midbottom=pos)
        self.bottom_rect = pygame.rect.Rect()
        self.under_rect = pygame.rect.Rect()

        self.direction = pygame.math.Vector2((direction_x, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.landed = False
        self.climbing = False
        self.collided_with_wall = False

        self.speed = 60
        self.off_screen_max = 100
        self.climb_decision = choice([0, 1]) # 0 = no climbing; 1 = climbing

        self.direction_timer = randint(2000, 5000)
        self.last_direction_change_time = pygame.time.get_ticks()

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

    def restart_direction_timers(self):
        self.direction_timer = randint(2000, 5000)
        self.last_direction_change_time = pygame.time.get_ticks()

    def direction_change(self):
        can_climb_up, can_climb_down = self.check_climb()
        elapsed_time = pygame.time.get_ticks() - self.last_direction_change_time

        # horizontal movement
        if self.collided_with_wall:
            self.direction.x *= -1

        if not self.climbing:
            self.direction.y = 0

        if not self.climbing and self.landed and elapsed_time >= self.direction_timer:
            self.direction.x *= -1
            self.restart_direction_timers()
            self.climb_decision = 1

        if not self.landed and (self.pos.x < -100 or self.pos.x > 420):
            self.direction.x *= -1
            self.restart_direction_timers()

        # vertical movement
        if can_climb_up and self.climb_decision == 1:
            if self.direction.y == 0:
                self.direction.y = -1
                self.direction.x = 0
                self.climbing = True
                self.climb_decision = choice([0, 0, 1])

        elif can_climb_down and self.climb_decision == 1:
            if self.direction.y == 0:
                self.direction.y = 1
                self.direction.x = 0
                self.climbing = True
                self.climb_decision = choice([0, 0, 1])

        # GOING UP OR DOWN BUT LANDED ON THE PLATFORM
        else:
            if self.climbing and self.landed:
                self.direction.y = 0
                self.climbing = False
                self.direction.x = choice([-1, 1])

    def animate(self, dt):
        state = 'walk' if self.direction.x else 'climb'

        self.frame_index = (self.frame_index + self.animation_speed * dt) % len(self.frames[state])
        self.image = self.frames[state][int(self.frame_index)]
        if self.direction.x == 1:
            self.image = pygame.transform.flip(self.image, True, False)

    def collisions_with_platforms(self):
        self.landed = False
        self.bottom_rect.update(self.rect.left - TILE_SIZE / 2, self.rect.bottom, self.rect.width + TILE_SIZE, 3)
        for platform in self.platformer.platforms_group:
            if self.bottom_rect.colliderect(platform.rect):
                self.landed = True
                if not self.climbing:
                    self.rect.bottom = platform.rect.top
                    self.pos.y = self.rect.y

    def collisions_with_walls(self):
        self.collided_with_wall = False
        for wall in self.platformer.collision_walls:
            if self.rect.colliderect(wall.rect):
                if self.direction.x > 0:
                    self.rect.right = wall.rect.left if self.direction.x > 0 else self.rect.left
                else:
                    self.rect.left = wall.rect.right
                self.pos.x = self.rect.x
                self.collided_with_wall = True

    def check_climb(self):
        """Determines whether the player can climb up or down a ladder."""
        offset = 2
        can_climb_up = can_climb_down = False
        self.under_rect.update(self.rect.centerx - self.rect.width // 6, self.rect.bottom,
                               self.rect.width // 3, self.rect.height // 3)

        for ladder in self.platformer.ladders_group:
            if self.rect.colliderect(ladder.rect):  # going up
                can_climb_up = abs(ladder.rect.centerx - self.under_rect.centerx) <= offset  # middle of ladder
            if self.under_rect.colliderect(ladder.rect):  # going down
                can_climb_down = abs(ladder.rect.centerx - self.under_rect.centerx) <= offset  # middle of ladder

        if (not can_climb_up and (not can_climb_down or self.direction.y < 0)) or (
                self.landed and can_climb_up and self.direction.y > 0 and not can_climb_down):
            self.climbing = False

        return can_climb_up, can_climb_down

    def update(self, dt):
        self.direction_change()
        self.move(dt)
        self.animate(dt)
        self.collisions_with_platforms()
        self.collisions_with_walls()
