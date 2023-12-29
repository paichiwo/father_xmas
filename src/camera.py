import pygame


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()

        self.half_window_width = self.display_surface.get_size()[0] // 2
        self.half_window_height = self.display_surface.get_size()[1] // 2

        # Camera offset
        self.offset = pygame.math.Vector2()

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_window_width
        self.offset.y = target.rect.centery - self.half_window_height

    def custom_draw(self, player):
        self.center_target_camera(player)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
