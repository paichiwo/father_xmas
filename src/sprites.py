from random import randint, choice, uniform
import math
import pygame

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

import pygame
from random import randint, uniform
import math

class Snowflake(Sprite):
    def __init__(self, pos, surf, boundary, group):
        super().__init__(pos, surf, group)

        self.boundary = boundary
        self.pos = pygame.Vector2(pos)
        self.base_x = self.pos.x  # Store initial X position for smooth oscillation

        self.speed = uniform(20, 30)
        self.drift_amplitude = uniform(5, 10)  # Slightly smaller to prevent extreme drift
        self.drift_frequency = uniform(0.3, 1.0)  # Lower frequency for smoother motion
        self.timer = 0

    def reset_speeds(self):
        """Reset speeds when the snowflake respawns at the top."""
        self.speed = uniform(20, 30)
        self.drift_amplitude = uniform(5, 10)  # Slightly smaller to prevent extreme drift
        self.drift_frequency = uniform(0.3, 1.0)  # Lower frequency for smoother motion
        self.timer = 0  # Reset drift phase to prevent erratic behavior

    def update(self, dt):
        """Updates snowflake position with smooth falling and drifting."""
        self.pos.y += self.speed * dt  # Fall downward
        self.timer += self.drift_frequency * dt  # Smooth oscillation update
        self.pos.x = self.base_x + math.sin(self.timer) * self.drift_amplitude  # Smooth left/right drift

        # Reset when it falls below the boundary
        if self.pos.y > self.boundary.bottom:
            self.pos.y = self.boundary.top - randint(5, 15)  # Start slightly above to avoid flickering
            self.base_x = randint(self.boundary.left, self.boundary.right)  # Random new X position
            self.reset_speeds()

        # Keep X within boundary limits
        self.pos.x = max(self.boundary.left, min(self.pos.x, self.boundary.right))

        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
