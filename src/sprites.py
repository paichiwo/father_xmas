from random import randint, choice
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
        self.speed = choice([20, 30, 40, 50])

    def update(self, dt):
        self.pos.y += self.speed * dt

        # Respawn at top when it falls below boundary
        if self.pos.y > self.boundary.bottom:
            self.pos.y = self.boundary.top
            self.pos.x = randint(self.boundary.left, self.boundary.right)

        # Ensure flakes stay within horizontal bounds
        self.pos.x = max(self.boundary.left, min(self.pos.x, self.boundary.right))

        self.rect.topleft = self.pos
