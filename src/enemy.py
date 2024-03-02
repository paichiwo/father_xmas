import random
import pygame

from src.config import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, x_change, status, off_screen, platformer, screen, group):
        super().__init__(group)

        self.x_change = x_change
        self.status = status
        self.platformer = platformer
        self.screen = screen

        self.frames = {
            'walk_right':
                [pygame.transform.flip(pygame.image.load(f'assets/enemy/elf/walk/elf_walk_{i}.png').convert_alpha(),
                                       True, False) for i in range(1, 5)],
            'walk_left':
                [pygame.image.load(f'assets/enemy/elf/walk/elf_walk_{i}.png').convert_alpha() for i in range(1, 5)],
            'climbing':
                [pygame.image.load(f'assets/enemy/elf/climb/elf_climb_{i}.png').convert_alpha() for i in range(1, 5)]
        }

        self.frame_index = 0
        self.animation_possible = True

        self.image = self.frames[self.status][self.frame_index]
        self.rect = self.image.get_rect(midbottom=pos)

        # Movement attributes
        self.y_change = 0

        self.direction_change_timer = random.randint(2000, 10000)  # Initial timer duration
        self.last_direction_change_time = pygame.time.get_ticks()

        self.off_screen_timer = random.randint(2000, 5000)  # Initial off-screen timer duration
        self.last_off_screen_time = pygame.time.get_ticks()
        self.off_screen = off_screen

        self.climbing = False
        self.climbing_down = False
        self.landed = True

        self.random_number = random.choice([0])

        # make enemy climb ladders:
        # find all possible ladders in the room
        # find if enemy is on the bottom or top of the ladder
        # create player response when collided with player (flash player, steal a sleigh piece)

    def animate(self):
        if self.animation_possible:
            self.frame_index += 0.2
            if self.frame_index >= len(self.frames[self.status]):
                self.frame_index = 0
        else:
            self.frame_index = 1

        self.image = self.frames[self.status][int(self.frame_index)]

    def check_wall_collision(self):
        for wall in self.platformer.walls_with_collision_group:

            if self.x_change > 0:
                enemy_hitbox = pygame.Rect(self.rect[0] + 2, self.rect[1], self.rect[2], self.rect[3])
                if enemy_hitbox.colliderect(wall.rect):
                    self.x_change = -1

            elif self.x_change < 0:
                enemy_hitbox = pygame.Rect(self.rect[0] - 2, self.rect[1], self.rect[2], self.rect[3])
                if enemy_hitbox.colliderect(wall.rect):
                    self.x_change = 1

            # pygame.draw.rect(self.screen, 'red', player_hitbox)

    def check_climb(self):
        self.climbing = False
        self.climbing_down = False

        under = pygame.rect.Rect((self.rect[0], self.rect[1] + self.rect.height),
                                 (self.rect[2], self.rect[3]))
        pygame.draw.rect(self.screen, 'yellow', under)
        offset = 3

        for ladder in self.platformer.ladders_group:
            ladder_middle_x = ladder.rect.centerx
            enemy_middle_x = under.centerx
            middle_of_ladder = abs(enemy_middle_x - ladder_middle_x) <= offset
            if self.x_change != 0:
                if self.rect.colliderect(ladder.rect) and middle_of_ladder:
                    self.rect.centerx = ladder.rect.centerx
                    self.climbing = True
                    self.landed = False
                    self.y_change = 1

                if under.colliderect(ladder.rect) and middle_of_ladder:
                    self.climbing_down = True
                    self.y_change = 1

    def check_landed(self):

        under = pygame.rect.Rect((self.rect[0], self.rect[1] + self.rect.height),
                                 (self.rect[2], self.rect[3]//4))
        for platform in self.platformer.platforms_group:
            if under.colliderect(platform.rect):
                if self.rect.bottom == platform.rect.top:
                    self.landed = True

    def move(self):
        if self.climbing and self.random_number == 0:
            self.rect.y -= self.y_change

        self.rect.x += self.x_change

    def move_off_screen(self):

        if self.rect.right <= 0 or self.rect.left > WIDTH:
            if not self.off_screen:
                self.off_screen = True
                self.landed = True
                self.last_off_screen_time = pygame.time.get_ticks()

            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.last_off_screen_time

            if elapsed_time >= self.off_screen_timer:
                self.off_screen = False
                self.landed = True
                self.last_off_screen_time = current_time
                self.off_screen_timer = random.randint(2000, 5000)

                if self.rect.right <= 0:
                    self.x_change = 1
                elif self.rect.left >= WIDTH:
                    self.x_change = -1

        else:
            self.off_screen = False
            self.landed = True

    def set_status(self):
        self.status = 'walk_right' if self.x_change > 0 else 'walk_left'

    def update_direction_change_timer(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_direction_change_time

        if elapsed_time >= self.direction_change_timer and not self.climbing and not self.climbing_down:
            self.x_change *= -1
            self.random_number = random.choice([0])

            self.last_direction_change_time = current_time
            self.direction_change_timer = random.randint(2000, 10000)

    def update(self):
        self.check_landed()
        self.animate()
        self.move()
        self.move_off_screen()
        self.check_wall_collision()
        self.check_climb()
        self.set_status()
        self.update_direction_change_timer()
        print(self.landed)

