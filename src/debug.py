from src.config import *

class DebugMenu:
    def __init__(self, screen, clock, level_manager, states):
        self.screen = screen
        self.level = level_manager
        self.states = states
        self.clock = clock

        self.surf = pygame.Surface((86, HEIGHT))
        self.surf.fill('GREY')
        self.surf.set_alpha(200)
        self.rect = self.surf.get_rect(topright=(WIDTH, 0))

        self.debug_items = {
            'FPS': 0
        }

        self.item_positions = []

    def draw_bg(self):
        self.screen.blit(self.surf, self.rect)

    def draw_title(self):
        title_text = FONT_8.render('DEBUG MENU:', True, 'ORANGE')
        title_rect = title_text.get_rect(center=(WIDTH - self.surf.get_width() / 2, 15))
        self.screen.blit(title_text, title_rect)

    def draw_items(self):
        mouse_pos = (pygame.mouse.get_pos()[0] // SCALE, pygame.mouse.get_pos()[1] // SCALE)
        self.item_positions.clear()
        self.draw_title()

        self.update_fps()

        x = WIDTH - 57
        y = 30

        for item, state in self.debug_items.items():
            item_color = 'ORANGE' if pygame.font.Font.render(FONT_8, item, True, 'YELLOW').get_rect(
                center=(x, y)).collidepoint(mouse_pos) else 'YELLOW'
            state_color = 'RED' if not state else 'GREEN'

            item_text = FONT_8.render(item, True, item_color)
            state_text = FONT_8.render(str(state), True, state_color)

            item_rect = item_text.get_rect(center=(x, y))
            state_rect = state_text.get_rect(center=(x + 42, y))

            self.screen.blit(item_text, item_rect)
            self.screen.blit(state_text, state_rect)

            self.item_positions.append((item, item_rect))
            y += 10


    def update_fps(self):
        self.debug_items['FPS'] = int(self.clock.get_fps())

    def update(self):
        self.draw_bg()
        self.draw_items()


