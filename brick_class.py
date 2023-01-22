import pygame
from functions import load_image
from settings import all_sprites


class Brick(pygame.sprite.Sprite):
    brick_image = load_image('brick.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = Brick.brick_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # опускание блоков
    def update(self, scroll):
        self.rect.y += scroll
        # вышелшие из экрана уничтожаются
        if self.rect.y > 900:
            self.kill()
