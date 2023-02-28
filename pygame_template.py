import pygame

WIDTH = 700
HEIGHT = 400
FPS = 60

BLACK = (0, 0, 0)
pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('test')
clock = pygame.time.Clock()

switch = True
while switch:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            switch = False
    display.fill(BLACK)
    pygame.display.flip()

pygame.quit()
