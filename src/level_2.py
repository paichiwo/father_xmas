from src.config import *


class LevelTwo:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.Surface((20, 20))
        pygame.draw.circle(self.image, 'blue', (self.image.get_width() // 2, self.image.get_height() // 2), 10)
        self.rect = self.image.get_rect()
        self.rect.topleft = (30, 30)

    def draw(self):
        self.screen.blit(self.image, self.rect)
        pygame.draw.rect(self.screen, 'red', self.rect, 1)

    def update(self):
        self.rect.x += 1
