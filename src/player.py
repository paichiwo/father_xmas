import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, ladder_group, platform_group, group):
        super().__init__(group)

        # general setup
        self.image = pygame.Surface((16, 32))
        self.image.fill('green')
        self.rect = self.image.get_rect(midbottom=pos)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 100
        self.climbing = False

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

    def get_current_platform(self):
        for platform_name, y_pos in self.platforms_y_pos.items():
            if y_pos >= self.rect.bottom > y_pos - self.speed:
                self.current_platform = platform_name

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

    def fall_onto_platform(self):

        # check for the current platform
        self.get_current_platform()

        # fall onto the platform if not on a ladder
        self.direction.y = 1
        if self.rect.bottom >= self.platforms_y_pos[self.current_platform]:
            self.direction.y = 0
            self.rect.bottom = self.platforms_y_pos[self.current_platform]

    def input(self):
        keys = pygame.key.get_pressed()

        # reset vertical direction
        self.direction.y = 0

        # reset climbing
        self.climbing = False

        # check if on a ladder
        on_ladder = pygame.sprite.spritecollideany(self, self.ladder_group)

        # check if player can climb
        can_climb, climb_down, middle_of_ladder = self.check_climb()

        if not on_ladder:
            self.fall_onto_platform()

        # handle vertical movement
        elif keys[pygame.K_UP] and can_climb and middle_of_ladder:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] and climb_down and middle_of_ladder:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # handle horizontal movement
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
        print(self.current_platform)
