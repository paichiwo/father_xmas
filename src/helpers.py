import pygame
import os

def import_assets(path):
    frames = {}

    for index, folder in enumerate(os.walk(path)):
        if index == 0:
            for name in folder[1]:
                frames[name] = []
        else:
            for file_name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                path = folder[0].replace('\\', '/') + '/' + file_name
                surf = pygame.image.load(path).convert_alpha()
                key = folder[0].split('\\')[1]
                frames[key].append(surf)
    return frames

def import_images(path):
    list_of_images = []

    for file in os.listdir(path):
        list_of_images.append(pygame.image.load(os.path.join(path, file)).convert_alpha())
    return list_of_images

def activate_state(states, new_state):
    for key in states.keys():
        states[key] = False
    states[new_state] = True