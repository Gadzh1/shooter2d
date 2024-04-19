import os
import random
import pygame

from constants import IMG_FOLDER, WIDTH, HEIGHT

zig_zag_max = 55

enemy_img = pygame.image.load(os.path.join(IMG_FOLDER, 'enemyRed1.png')).convert()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_x, speed_y, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (70, 50))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.hp = 100
        self.damage = 12
        self.size = 2
        self.radius = 20

        self.speed_x = speed_x
        self.speed_y = speed_y

        num = random.randint(1, 3)

        if num == 1:
            self.action = self.action_left_right
        elif num == 2:
            self.action = self.action_basic
        elif num == 3:
            self.action = self.action_zigzag

        self.x_direction = 1
        self.zigzag_count = zig_zag_max

        rand_num = random.randrange(50, WIDTH - 50, 20)

        self.rect.centerx = x
        self.rect.y = y

        # ----------------------

        self.pos = random.randrange(0, WIDTH - 70, 6)
        self.count = 30
        self.action_order = 1

        # ----------------------

    def update(self):

        self.action(self.speed_x, self.speed_y)

        if self.rect.y > HEIGHT:
            self.kill()

    def action_left_right(self, x, y):
        # global count, pos, action_order

        if self.action_order == 1:
            if self.count > 0:
                self.rect.y += y
                self.count -= 1
                return
            self.count = random.randint(2, 5)
            self.action_order += 1

        if self.action_order == 2:
            self.rect.x += x * self.x_direction

            if self.rect.right > WIDTH:
                self.x_direction = -1
                self.rect.right = WIDTH
                self.count -= 1
                return

            if self.rect.left < 0:
                self.x_direction = 1
                self.rect.left = 0
                self.count -= 1
                return

            if self.count == 0:
                self.action_order += 1
                return

        if self.action_order == 3:
            left_mid = self.pos - self.rect.width // 2 - 20
            right_mid = self.pos + self.rect.width // 2 + 20

            self.rect.x += x * self.x_direction

            if self.rect.left > left_mid and self.rect.right < right_mid:
                self.action_order += 1

        if self.action_order == 4:
            if self.rect.y < HEIGHT:
                self.rect.y += y
            else:
                self.kill()

    def action_basic(self, x, y):
        self.rect.x += x * self.x_direction
        self.rect.y += y

    def action_zigzag(self, x, y):
        if self.zigzag_count > 0:
            self.action_basic(x, y)
            self.zigzag_count -= 1
            return
        self.zigzag_count = zig_zag_max
        self.x_direction *= -1
        self.action_zigzag(x, y)
