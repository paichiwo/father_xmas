from src.config import *
from src.helpers import activate_state

# add mouse functionality for options

class MainMenuScene:
    def __init__(self, screen, window):
        self.screen = screen
        self.window = window

        self.states = {
            'START': False,
            'MAIN MENU': True,
            'OPTIONS': False,
            'SCORES': False,
            'CREDITS': False
        }

        self.scenes = {
            'OPTIONS': OptionsScene(self.screen, self),
            'SCORES': ScoresScene(self.screen),
            'CREDITS': CreditsScene(self.screen)
        }

        self.menu_items = [key for key in self.states.keys() if key != 'MAIN MENU']
        self.menu_rects = {}
        self.current_option = 'START'
        self.button_held = False

    def draw_main_menu(self):
        self.menu_rects = {}

        for item in self.menu_items:
            color = DK_RED if item == self.current_option else WHITE
            text = FONT_8.render(item, False, color)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50 + self.menu_items.index(item) * 10))

            self.menu_rects[item] = rect # Store the rects for mouse detection
            self.screen.blit(text, rect)

    def input(self, event):
        if self.states['MAIN MENU']:
            # handle keyboard input
            if event.type == pygame.KEYDOWN and not self.button_held:
                self.button_held = True
                current_index = self.menu_items.index(self.current_option)

                if event.key == pygame.K_UP:
                    self.current_option = self.menu_items[(current_index - 1) % len(self.menu_items)]
                elif event.key == pygame.K_DOWN:
                    self.current_option = self.menu_items[(current_index + 1) % len(self.menu_items)]
                elif event.key == pygame.K_RETURN:
                    activate_state(self.states, self.current_option)

            elif event.type == pygame.KEYUP:
                self.button_held = False

            # handle mouse input
            elif event.type == pygame.MOUSEMOTION:
                for item, rect in self.menu_rects.items():
                    if rect.collidepoint(event.pos):
                        self.current_option = item

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.button_held:
                self.button_held = True
                for item, rect in self.menu_rects.items():
                    if rect.collidepoint(event.pos):
                        activate_state(self.states, item)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.button_held = False

    def reset(self):
        activate_state(self.states, 'MAIN MENU')

    def update(self, event):
        self.screen.fill('BLACK')

        if self.states['MAIN MENU']:
            self.draw_main_menu()
            self.input(event)
        else:
            for state, scene in self.scenes.items():
                if self.states[state]:
                    scene.update(event)
                    break

class OptionsScene:
    def __init__(self, screen, main_menu):
        self.screen = screen
        self.main = main_menu

        self.states = {
            'FULLSCREEN': False,
            'VOLUME': 50,
            'ACCEPT': False
        }

        self.options = {
            'FULLSCREEN': f"{'YES' if self.states['FULLSCREEN'] else 'NO'}",
            'VOLUME': str(self.states['VOLUME']),
            'ACCEPT': ''
        }

        self.menu_items = list(self.states.keys())
        self.menu_rects = {item: pygame.rect.Rect() for item in self.menu_items}
        self.current_option = 'FULLSCREEN'

        self.volume_items = ['outline', 'inner', 'minus', 'plus']
        self.volume_rects = {item: pygame.rect.Rect() for item in self.volume_items}

        self.button_held = False
        self.button_interaction_state = None
        self.button_interaction_time = 0

    def get_button_color(self, button_type):
        if self.button_interaction_state != button_type:
            return WHITE  # Default color for inactive buttons

        elapsed_time = pygame.time.get_ticks() - self.button_interaction_time
        duration = 100  # Effect duration in milliseconds

        if elapsed_time > duration:
            self.button_interaction_state = None
            return WHITE

        t = min(elapsed_time / duration, 1)
        return tuple(int(WHITE[i] * (1 - t) + DK_RED[i] * t) for i in range(3))

    def start_button_effect(self, button_type):
        self.button_interaction_state = button_type
        self.button_interaction_time = pygame.time.get_ticks()

    def draw_volume(self):
        # Volume inner rectangle (represents current volume level)
        volume_value_rect = pygame.rect.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 59, self.states['VOLUME'], 11)
        pygame.draw.rect(self.screen, DK_RED, volume_value_rect)

        # Volume outline rectangle
        volume_outline_rect = pygame.rect.Rect(WIDTH // 2 - 52, HEIGHT // 2 + 57, 104, 15)
        pygame.draw.rect(self.screen, WHITE, volume_outline_rect, 1)

        # Apply color effect to minus button
        minus_color = self.get_button_color('minus')
        minus_rect = pygame.rect.Rect(WIDTH // 2 - 69, HEIGHT // 2 + 57, 15, 15)
        pygame.draw.rect(self.screen, minus_color, minus_rect, 1)
        minus_text = FONT_8.render('<', False, minus_color)
        self.screen.blit(minus_text, minus_rect.move(3, 4))

        # Apply color effect to plus button
        plus_color = self.get_button_color('plus')
        plus_rect = pygame.rect.Rect(WIDTH // 2 + 54, HEIGHT // 2 + 57, 15, 15)
        pygame.draw.rect(self.screen, plus_color, plus_rect, 1)
        plus_text = FONT_8.render('>', False, plus_color)
        self.screen.blit(plus_text, plus_rect.move(4, 4))

        # Store rectangles for input detection
        self.volume_rects['outline'] = volume_outline_rect
        self.volume_rects['inner'] = volume_value_rect
        self.volume_rects['minus'] = minus_rect
        self.volume_rects['plus'] = plus_rect

    def draw_options_menu(self):
        self.menu_rects = {}
        self.draw_volume()

        for key, value in self.options.items():
            color = DK_RED if key == self.current_option and key != 'VOLUME' else WHITE
            text = FONT_8.render(f'{key}: {value}' if key != 'ACCEPT' else key, False, color)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50 + self.menu_items.index(key) * 15))

            if key == self.current_option and key == 'VOLUME':
                volume_outline_rect = pygame.rect.Rect(WIDTH // 2 - 52, HEIGHT // 2 + 57, 104, 15)
                pygame.draw.rect(self.screen, DK_RED, volume_outline_rect, 1)

            self.menu_rects[key] = rect # Store the rects for mouse detection
            self.screen.blit(text, rect)

    def input(self, event):
        # Handle keyboard
        if event.type == pygame.KEYDOWN and not self.button_held:
            self.button_held = True
            current_index = self.menu_items.index(self.current_option)

            if event.key == pygame.K_UP:
                self.current_option = self.menu_items[(current_index - 1) % len(self.menu_items)]

            if event.key == pygame.K_DOWN:
                self.current_option = self.menu_items[(current_index + 1) % len(self.menu_items)]

            if event.key == pygame.K_LEFT:
                if self.current_option == 'FULLSCREEN':
                    self.states['FULLSCREEN'] = not self.states['FULLSCREEN']
                    self.main.window.set_fullscreen(True) if self.states[
                        'FULLSCREEN'] else self.main.window.set_windowed()
                    self.options['FULLSCREEN'] = f"{'YES' if self.states['FULLSCREEN'] else 'NO'}"

                elif self.current_option == 'VOLUME':
                    self.states['VOLUME'] = max(0, self.states['VOLUME'] - 1)
                    self.options['VOLUME'] = str(self.states['VOLUME'])
                    self.start_button_effect('minus')  # Start color effect for minus button

            if event.key == pygame.K_RIGHT:
                if self.current_option == 'FULLSCREEN':
                    self.states['FULLSCREEN'] = not self.states['FULLSCREEN']
                    self.main.window.set_fullscreen(True) if self.states[
                        'FULLSCREEN'] else self.main.window.set_windowed()
                    self.options['FULLSCREEN'] = f"{'YES' if self.states['FULLSCREEN'] else 'NO'}"

                elif self.current_option == 'VOLUME':
                    self.states['VOLUME'] = min(100, self.states['VOLUME'] + 1)
                    self.options['VOLUME'] = str(self.states['VOLUME'])
                    self.start_button_effect('plus')  # Start color effect for plus button

            if event.key == pygame.K_RETURN:
                if self.current_option == 'ACCEPT':
                    self.main.reset()

        elif event.type == pygame.KEYUP:
            self.button_held = False

        # Handle mouse input for plus and minus buttons
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.button_held:
            self.button_held = True
            if self.volume_rects['minus'].collidepoint(event.pos):
                self.states['VOLUME'] = max(0, self.states['VOLUME'] - 1)
                self.options['VOLUME'] = str(self.states['VOLUME'])
                self.start_button_effect('minus')  # Start color effect for minus button

            elif self.volume_rects['plus'].collidepoint(event.pos):
                self.states['VOLUME'] = min(100, self.states['VOLUME'] + 1)
                self.options['VOLUME'] = str(self.states['VOLUME'])
                self.start_button_effect('plus')  # Start color effect for plus button

        elif event.type == pygame.MOUSEBUTTONUP:
            self.button_held = False

    def update(self, event):
        self.draw_options_menu()
        self.input(event)

class ScoresScene:
    def __init__(self, screen):
        self.screen = screen

    def update(self):
        text = FONT_8.render('SCORES', False, WHITE)
        rect = text.get_rect(center=(WIDTH // 2, 10))
        self.screen.blit(text, rect)

class CreditsScene:
    def __init__(self, screen):
        self.screen = screen

    def update(self):
        text = FONT_8.render('CREDITS', False, WHITE)
        rect = text.get_rect(center=(WIDTH // 2, 10))
        self.screen.blit(text, rect)

class GameOverScene:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):

        game_over_text = FONT_8.render("GAME OVER", True, WHITE)
        restart_text = FONT_8.render("Press 'R' TO RESTART", True, WHITE)

        game_over_rect = game_over_text.get_rect()
        restart_rect = restart_text.get_rect()

        game_over_rect.center = (WIDTH // 2, HEIGHT // 2)
        restart_rect.center = (WIDTH // 2, HEIGHT // 2 + 10)

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)