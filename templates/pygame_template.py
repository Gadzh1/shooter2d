import pygame
import os



WIDTH = 700
HEIGHT = 400
FPS = 60

BLACK = (0, 0, 0)
pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('test')
clock = pygame.time.Clock()
group_sprite = pygame.sprite.Group()

switch = True
while switch:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            switch = False

    group_sprite.update()

    display.fill(BLACK)
    group_sprite.draw(display)
    pygame.display.flip()

pygame.quit()
