import random
import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, x_change, status, platformer, screen, group):
        super().__init__(group)

        self.x_pos = x_pos
        self.y_pos = y_pos
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
        self.rect = self.image.get_rect(midbottom=(self.x_pos, self.y_pos))

        # Movement attributes
        self.y_change = 0

        self.direction_change_timer = random.randint(2000, 5000)  # Initial timer duration
        self.last_direction_change_time = pygame.time.get_ticks()

        self.off_screen_timer = random.randint(2000, 5000)  # Initial off-screen timer duration
        self.last_off_screen_time = pygame.time.get_ticks()
        self.off_screen = False

        # create functionality what happens when off-screen
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
                enemy_hitbox = pygame.Rect(self.rect[0]+2, self.rect[1], self.rect[2], self.rect[3])
                if enemy_hitbox.colliderect(wall.rect):
                    self.x_change = -1

            elif self.x_change < 0:
                enemy_hitbox = pygame.Rect(self.rect[0]-2, self.rect[1], self.rect[2], self.rect[3])
                if enemy_hitbox.colliderect(wall.rect):
                    self.x_change = 1

            # pygame.draw.rect(self.screen, 'red', player_hitbox)

    def move(self):
        self.rect.x += self.x_change

    def move_off_screen(self):

        if self.rect.left < -16 or self.rect.right > 320:
            if not self.off_screen:
                self.off_screen = True
                self.last_off_screen_time = pygame.time.get_ticks()

            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.last_off_screen_time

            if elapsed_time >= self.off_screen_timer:
                self.off_screen = False
                self.last_off_screen_time = current_time
                self.off_screen_timer = random.randint(3000, 9000)

                if self.rect.left < -16:
                    self.x_change = 1
                elif self.rect.right > 360:
                    self.x_change = -1

                self.rect.x += self.x_change
        else:
            self.off_screen = False
        print(self.off_screen)

    def set_status(self):
        if self.x_change > 0:
            self.status = 'walk_right'
        else:
            self.status = 'walk_left'

    def update_direction_change_timer(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_direction_change_time

        if elapsed_time >= self.direction_change_timer:
            self.x_change *= -1

            self.last_direction_change_time = current_time
            self.direction_change_timer = random.randint(2000, 5000)

    def update(self):
        self.animate()
        self.check_wall_collision()
        self.move()
        self.move_off_screen()
        self.set_status()
        self.update_direction_change_timer()
        # print(self.status)
        # print(self.x_change)
