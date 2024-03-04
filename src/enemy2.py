import random
from src.entity import Entity
import pygame


class EnemyElf(Entity):
    def __init__(self, pos, direction_x, screen, platformer, path, group):
        super().__init__(pos, screen, platformer, path, group)

        self.speed = 60
        self.random_number = random.choice([0])

        # timers
        self.direction_change_timer = random.randint(2000, 10000)  # Initial timer duration
        self.last_direction_change_time = pygame.time.get_ticks()

        self.off_screen_timer = random.randint(2000, 5000)  # Initial off-screen timer duration
        self.last_off_screen_time = pygame.time.get_ticks()

        self.direction.x = direction_x

    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)

    def set_status(self):
        self.status = 'right' if self.direction.x > 0 else 'left'

    def collisions(self):
        # platform collision
        self.landed = False
        for i in range(len(self.platformer.platforms_group)):
            for platform in self.platformer.platforms_group:
                if self.bottom.colliderect(platform.rect):
                    self.landed = True
                    if not self.climbing:
                        self.direction.y = 0
                        self.rect.bottom = platform.rect[1]

        # wall collision
        for wall in self.platformer.collision_walls:
            hitbox = pygame.Rect(
                self.rect[0] + (2 if self.direction.x > 0 else -2), self.rect[1], self.rect[2], self.rect[3])

            if hitbox.colliderect(wall.rect):
                if self.direction.x > 0:
                    self.direction.x = -1
                else:
                    self.direction.x = 1

        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom, self.rect.width, 3)

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
        self.set_status()

        self.collisions()
