import pygame
from functions import load_image


class Monster(pygame.sprite.Sprite):
    monster_image = load_image('monster.png')

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Monster.monster_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        self.rect.y += scroll
        self.rect.x = self.rect.x + 2
        if self.rect.x > 500:
            self.rect.x = -150
        # если выходят за границу уничтожаются
        if self.rect.y > 900:
            self.kill()
