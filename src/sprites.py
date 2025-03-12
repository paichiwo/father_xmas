from random import randint, choice, uniform
from src.config import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)

        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)

class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, group):
        super().__init__(pos, frames[0], group)

        self.frames = frames
        self.frames_index = 0
        self.image = self.frames[self.frames_index]

    def animate(self, dt):
        self.frames_index += 9 * dt
        if self.frames_index >= len(self.frames):
            self.frames_index = 0

        self.image = self.frames[int(self.frames_index)]

    def update(self, dt):
        self.animate(dt)

class Sleigh(Sprite):
    def __init__(self, pos, screen, surf, group):
        super().__init__(pos, surf, group)

        self.screen = screen
        self.rect = self.image.get_rect(bottomleft=pos)

    def update(self):
        self.screen.blit(self.image, self.rect)

class Snowflake(Sprite):
    def __init__(self, pos, surf, boundary, group):
        super().__init__(pos, surf, group)

        self.boundary = boundary

        self.pos = pygame.Vector2(pos)
        self.speed = uniform(20, 30)
        self.drift_speed =uniform(-10, 10)

    def reset_speeds(self):
        self.speed = uniform(20, 50)
        self.drift_speed =uniform(-10, 10)

    def update(self, dt):
        self.pos.y += (self.speed * dt)
        self.pos.x += self.drift_speed * dt

        # Respawn at top when it falls below boundary
        if self.pos.y > self.boundary.bottom:
            self.pos.y = self.boundary.top
            self.pos.x = randint(self.boundary.left, self.boundary.right)
            self.reset_speeds()

        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
