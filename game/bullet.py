import os
import pygame
import random

WIDTH = 400
HEIGHT = 600

display = pygame.display.set_mode((WIDTH, HEIGHT))
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
blue_bullet_img = pygame.image.load(os.path.join(img_folder, 'laserBlue02.png')).convert()
red_bullet_img = pygame.image.load(os.path.join(img_folder, 'laserRed04.png')).convert()


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


def create_bullet(btype, player, shoot_sounds, all_sprites, bullets):
    bullet = Bullet(player.rect.centerx, player.rect.top, btype)
    random.choice(shoot_sounds).play()
    all_sprites.add(bullet)
    bullets.add(bullet)
