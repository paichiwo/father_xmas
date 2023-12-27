import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, ladder_group, platform_group, group):
        super().__init__(group)

        # general setup
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.Surface((16, 32))
        self.image.fill('green')
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x_pos, self.y_pos)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 100
        self.climbing = False
        self.landed = False

        # platforms
        self.platform_group = platform_group
        self.platforms_y_pos = self.get_positions(platform_group, 'platform')
        self.current_platform = None

        # ladders
        self.ladder_group = ladder_group
        self.ladders_y_pos = self.get_positions(ladder_group, 'ladder')

    @staticmethod
    def get_positions(group, prefix):
        positions = {}
        for index, obj in enumerate(group):
            key = f'{prefix}_{index + 1}'
            positions[key] = obj.rect.top if prefix == 'platform' else obj.rect.bottom
        return positions

    def check_climb(self):
        can_climb = False
        climb_down = False
        middle_of_ladder = False

        under = pygame.rect.Rect((self.rect[0], self.rect[1] + self.rect.height), (self.rect[2], self.rect[3]))

        for ladder in self.ladder_group:
            if self.rect.colliderect(ladder.rect) and not can_climb:
                can_climb = True
                offset = 10
                middle_of_ladder = abs(self.rect.centerx - ladder.rect.centerx) <= offset

            if under.colliderect(ladder):
                climb_down = True

        self.climbing = can_climb and middle_of_ladder
        return can_climb, climb_down, middle_of_ladder

    def controls(self, event):

        can_climb, climbed_down, middle_of_ladder = self.check_climb()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction.x = -1
            if event.key == pygame.K_RIGHT:
                self.direction.x = 1
            if event.key == pygame.K_UP:
                self.direction.y = -1
            if event.key == pygame.K_DOWN:
                self.direction.y = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.direction.x = 0
            if event.key == pygame.K_RIGHT:
                self.direction.x = 0
            if event.key == pygame.K_UP:
                self.direction.y = 0
            if event.key == pygame.K_DOWN:
                self.direction.y = 0

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
        self.move(dt)
