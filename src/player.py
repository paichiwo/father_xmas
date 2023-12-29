import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, screen, ladder_group, platform_group, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.screen = screen

        # Image & Rect
        self.image = pygame.Surface((16, 25))
        self.image.fill('green')
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x_pos, self.y_pos)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom, self.rect.width, 3)

        # Movement attributes
        self.speed = 1
        self.y_change = 0
        self.x_change = 0
        self.climbing = False
        self.landed = False

        # Platforms
        self.platform_group = platform_group
        self.platform_rects = [platform.rect for platform in self.platform_group]

        # Ladders
        self.ladder_group = ladder_group
        self.ladders_rects = [ladder.rect for ladder in self.ladder_group]

    def check_landed(self):
        for i in range(len(self.platform_rects)):
            if self.bottom.colliderect(self.platform_rects[i]):
                self.landed = True
                if not self.climbing:
                    if self.rect.bottom != self.platform_rects[i][1]:
                        self.y_change = 0
                    self.rect.bottom = self.platform_rects[i][1]

    def check_climb(self):
        can_climb = False
        climb_down = False

        under = pygame.rect.Rect((self.rect[0], self.rect[1] + self.rect.height),
                                 (self.rect[2], self.rect[3] / 3))
        # pygame.draw.rect(self.screen, 'yellow', under)

        for ladder in self.ladders_rects:
            if self.rect.colliderect(ladder) and not can_climb:
                can_climb = True
            if under.colliderect(ladder):
                climb_down = True

        if (not can_climb and (not climb_down or self.y_change < 0)) or (
                self.landed and can_climb and self.y_change > 0 and not climb_down):
            self.climbing = False

        return can_climb, climb_down

    def move(self):
        self.rect.move_ip(self.x_change * self.speed, self.y_change)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom, self.rect.width, 3)

    def controls(self, event, can_climb, climbed_down):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not self.climbing:
                self.x_change = 1
            if event.key == pygame.K_LEFT and not self.climbing:
                self.x_change = -1

            if event.key == pygame.K_UP:
                if can_climb:
                    self.y_change -= 1
                    self.x_change = 0
                    self.climbing = True
            if event.key == pygame.K_DOWN:
                if climbed_down:
                    self.y_change += 1
                    self.x_change = 0
                    self.climbing = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.x_change = 0
            if event.key == pygame.K_LEFT:
                self.x_change = 0
            if event.key == pygame.K_UP:
                if can_climb:
                    self.y_change = 0
                if self.climbing and self.landed:
                    self.climbing = False
            if event.key == pygame.K_DOWN:
                if climbed_down:
                    self.y_change = 0
                if self.climbing and self.landed:
                    self.climbing = False

    def update(self):
        self.landed = False
        self.check_landed()
        self.move()
        print(self.x_change, self.y_change)
        # pygame.draw.rect(self.screen, 'red', self.bottom)
