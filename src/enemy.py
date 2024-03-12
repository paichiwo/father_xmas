import random
from src.entity import Entity
import pygame


class EnemyElf(Entity):
    def __init__(self, pos, direction_x, screen, platformer, path, group):
        super().__init__(pos, screen, platformer, path, group)

        self.name = 'elf'

        self.direction.x = direction_x
        self.speed = 60
        self.random_number = random.choice([0])

        # timers
        self.direction_timer = random.randint(2000, 5000)  # Initial timer duration
        self.last_direction_change_time = pygame.time.get_ticks()

        self.off_screen_timer = random.randint(2000, 5000)  # Initial off-screen timer duration
        self.last_off_screen_time = pygame.time.get_ticks()

    def direction_change(self):
        self.status = 'right' if self.direction.x > 0 else 'left'

        can_climb, climb_down, middle_of_ladder = self.check_climb()
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_direction_change_time

        # horizontal
        if not self.climbing:
            if elapsed_time >= self.direction_timer and not self.climbing or self.pos.x > 450 or self.pos.x < -120:
                self.direction.x *= -1
                self.last_direction_change_time = current_time
                self.direction_timer = random.randint(2000, 5000)
                self.random_number = random.choice([0, 1])

        # vertical
        if can_climb and middle_of_ladder and self.random_number == 0:
            self.direction.y = -1
            self.direction.x = 0
            self.climbing = True
            self.status = 'climb'
        if climb_down and middle_of_ladder and self.random_number == 0:
            self.direction.y = 1
            self.direction.x = 0
            self.climbing = True
            self.status = 'climb'
        else:
            self.direction.y = 0
            if self.climbing and self.landed:
                self.climbing = False
                self.random_number = random.choice([0, 1])
                self.direction.x = 1

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
        self.direction_change()

        self.collisions()
