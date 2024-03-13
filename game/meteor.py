import os
import random
import pygame

from constants import WIDTH, IMG_FOLDER

meteor_images = []
meteor_list = [('meteorBrown_small2.png',
                'meteorBrown_small1.png'),

               ('meteorBrown_med1.png',
                'meteorBrown_med3.png'),

               ('meteorBrown_big1.png',
                'meteorBrown_big3.png')]

for img in meteor_list:
    temp = []
    for i in img:
        temp.append(pygame.image.load(os.path.join(IMG_FOLDER, i)).convert())
    meteor_images.append(temp)


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        rand_num = random.randrange(0, 3)
        self.size = rand_num

        self.image_orig = random.choice(meteor_images[rand_num])
        self.image_orig.set_colorkey((0, 0, 0))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.8 / 2)

        if rand_num == 0:
            self.hp = random.randrange(30, 71)
            self.damage = random.randrange(1, 3)
        elif rand_num == 1:
            self.hp = random.randrange(70, 101)
            self.damage = random.randrange(4, 6)
        elif rand_num == 2:
            self.hp = random.randrange(100, 151)
            self.damage = random.randrange(7, 9)

        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(2, 4)
        self.speed_x = random.randrange(-1, 2)

        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()

        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = self.image = pygame.transform.rotate(self.image_orig, self.rot)
            old_centre = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_centre

    def update(self):
        self.rotate()

        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
