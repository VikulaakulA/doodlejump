import pygame

import os
import sys
from settings import size
pygame.init()

pygame.display.set_caption('DOODLE JUMP')
screen = pygame.display.set_mode(size)


# выход из игры
def terminate():
    pygame.quit()
    sys.exit()


# загрузка изображений + удаление фона
def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
