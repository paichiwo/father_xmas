import pygame

from src.config import *

class DebugMenu:
    def __init__(self, screen, clock, level_manager, states):
        """
        Initializes the debug menu.

        Args:
            screen (pygame.Surface): The game screen to draw the menu on.
            clock (pygame.time.Clock): The game clock to track FPS.
            level_manager: The level manager handling player and enemy data.
            states (dict): Dictionary storing game states.
        """
        self.screen = screen
        self.level = level_manager
        self.states = states
        self.clock = clock

        self.surf = pygame.Surface((86, HEIGHT))
        self.surf.fill('BLACK')
        self.surf.set_alpha(200)
        self.rect = self.surf.get_rect(topright=(WIDTH, 0))

        self.debug_items = {
            'FPS': 0,
            'UNDER': False,
            'BOTTOM': False
        }

        self.item_positions = []
        self.mouse_button_held = False

    def draw_bg(self):
        """Draws the debug menu background."""
        self.screen.blit(self.surf, self.rect)

    def draw_title(self):
        """Draws the title of the debug menu."""
        title_text = FONT_DEBUG.render('DEBUG MENU', True, 'ORANGE')
        title_rect = title_text.get_rect(center=(WIDTH - self.surf.get_width() / 2, 15))
        self.screen.blit(title_text, title_rect)

    def draw_items(self):
        """Draws debug menu items and their current states."""
        mouse_pos = (pygame.mouse.get_pos()[0] // SCALE, pygame.mouse.get_pos()[1] // SCALE)
        self.item_positions.clear()

        self.draw_title()
        self.update_fps()
        self.draw_under_rects()
        self.draw_bottom_rects()

        padding = 3
        x_left = self.rect.left + padding
        x_right = self.rect.right - padding
        y = 30

        for item, state in self.debug_items.items():
            item_color = 'ORANGE' if pygame.font.Font.render(FONT_8, item, True, 'YELLOW').get_rect(
                topleft=(x_left, y)).collidepoint(mouse_pos) else 'YELLOW'
            state_color = 'RED' if not state else 'GREEN'

            item_text = FONT_DEBUG.render(item, True, item_color)
            item_rect = item_text.get_rect(topleft=(x_left, y))

            state_text = FONT_DEBUG.render(str(state), True, state_color)
            state_rect = state_text.get_rect(topright=(x_right, y))

            self.screen.blit(item_text, item_rect)
            self.screen.blit(state_text, state_rect)

            self.item_positions.append((item, item_rect))
            y += 10

    def update_fps(self):
        """Updates the FPS value in the debug menu."""
        self.debug_items['FPS'] = int(self.clock.get_fps())

    def draw_under_rects(self):
        """Draws under_rects of the player and enemies"""
        if self.debug_items['UNDER']:
            pygame.draw.rect(self.screen, 'YELLOW', self.level.player.under_rect, 1)
            for enemy in self.level.enemy_group:
                pygame.draw.rect(self.screen, 'YELLOW', enemy.under_rect, 1)

    def draw_bottom_rects(self):
        """Draws bottom_rects of the player and enemies"""
        if self.debug_items['BOTTOM']:
            pygame.draw.rect(self.screen, 'ORANGE', self.level.player.bottom_rect, 1)
            for enemy in self.level.enemy_group:
                pygame.draw.rect(self.screen, 'ORANGE', enemy.bottom_rect, 1)

    def handle_mouse_event(self, event):
        """Handles mouse input for toggling debug options."""
        if event.type == pygame.MOUSEBUTTONDOWN and not self.mouse_button_held:
            self.mouse_button_held = True
            for item, item_rect in self.item_positions:
                if item_rect.collidepoint(event.pos):
                    self.toggle_item(item)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_button_held = False

    def toggle_item(self, item: str):
        """Toggles the state of a debug item."""
        if item == 'UNDER':
            self.debug_items[item] = not self.debug_items[item]
        elif item == 'BOTTOM':
            self.debug_items[item] = not self.debug_items[item]

    def update(self, event):
        """Updates and renders the debug menu."""
        self.draw_bg()
        self.draw_items()
        self.handle_mouse_event(event)

