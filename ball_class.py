import pygame
from settings import all_sprites


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.Surface((10, 20))
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        # выходят за верхнюю границу - уничтожаются
        if self.rect.y < 0:
            self.kill()