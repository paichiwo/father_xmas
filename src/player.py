import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, ladder_group, platform_group, group):
        super().__init__(group)

        # general setup
        self.image = pygame.Surface((32, 64))
        self.image.fill('green')
        self.rect = self.image.get_rect(midbottom=pos)

        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # platforms
        self.platform_group = platform_group
        self.platforms_y_pos = {}
        for index, platform in enumerate(self.platform_group):
            self.platforms_y_pos[f'platform_{index+1}'] = platform.rect.midtop[1]

        self.current_platform = None
        self.landed = False
        self.climbing = False

        # ladders
        self.ladder_group = ladder_group
        self.ladders_y_pos = {}
        for index, ladder in enumerate(self.ladder_group):
            self.ladders_y_pos[f'ladder_{index+1}'] = ladder.rect.midbottom[1]

    def get_current_platform(self):
        for platform_name, y_pos in self.platforms_y_pos.items():
            if y_pos >= self.rect.bottom > y_pos - self.speed:
                self.current_platform = platform_name

    def get_current_ladder(self):
        for ladder_name, y_pos in self.ladders_y_pos.items():
            if y_pos >= self.rect.bottom > y_pos - self.speed:
                self.current_ladder = ladder_name
                return

    def check_climb(self):
        can_climb = False
        climb_down = False
        under = pygame.rect.Rect((self.rect[0], self.rect[1] + self.rect.height),
                                 (self.rect[2], self.rect[3]))
        for lad in self.ladder_group:
            if self.rect.colliderect(lad.rect) and not can_climb:
                can_climb = True
            if under.colliderect(lad):
                climb_down = True
        if (not can_climb and (not climb_down or self.direction.y < 0)) or \
                (self.landed and can_climb and self.direction.y > 0 and not climb_down):
            self.climbing = False
        return can_climb, climb_down

    def input(self):
        keys = pygame.key.get_pressed()

        # reset vertical direction
        self.direction.y = 0
        self.climbing = False

        # check if on a ladder
        on_ladder = pygame.sprite.spritecollideany(self, self.ladder_group)
        self.get_current_platform()
        can_climb, climb_down = self.check_climb()

        if not on_ladder:

            # fall onto the platform if not on a ladder
            self.direction.y = 1
            if self.rect.bottom >= self.platforms_y_pos[self.current_platform]:
                self.direction.y = 0
                self.rect.bottom = self.platforms_y_pos[self.current_platform]
        else:
            self.climbing = can_climb
            # if on a ladder, allow climbing
            if keys[pygame.K_UP] and can_climb:
                self.direction.y = -1
                self.direction.x = 0
            elif keys[pygame.K_DOWN] and climb_down:
                self.direction.y = 1
                self.direction.x = 0
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
