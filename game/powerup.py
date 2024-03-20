import pygame
import os

from constants import WIDTH, HEIGHT, IMG_FOLDER

powerup_images = {
    'shield': pygame.image.load(os.path.join(IMG_FOLDER, 'shield_gold.png')).convert(),
    'gun': pygame.image.load(os.path.join(IMG_FOLDER, 'bolt_gold.png')).convert()
}


class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(powerup_images[type], (25, 25))
        self.type = type
        self.x = x
        self.y = y
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = 5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom - 5 < 0:
            self.kill()
