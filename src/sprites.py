import random
import pygame
from src.config import WHITE


class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)

        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class AnimatedSprite(SimpleSprite):
    def __init__(self, pos, surf, group):
        super().__init__(pos, surf[0], group)

        self.frames = surf
        self.frames_index = 0
        self.image = self.frames[self.frames_index]

    def animate(self):
        self.frames_index += 0.2
        if self.frames_index >= len(self.frames):
            self.frames_index = 0

        self.image = self.frames[int(self.frames_index)]

    def update(self):
        self.animate()


class Sleigh(SimpleSprite):
    def __init__(self, pos, screen, surf, group):
        super().__init__(pos, surf, group)

        self.screen = screen
        self.rect = self.image.get_rect(bottomleft=pos)

    def update(self):
        self.screen.blit(self.image, self.rect)


class Snowflake:
    def __init__(self, x, y, screen, snow_boundary):
        self.pos = pygame.Vector2(x, y)
        self.screen = screen
        self.snow_boundary = snow_boundary
        self.size = random.randint(1, 2)
        self.speed = random.choice([0.4, 0.6, 0.8, 1])

    def draw(self):
        pygame.draw.circle(self.screen, WHITE, (int(self.pos.x), int(self.pos.y)), self.size)

    def update(self):
        self.pos.y += self.speed
        if self.pos.y > self.snow_boundary.bottom:
            self.pos.y = self.snow_boundary.top
        if self.pos.x < self.snow_boundary.left or self.pos.x > self.snow_boundary.right:
            self.pos.x = random.randint(self.snow_boundary.left, self.snow_boundary.right)
