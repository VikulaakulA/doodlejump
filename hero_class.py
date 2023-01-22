from settings import balls, monsters, borders, all_sprites, speed, gravity, screen

import pygame
from functions import load_image
from ball_class import Ball


class Hero(pygame.sprite.Sprite):
    hero_image = load_image('hero.png')
    hero2_image = load_image('hero2.png')

    def __init__(self, heroes, *group):
        super().__init__(heroes, *group)
        self.image = Hero.hero_image
        self.rect = self.image.get_rect()
        self.rect.x = 250
        self.rect.y = 450
        self.direction = 0
        self.points = 0
        self.is_dead = False

    def update(self):
        scroll = 0
        above_y = 0

        # выход за вертикальные границы
        if self.rect.x > 490:
            self.rect.x = 0
        elif self.rect.x < 0:
            self.rect.x = 490

        # горизонтальное движение
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
        elif keys[pygame.K_RIGHT]:
            self.rect.x += speed

        # падение персонажа
        self.direction += gravity
        above_y += self.direction

        # соприкосновение с блоками
        for brick in borders:
            if brick.rect.colliderect(self.rect.x, self.rect.y, 77, 76):
                # если персонаж выше блока и падает
                if self.rect.bottom < brick.rect.bottom:
                    if self.direction > 0:
                        self.rect.bottom = brick.rect.top
                        above_y = 0
                        # подпрыгивает
                        self.direction = -20

        # скроллинг блоков: если касается середины экрана
        if self.rect.top <= 450:
            # если в прыжке
            if self.direction < 0:
                scroll = -above_y

        # счёт и вывод очков
        if scroll > 0:
            self.points += scroll
        t = pygame.font.Font(None, 25)
        t = t.render(str(self.points), False, ('white'))
        screen.blit(t, (10, 10))

        # конец игры при падении персонажа
        if self.rect.bottom + above_y > 900:
            self.is_dead = True
            self.kill()

        # персонаж опускается на сколько превысил середину и опускается на сколько опускаются блоки
        self.rect.y += above_y + scroll
        for monster in monsters:
            if monster.rect.colliderect(self.rect.x, self.rect.y, 77, 76):
                self.is_dead = True
                self.kill()

        return scroll, self.points

    def balls(self):
        ball = Ball(self.rect.centerx, self.rect.top)
        balls.add(ball)
        all_sprites.add(ball)
