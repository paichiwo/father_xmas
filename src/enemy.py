import random
from src.helpers import import_assets
from src.config import *

class EnemyElf(pygame.sprite.Sprite):
    def __init__(self, screen, platformer, path, pos, direction_x, group):
        super().__init__(group)

        self.screen = screen
        self.platformer = platformer

        self.frames = import_assets(path)
        self.frame_index = 0
        self.image = self.frames['walk'][self.frame_index]
        self.rect = self.image.get_rect(midbottom=pos)
        self.bottom_rect = pygame.rect.Rect()
        self.under_rect = pygame.rect.Rect()

        self.direction = pygame.math.Vector2((direction_x, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        self.climbing = False
        self.landed = False
        self.collided_with_wall = False

        self.speed = 50
        self.off_screen_max = 100
        self.climb_decision = random.choice([0, 1]) # 0 = no climbing; 1 = climbing

        self.direction_timer = random.randint(2000, 5000)
        self.last_direction_change_time = pygame.time.get_ticks()
        self.off_screen_timer = random.randint(2000, 5000)
        self.last_off_screen_time = pygame.time.get_ticks()

    def animate(self, dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.frames['walk']):
            self.frame_index = 0

        if self.direction.x == -1:
            self.image = self.frames['walk'][int(self.frame_index)]
        elif self.direction.x == 1:
            self.image = pygame.transform.flip(self.frames['walk'][int(self.frame_index)], True, False)
        elif self.direction.x == 0 and (self.direction.y in [-1, 1]):
            self.image = self.frames['climb'][int(self.frame_index)]

    def move(self, dt):
        # horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)

        # vertical
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)

    def check_climb(self):
        can_climb_up, can_climb_down, middle_of_ladder = False, False, False
        self.under_rect.update(self.rect.centerx - self.rect.width // 6, self.rect.bottom,
                               self.rect.width // 3, self.rect.height // 3)
        offset = 1

        for ladder in self.platformer.ladders_group:
            # going up
            if self.rect.colliderect(ladder.rect) and not can_climb_up:
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

    def direction_change(self):
        can_climb_up, can_climb_down, middle_of_ladder = self.check_climb()
        elapsed_time = pygame.time.get_ticks() - self.last_direction_change_time

        # horizontal movement
        if not self.climbing:
            if self.landed and (elapsed_time >= self.direction_timer or self.collided_with_wall):
                self.direction.y = 0
                self.direction.x *= -1
                self.direction_timer = random.randint(2000, 5000)
                self.last_direction_change_time = pygame.time.get_ticks()
                self.climb_decision = 1

            elif not self.landed and (self.pos.x < -100 or self.pos.x > 420):
                self.direction.x *= -1
                self.direction_timer = random.randint(2000, 5000)
                self.last_direction_change_time = pygame.time.get_ticks()

        # vertical movement
        # GOING UP
        elif can_climb_up and middle_of_ladder and self.climb_decision == 1:
            if self.direction.y == 0:
                self.direction.y = -1
                self.direction.x = 0
                self.climbing = True
                self.climb_decision = random.choice([0, 0, 1])

        # GOING DOWN
        elif can_climb_down and middle_of_ladder and self.climb_decision == 1:
            if self.direction.y == 0:
                self.direction.y = 1
                self.direction.x = 0
                self.climbing = True
                self.climb_decision = random.choice([0, 0, 1])

        # GOING UP OR DOWN BUT LANDED ON THE PLATFORM
        else:
            if self.climbing and self.landed:
                self.direction.y = 0
                self.climbing = False
                self.direction.x = random.choice([-1, 1])

    def collisions_with_platforms(self):
        self.landed = False
        self.bottom_rect.update(self.rect.left, self.rect.bottom, self.rect.width, 3)

        for platform in self.platformer.platforms_group:
            if self.bottom_rect.colliderect(platform.rect):
                self.landed = True
                if not self.climbing:
                    self.direction.y = 0
                    self.rect.bottom = platform.rect.y
                break

    def collisions_with_walls(self):
        self.collided_with_wall = False
        for wall in self.platformer.collision_walls:
            if self.rect.colliderect(wall.rect):
                self.collided_with_wall = True

    def update(self, dt):
        self.animate(dt)
        self.move(dt)
        self.collisions_with_platforms()
        self.collisions_with_walls()
        self.direction_change()
