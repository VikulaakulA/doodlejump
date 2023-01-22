import random
import pygame
import sqlite3

from functions import load_image, terminate
from settings import size, width, height, scores, balls, monsters, borders, all_sprites, heroes

from hero_class import Hero
from brick_class import Brick
from monster_class import Monster
from border_class import Border

clock = pygame.time.Clock()

fps = 60
speed = 10
scroll = 0
gravity = 1
brick_count = 10
monsters_count = 2

pygame.init()
pygame.display.set_caption('DOODLE JUMP')
screen = pygame.display.set_mode(size)

db = sqlite3.connect("score.db")
cursor = db.cursor()


# заставка
def start():
    fon = pygame.transform.scale(load_image('start.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return 1
        pygame.display.flip()
        clock.tick(fps)


def game():
    global scroll, points, brick
    scroll, points = 0, 0
    hero = Hero(all_sprites, heroes)
    Border()
    while True:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                hero.image = hero.hero2_image
                hero.balls()
            if event.type == pygame.MOUSEBUTTONUP:
                hero.image = hero.hero_image

        #если персонаж умер - показ очков
        if hero.is_dead:
            for i in borders:
                i.kill()
            for i in monsters:
                i.kill()
            return 2

        # создание первого блока
        if len(borders) == 0:
            brick = Brick(200, 850)
            borders.add(brick)
            all_sprites.add(brick)

        # создание остальных блоков, на расстоянии, чтобы допрыгнуть
        if len(borders) < brick_count:
            x = random.randint(0, 393)
            y = brick.rect.y - random.randint(80, 120)
            brick = Brick(x, y)
            borders.add(brick)
            all_sprites.add(brick)

        scroll, points = hero.update()

        # появление монстров
        if points > 2000 and len(monsters) == 0:
            monster = Monster(0, -500)
            monsters.add(monster)
            all_sprites.add(monster)
            borders.add(monster)

        balls.update()

        # умер ли монстр при столкновении с выстрелом
        dead_monsters = pygame.sprite.groupcollide(balls, monsters, True, True)
        for _ in dead_monsters:
            x = 0
            y = random.randint(-1500, -300)
            monster = Monster(x, y)
            monsters.add(monster)
            all_sprites.add(monster)
            borders.add(monster)

        borders.update(scroll)
        all_sprites.draw(screen)
        heroes.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


# конец игры и очки
def end(points):
    screen.fill('black')
    fon = pygame.transform.scale(load_image('score.png'), (width, height))
    screen.blit(fon, (0, 0))

    # показ очков
    if len(str(points)) == 1:
        x = 225
    elif len(str(points)) == 3:
        x = 200
    else:
        x = 180
    t = pygame.font.Font(None, 70)
    t = t.render(str(points), False, ('white'))
    screen.blit(t, (x, 550))

    # очки заносятся в базу данных
    cursor.execute(f"""INSERT INTO score VALUES (NULL, {points})""")
    db.commit()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                event.type == pygame.MOUSEBUTTONDOWN:
                return 3
        pygame.display.flip()
        clock.tick(fps)


# топ очков
def score():
    global score

    screen.fill('black')
    fon = pygame.transform.scale(screen, (width, height))
    screen.blit(fon, (0, 0))
    # наибольшие из набранных очков
    scores.append(cursor.execute(f"""SELECT score FROM score ORDER BY score DESC """).fetchall())
    db.commit()
    # показ топа очков
    t1 = pygame.font.Font(None, 50)
    t1 = t1.render('TOP SCORE:', False, ('white'))
    screen.blit(t1, (150,  30))
    for i, num in enumerate(scores[0][:10]):
        t2 = pygame.font.Font(None, 50)
        t2 = t2.render(str(num[0]), False, ('white'))
        screen.blit(t2, (220,  i * 60 + 120))
    scores.clear()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            # игра заново
            elif event.type == pygame.KEYDOWN or \
                event.type == pygame.MOUSEBUTTONDOWN:
                return 0
        pygame.display.flip()
        clock.tick(fps)

c = 0
while c != 4:
    if c == 0:
        c = start()
    elif c == 1:
        c = game()
    elif c == 2:
        c = end(points)
    elif c == 3:
        c = score()

db.close()
pygame.quit()
