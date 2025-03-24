import sys
import pygame
from math import sin
from src.helpers import import_assets



pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, group):
        super().__init__(group)
        self.screen = screen
        self.scale = 4
        self.frames = import_assets('../assets/player')
        self.frame_index = 0
        self.state = 'idle'
        self.image = self.get_scaled_frame()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 5

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def get_scaled_frame(self):
        frame = self.frames[self.state][self.frame_index]
        return pygame.transform.scale(frame, (frame.get_width() * self.scale, frame.get_height() * self.scale))

    def move(self):
        keys = pygame.key.get_pressed()

        if self.direction.magnitude() > 0:
            self.direction = round(self.direction.normalize())

        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.pos += self.direction * self.speed
        self.rect.topleft = (self.pos.x, self.pos.y)

    def collisions_with_screen(self):
        self.rect.clamp_ip(pygame.Rect(0, 0, 960, 480))
        self.pos.update(self.rect.topleft)

    def blink(self):
        self.screen.blit(self.image, self.rect) # blit players image

        surf = self.mask.to_surface() # create surface from mask
        surf.set_colorkey((0, 0, 0))

        colored_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        colored_surf.fill('white')
        surf.blit(colored_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT) # blit color onto a mask

        value = (sin(pygame.time.get_ticks() / 100) + 1) / 2
        surf.set_alpha(int(value * 255)) # set mask alpha
        self.screen.blit(surf, self.rect.topleft) # blit mask

    def update(self):
        self.move()
        self.collisions_with_screen()
        self.blink()

class Game:
    def __init__(self):
        self.width, self.height = 960, 480
        self.screen = pygame.display.set_mode((self.width, self.height), vsync=True)
        pygame.display.set_caption('Mask tests')
        self.clock = pygame.time.Clock()

        self.player_group = pygame.sprite.Group()
        self.player = Player(self.screen, self.player_group)

    def run(self):
        while True:
            self.screen.fill('black')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            self.player_group.update()
            self.player.blink()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    Game().run()
