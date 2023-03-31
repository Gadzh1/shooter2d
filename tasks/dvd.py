import pygame
import random
from random import choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (25, HEIGHT / 2)
        self.is_right = True
        self.is_left = False
        self.is_down = False
        self.is_up = True

    def set_directions_x(self, left, right):
        self.is_left = left
        self.is_right = right

    def set_directions_y(self, up, down):
        self.is_up = up
        self.is_down = down

    def change_color(self, colors):
        # self.image.fill(colors[random.randint(0, 4)])
        self.image.fill(choice(COLORS))

    def update(self):
        if self.is_right:
            if self.rect.right + 5 > WIDTH:
                self.change_color(COLORS)
                self.set_directions_x(True, False)
                return
            self.rect.x += 5

        if self.is_left:
            if self.rect.left - 5 < 0:
                self.change_color(COLORS)
                self.set_directions_x(False, True)
                return
            self.rect.x -= 5

        if self.is_up:
            if self.rect.top - 5 < 0:
                self.change_color(COLORS)
                self.set_directions_y(False, True)
                return
            self.rect.y -= 5

        if self.is_down:
            if self.rect.bottom + 5 > HEIGHT:
                self.change_color(COLORS)
                self.set_directions_y(True, False)
                return
            self.rect.y += 5


WIDTH = 700
HEIGHT = 400
FPS = 60

BLACK = (0, 0, 0)
BLUE = (0, 100, 250)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
COLORS = (BLUE, RED, YELLOW, GREEN, WHITE)

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('test')
clock = pygame.time.Clock()
group_sprite = pygame.sprite.Group()
player = Player()
group_sprite.add(player)

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
