import pygame

from src.config import *


class MainMenuScene:
    def __init__(self, screen):
        self.screen = screen

        self.states = {
            'START': False,
            'MAIN MENU': True,
            'OPTIONS': False,
            'SCORES': False,
            'CREDITS': False
        }

        self.scenes = {
            'OPTIONS': OptionsScene(self.screen),
            'SCORES': ScoresScene(self.screen),
            'CREDITS': CreditsScene(self.screen)
        }

        self.menu_items = [key for key in self.states.keys() if key != 'MAIN MENU']
        self.menu_rects = {}
        self.selected_option = 'START'

    def activate_state(self, state):
        for key in self.states.keys():
            self.states[key] = False
        self.states[state] = True

    def draw_main_menu(self):
        self.menu_rects = {}

        for item in self.menu_items:
            color = 'GREEN' if item == self.selected_option else 'WHITE'
            text = FONT_8.render(item, False, color)
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50 + self.menu_items.index(item) * 10))

            self.menu_rects[item] = rect # Store the rects for mouse detection
            self.screen.blit(text, rect)

    def input(self, event):
        if self.states['MAIN MENU']:
            if event.type == pygame.KEYDOWN:
                current_index = self.menu_items.index(self.selected_option)

                if event.key == pygame.K_UP:
                    self.selected_option = self.menu_items[(current_index - 1) % len(self.menu_items)]
                elif event.key == pygame.K_DOWN:
                    self.selected_option = self.menu_items[(current_index + 1) % len(self.menu_items)]
                elif event.key == pygame.K_RETURN:
                    self.activate_state(self.selected_option)

            elif event.type == pygame.MOUSEMOTION:
                for item, rect in self.menu_rects.items():
                    if rect.collidepoint(event.pos):
                        self.selected_option = item

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for item, rect in self.menu_rects.items():
                    if rect.collidepoint(event.pos):
                        self.activate_state(item)

    def reset(self):
        self.activate_state('MAIN MENU')

    def update(self):
        self.screen.fill('BLACK')

        if self.states['MAIN MENU']:
            self.draw_main_menu()
        else:
            for state, scene in self.scenes.items():
                if self.states[state]:
                    scene.update()
                    break

class OptionsScene:
    def __init__(self, screen):
        self.screen = screen

    def update(self):
        text = FONT_8.render('OPTIONS', False, 'WHITE')
        rect = text.get_rect(center=(WIDTH // 2, 10))
        self.screen.blit(text, rect)

class ScoresScene:
    def __init__(self, screen):
        self.screen = screen

    def update(self):
        text = FONT_8.render('SCORES', False, 'WHITE')
        rect = text.get_rect(center=(WIDTH // 2, 10))
        self.screen.blit(text, rect)

class CreditsScene:
    def __init__(self, screen):
        self.screen = screen

    def update(self):
        text = FONT_8.render('CREDITS', False, 'WHITE')
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