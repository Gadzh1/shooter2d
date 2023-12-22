import os
import pygame

from constants import IMG_FOLDER
player_img = pygame.image.load(os.path.join(IMG_FOLDER, 'playerShip2_blue.png')).convert()


class Health(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (40, 20))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.image.set_colorkey((0, 0, 0))
