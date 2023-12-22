import os
import pygame

from  constants import GAME_FOLDER

explosion_anim = {'lg': [], 'sm': []}

img_exp = os.path.join(GAME_FOLDER, 'img', 'exploation')

for i in range(9):
    filename = f'regularExplosion0{i}.png'
    png = pygame.image.load(os.path.join(img_exp, filename)).convert()
    png.set_colorkey((0, 0, 0))
    large = pygame.transform.scale(png, (100, 100))
    explosion_anim['lg'].append(large)
    small = pygame.transform.scale(png, (60, 60))
    explosion_anim['sm'].append(small)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size_name):
        pygame.sprite.Sprite.__init__(self)
        self.size_name = size_name
        self.image = explosion_anim[size_name][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()

        if now - self.last_update >= self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size_name]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size_name][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
