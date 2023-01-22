import pygame

pygame.init()
size = width, height = 500, 900
screen = pygame.display.set_mode(size)

scores = []

balls = pygame.sprite.Group()
monsters = pygame.sprite.Group()
borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
heroes = pygame.sprite.Group()

clock = pygame.time.Clock()

fps = 60
speed = 10
scroll = 0
gravity = 1
brick_count = 10
monsters_count = 2