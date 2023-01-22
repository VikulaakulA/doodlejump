import pygame
from settings import all_sprites


class Border(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.Surface([500, 1])
        self.rect = pygame.Rect(0, 900, 500, 1)
