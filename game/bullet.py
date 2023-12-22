import os
import random
import pygame

from constants import WIDTH, HEIGHT, IMG_FOLDER

display = pygame.display.set_mode((WIDTH, HEIGHT))
blue_bullet_img = pygame.image.load(os.path.join(IMG_FOLDER, 'laserBlue02.png')).convert()
red_bullet_img = pygame.image.load(os.path.join(IMG_FOLDER, 'laserRed04.png')).convert()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, btype='blue'):
        pygame.sprite.Sprite.__init__(self)

        if btype == 'blue':
            self.image = pygame.transform.scale(blue_bullet_img, (10, 25))
        elif btype == 'red':
            self.image = pygame.transform.scale(red_bullet_img, (100, 600))
            self.now = pygame.time.get_ticks()

        self.type = btype
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = 5

        self.damage = random.randrange(30, 51)

    def update(self):
        if self.type == 'blue':
            self.rect.y -= self.speed_y
            if self.rect.bottom - 5 < 0:
                self.kill()
        elif self.type == 'red':
            if (pygame.time.get_ticks() - self.now) >= 1000:
                self.kill()
