from src.config import *
from src.helpers import import_assets

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, path, group):
        super().__init__(group)

        self.frames = import_assets(path)
        self.frame_index = 1
        self.image = self.frames['walk'][self.frame_index]
        self.rect = self.image.get_frect(midbottom=pos)

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 120

    def move(self, dt):
        """Moves the player based on direction and speed."""
        self.pos.x += self.direction.x * self.speed * dt
        self.pos.y += self.direction.y * self.speed * dt

        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

    def input(self):
        """Handles user input for movement and climbing."""
        keys = pygame.key.get_pressed()

        # horizontal
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def animate(self, dt):
        """Handles sprite animation based on movement."""
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.frames['walk']):
            self.frame_index = 0

        if self.direction.x == -1:
            self.image = self.frames['walk'][int(self.frame_index)]
        elif self.direction.x == 1:
            self.image = pygame.transform.flip(self.frames['walk'][int(self.frame_index)], True, False)
        elif self.direction.x == 0 and (self.direction.y in [-1, 1]):
            self.image = self.frames['climb'][int(self.frame_index)]

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
