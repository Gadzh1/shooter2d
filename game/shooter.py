import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 50)
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speed_x = -5
        if keys[pygame.K_d]:
            self.speed_x = 5
        self.rect.x += self.speed_x

        if self.rect.right + 5 > WIDTH:
            self.rect.x -= 5

        if self.rect.left - 5 < 0:
            self.rect.x += 5


WIDTH = 400
HEIGHT = 600
FPS = 60
BACKGROUND = (21, 7, 122)

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('test')
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

switch = True
while switch:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            switch = False

    all_sprites.update()

    display.fill(BACKGROUND)
    all_sprites.draw(display)
    pygame.display.flip()

pygame.quit()
