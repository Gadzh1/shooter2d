import os
import pygame

from constants import WIDTH, HEIGHT, IMG_FOLDER

player_img = pygame.image.load(os.path.join(IMG_FOLDER, 'playerShip2_blue.png')).convert()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70, 50))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = 30
        self.health = 12

        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

        self.rect.center = (WIDTH / 2, HEIGHT - 50)
        self.speed_x = 0

    def update(self):
        global score
        self.speed_x = 0
        keys_state = pygame.key.get_pressed()
        if keys_state[pygame.K_a]:
            self.speed_x = -5
        if keys_state[pygame.K_d]:
            self.speed_x = 5
        self.rect.x += self.speed_x

        if self.rect.right + 5 > WIDTH:
            self.rect.x -= 5

        if self.rect.left - 5 < 0:
            self.rect.x += 5
