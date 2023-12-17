import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, platform_y_pos, group):
        super().__init__(group)

        self.platform_y_pos = platform_y_pos

        # general setup
        self.image = pygame.Surface((32, 64))
        self.image.fill('green')
        self.rect = self.image.get_rect(midbottom=pos)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def input(self):
        keys = pygame.key.get_pressed()

        # fall onto the platform
        self.direction.y = 1
        if self.rect.midbottom[1] >= self.platform_y_pos:
            self.direction.y = 0
            self.rect.bottom = self.platform_y_pos

        # directions
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, dt):

        # normalizing a vector (diagonal movement not faster than normal movement)
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.move(dt)
