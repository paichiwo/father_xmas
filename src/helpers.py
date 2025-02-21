import pygame
from os import walk

def import_assets(path):
    frames = {}

    for index, folder in enumerate(walk(path)):
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