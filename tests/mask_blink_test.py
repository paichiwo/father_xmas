import sys
import pygame
import pygame._sdl2 as sdl2
from math import sin
from src.helpers import import_assets

WIDTH, HEIGHT = 320, 180
SCALE = 4

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, screen, group):
        super().__init__(group)
        self.screen = screen
        self.frames = import_assets('../assets/player')
        self.frame_index = 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 80

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def move(self, dt):
        keys = pygame.key.get_pressed()

        if self.direction.magnitude() > 0:
            self.direction = round(self.direction.normalize())

        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

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

    def update(self, dt):
        self.move(dt)
        self.collisions_with_screen()
        self.blink()

class Game:
    def __init__(self):
        self.width, self.height = 960, 480
        # Game setup
        self.clock = pygame.time.Clock()

        # Scaled window setup
        self.window = pygame.Window(size=(WIDTH * SCALE, HEIGHT * SCALE), title="MASK BLINK TEST")
        self.window.resizable = True
        self.renderer = sdl2.Renderer(self.window, vsync=True)
        self.renderer.logical_size = (WIDTH, HEIGHT)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.window.get_surface()
        self.clock = pygame.time.Clock()

        self.player_group = pygame.sprite.Group()
        self.player = Player(self.screen, self.player_group)

    def run(self):
        while True:
            self.screen.fill('black')
            self.renderer.clear()
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player_group.update(dt)
            self.player.blink()

            sdl2.Texture.from_surface(self.renderer, self.screen).draw()
            self.renderer.present()

if __name__ == '__main__':
    Game().run()
