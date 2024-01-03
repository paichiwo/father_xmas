import pygame
import random


class SnowFlake(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height, screen):
        super().__init__()

        self.window_width = window_width
        self.window_height = window_height
        self.screen = screen

        self.snowflake_size = 1
        self.color = 'grey'

        self.image = pygame.Surface((self.snowflake_size, self.snowflake_size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.snowflake_size, self.snowflake_size), self.snowflake_size)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.window_width)
        self.rect.y = random.randint(0, self.window_height)

        self.speed = random.randint(1, 2)

    def update(self):
        self.rect.y += self.speed

        # If a snowflake falls below the screen, reset its position to the top
        if self.rect.y > self.window_height:
            self.rect.x = random.randint(0, self.window_width)
            self.rect.y = 0


class Snow(pygame.sprite.Group):
    def __init__(self, window_width, window_height, screen):
        super().__init__()

        self.window_width = window_width
        self.window_height = window_height
        self.screen = screen

        self.snowflake_count = 50
        self.generate_initial_snowflakes()

    def generate_initial_snowflakes(self):
        for _ in range(self.snowflake_count):
            snowflake = SnowFlake(self.window_width, self.window_height, self.screen)
            self.add(snowflake)

    def update(self):
        for snowflake in self.sprites():
            snowflake.update()

