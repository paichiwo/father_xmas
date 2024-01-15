import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, screen, ladder_group, platform_group, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.screen = screen

        # Image & Rect
        self.frames = {
            'walk_left':
                [pygame.transform.flip(pygame.image.load(f'assets/player/walk/santa_walk_{i}.png').convert_alpha(),
                                       True, False) for i in range(1, 5)],
            'walk_right':
                [pygame.image.load(f'assets/player/walk/santa_walk_{i}.png').convert_alpha() for i in range(1, 5)],
            'climbing':
                [pygame.image.load(f'assets/player/climb/santa_climb_{i}.png').convert_alpha() for i in range(1, 5)]
        }

        # Animation index
        self.status = 'walk_right'
        self.frame_index = 1
        self.animation_possible = False

        self.image = self.frames[self.status][self.frame_index]
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

    def animate(self):
        if self.animation_possible:
            self.frame_index += 0.1
            if self.frame_index >= len(self.frames[self.status]):
                self.frame_index = 0
        else:
            self.frame_index = 1

        self.image = self.frames[self.status][int(self.frame_index)]

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
        middle_of_ladder = False

        under = pygame.rect.Rect((self.rect[0], self.rect[1] + self.rect.height),
                                 (self.rect[2], self.rect[3] / 3))
        # pygame.draw.rect(self.screen, 'yellow', under)
        offset = 5

        for ladder in self.ladders_rects:
            if self.rect.colliderect(ladder) and not can_climb:
                can_climb = True
                ladder_middle_x = ladder.centerx
                player_middle_x = under.centerx
                middle_of_ladder = abs(player_middle_x - ladder_middle_x) <= offset

            if under.colliderect(ladder):
                climb_down = True
                ladder_middle_x = ladder.centerx
                player_middle_x = under.centerx
                middle_of_ladder = abs(player_middle_x - ladder_middle_x) <= offset

        if (not can_climb and (not climb_down or self.y_change < 0)) or (
                self.landed and can_climb and self.y_change > 0 and not climb_down):
            self.climbing = False

        return can_climb, climb_down, middle_of_ladder

    def move(self):
        self.rect.move_ip(self.x_change * self.speed, self.y_change)
        self.bottom = pygame.rect.Rect(self.rect.left, self.rect.bottom, self.rect.width, 3)

    def controls(self, event, can_climb, climbed_down, middle_of_ladder):
        self.animation_possible = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and not self.climbing:
                self.x_change = 1
                self.status = 'walk_right'
                self.animation_possible = True
            if event.key == pygame.K_LEFT and not self.climbing:
                self.x_change = -1
                self.status = 'walk_left'
                self.animation_possible = True
            if event.key == pygame.K_UP and middle_of_ladder:
                if can_climb:
                    self.y_change = -1
                    self.x_change = 0
                    self.climbing = True
                    self.status = 'climbing'
            if event.key == pygame.K_DOWN and middle_of_ladder:
                if climbed_down:
                    self.y_change = 1
                    self.x_change = 0
                    self.climbing = True
                    self.status = 'climbing'

        elif event.type == pygame.KEYUP:
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

    def reset(self):
        self.rect.midbottom = (100, 150)
        self.status = 'walk_right'

    def update(self):
        self.landed = False
        self.check_landed()
        self.animate()
        self.move()
        # pygame.draw.rect(self.screen, 'red', self.bottom)
