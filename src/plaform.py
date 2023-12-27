import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, length, height, screen, group):
        super().__init__(group)

        # General setup
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.length = length
        self.height = height
        self.screen = screen

        # Image & Rect
        self.image = pygame.Surface((self.length, self.height))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))

        # Platform top surface
        self.platform_tops = self.get_top_line_surface()

    def get_top_line_surface(self):
        top_line_surface = pygame.rect.Rect((self.x_pos, self.y_pos), (self.length, 5))
        pygame.draw.rect(self.screen, 'orange', top_line_surface)
        return top_line_surface
