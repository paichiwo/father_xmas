import random
import pygame
from src.helpers import import_assets

# create debug menu
class EnemyElf(pygame.sprite.Sprite):
    def __init__(self, pos, direction_x, screen, platformer, path, group):
        super().__init__(pos, screen, platformer, path, group)

        self.screen = screen
        self.platformer = platformer

        # Image, Rect, Animation
        self.frames = import_assets(path)
        self.frame_index = 1
        self.status = 'left'

        self.image = self.frames[self.status][self.frame_index]
        self.rect = self.image.get_rect(midbottom=pos)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom, self.rect.width, 3)
        self.under = self.rect

        # Movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 120

        self.climbing = False
        self.landed = False



        self.direction.x = direction_x
        self.speed = 50
        self.random_number = random.choice([0, 1])

        # timers
        self.direction_timer = random.randint(2000, 5000)
        self.last_direction_change_time = pygame.time.get_ticks()

        self.off_screen_timer = random.randint(2000, 5000)
        self.last_off_screen_time = pygame.time.get_ticks()

    def animate(self, dt):
            self.frame_index += 7 * dt
            if self.frame_index >= len(self.frames[self.status]):
                self.frame_index = 0

    def move(self, dt):
        if self.climbing:
            self.direction.x = 0

        # horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)

        # horizontal
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.y = round(self.pos.y)

        # pygame.draw.rect(self.screen, 'orange', self.bottom)

    def direction_change(self):
        can_climb_up, can_climb_down, middle_of_ladder = self.check_climb()
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_direction_change_time

        # horizontal
        if not self.climbing and self.landed:
            self.status = 'right' if self.direction.x > 0 else 'left'

            if elapsed_time >= self.direction_timer or self.pos.x > 450 or self.pos.x < -120:
                self.direction.y = 0
                self.direction.x *= -1
                self.random_number = 0
                self.last_direction_change_time = current_time
                self.direction_timer = random.randint(2000, 5000)
                # self.random_number = random.choice([0, 1])

        # vertical
        if can_climb_up and middle_of_ladder and self.random_number == 0:
            print('can climb up')
            if self.direction.y == 0:  # Not already climbing
                self.direction.y = -1  # Climb up
                self.direction.x = 0
                self.climbing = True
                self.status = 'climb'
                self.random_number = random.choice([0, 1, 1])

        elif can_climb_down and middle_of_ladder and self.random_number == 0:
            print('can climb down')
            if self.direction.y == 0:  # Not already climbing
                self.direction.y = 1  # Climb down
                self.direction.x = 0
                self.climbing = True
                self.status = 'climb'
                self.random_number = random.choice([0, 1])

        else:
            if self.climbing and self.landed:
                self.direction.y = 0
                self.climbing = False
                self.direction.x = self.random_number
                self.random_number = random.choice([-1, 1])
                # self.direction.x = 1 if self.direction.x == -1 else -1

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
                    self.direction.x = -1
                else:
                    self.direction.x = 1

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

        offset = 1

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

    def update(self, dt):
        if self.status == 'right' or self.status == 'left':
            self.image = self.frames[self.status][int(self.frame_index)]
        elif self.status == 'climb':
            self.image = self.frames['climb'][int(self.frame_index)]

        self.move(dt)
        self.animate(dt)
        self.direction_change()
        self.collisions()

