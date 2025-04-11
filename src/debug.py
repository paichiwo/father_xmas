import os
import psutil
import pygame.draw
from src.config import *
from src.helpers import activate_state

class DebugMenu:
    def __init__(self, screen, clock, level_1, states):
        """
        Initializes the debug menu.

        Args:
            screen (pygame.Surface): The game screen to draw the menu on.
            clock (pygame.time.Clock): The game clock to track FPS.
            level_1: The level manager handling player and enemy data.
            states (dict): Dictionary storing game states.
        """
        self.screen = screen
        self.level_1 = level_1
        self.states = states
        self.clock = clock

        self.surf = pygame.Surface((86, HEIGHT))
        self.surf.fill(BLACK)
        self.surf.set_alpha(200)
        self.rect = self.surf.get_rect(topright=(WIDTH, 0))

        self.debug_items = {
            'FPS': 0,
            'RAM': '0',
            'CPU': '0',
            'UNDER': False,
            'BOTTOM': False,
            'RECTS': False,
            'EPOS.X': '0',
            'EDIR.X': '0',
            'EDIR TIME': '0',
            'ECHOICE': 1,
            'ECLIMB': False,
            'ELANDED': True,
            'LEVEL': 1,
            'SLEIGH': False
        }

        self.item_positions = []
        self.mouse_button_held = False

    def draw_bg(self):
        """Draws the debug menu background."""
        self.screen.blit(self.surf, self.rect)

    def draw_title(self):
        """Draws the title of the debug menu."""
        title_text = FONT_DEBUG.render('DEBUG MENU', True, ORANGE)
        title_rect = title_text.get_rect(center=(WIDTH - self.surf.get_width() / 2, 10))
        self.screen.blit(title_text, title_rect)

    def draw_items(self):
        """Draws debug menu items and their current states."""
        mouse_pos = (pygame.mouse.get_pos()[0] // SCALE, pygame.mouse.get_pos()[1] // SCALE)
        self.item_positions.clear()

        self.draw_title()
        self.update_fps_ram_cpu()
        self.draw_under_rects()
        self.draw_bottom_rects()
        self.draw_rects()
        self.show_enemy_debug_stats()
        self.show_sleigh_in_inventory()

        padding = 3
        x_left = self.rect.left + padding
        x_right = self.rect.right - padding + 1
        y = 20

        for item, state in self.debug_items.items():
            item_color = 'ORANGE' if pygame.font.Font.render(FONT_8, item, True, YELLOW).get_rect(
                topleft=(x_left, y)).collidepoint(mouse_pos) else YELLOW
            state_color = RED if not state else GREEN

            item_text = FONT_DEBUG.render(item, True, item_color)
            item_rect = item_text.get_rect(topleft=(x_left, y))

            state_text = FONT_DEBUG.render(str(state), True, state_color)
            state_rect = state_text.get_rect(topright=(x_right, y))

            self.screen.blit(item_text, item_rect)
            self.screen.blit(state_text, state_rect)

            self.item_positions.append((item, item_rect))
            y += 10

    def update_fps_ram_cpu(self):
        """Updates the FPS value in the debug menu."""
        self.debug_items['FPS'] = int(self.clock.get_fps())
        process = psutil.Process(os.getpid())
        self.debug_items['RAM'] = f'{process.memory_info().rss / (1024 * 1024):.2f} MB'
        self.debug_items['CPU'] = f'{process.cpu_percent():.1f} %'

    def draw_under_rects(self):
        """Draws under_rects of the player and enemies"""
        if self.debug_items['UNDER']:
            pygame.draw.rect(self.screen, YELLOW, self.level_1.player.under_rect, 1)
            for enemy in self.level_1.enemy_group:
                pygame.draw.rect(self.screen, YELLOW, enemy.under_rect, 1)

    def draw_bottom_rects(self):
        """Draws player's and enemies bottom_rect"""
        if self.debug_items['BOTTOM']:
            pygame.draw.rect(self.screen, ORANGE, self.level_1.player.bottom_rect, 1)
            for enemy in self.level_1.enemy_group:
                pygame.draw.rect(self.screen, ORANGE, enemy.bottom_rect, 1)

    def draw_rects(self):
        """Draws player's and enemies rects"""
        if self.debug_items['RECTS']:
            pygame.draw.rect(self.screen, WHITE, self.level_1.player.rect, 1)
            for enemy in self.level_1.enemy_group:
                pygame.draw.rect(self.screen, WHITE, enemy.rect, 1)

    def show_enemy_debug_stats(self):
        """Shows info about enemies: pos.x, direction.x, direction_timer"""
        for enemy in self.level_1.enemy_group:
            self.debug_items['EDIR.X'] = 'LEFT' if enemy.direction.x < 0 else 'RIGHT'

            time_left = str(max(0, (enemy.last_direction_change_time + enemy.direction_timer - pygame.time.get_ticks())))
            self.debug_items['EDIR TIME'] = time_left

            if int(enemy.pos.x) in range(-enemy.off_screen_max, WIDTH + enemy.off_screen_max):
                self.debug_items['EPOS.X'] = round(enemy.pos.x)

            self.debug_items['ECHOICE'] = enemy.climb_decision
            self.debug_items['ECLIMB'] = enemy.climbing
            self.debug_items['ELANDED'] = enemy.landed

    def change_level(self):
        """Changes game levels"""
        if self.debug_items['LEVEL'] == 1:
            activate_state(self.states, 'level_2_running')
            self.debug_items['LEVEL'] = 2
        elif self.debug_items['LEVEL'] == 2:
            activate_state(self.states, 'level_1_running')
            self.debug_items['LEVEL'] = 1

    def show_sleigh_in_inventory(self):
        self.debug_items['SLEIGH'] = self.level_1.player.sleigh_in_inventory

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
        if item in ['UNDER', 'BOTTOM', 'RECTS']:
            self.debug_items[item] = not self.debug_items[item]
        elif item == 'LEVEL':
            self.change_level()

    def update(self, event):
        """Updates and renders the debug menu."""
        self.draw_bg()
        self.draw_items()
        self.handle_mouse_event(event)
