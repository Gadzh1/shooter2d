import os
import random
import pygame
import time

from constants import IMG_FOLDER, WIDTH, HEIGHT

ZIG_ZAG_MAX = 55
COUNT = 30
POS = random.randrange(0, WIDTH - 70, 6)
IS_DOWN = True
IS_LEFT_RIGHT = False
IS_MIDDLE = False
IS_FALL_DOWN = False

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
        # self.action = action
        self.x_direction = 1
        self.zigzag_count = ZIG_ZAG_MAX

        rand_num = random.randrange(50, WIDTH - 50, 20)

        self.rect.centerx = x
        self.rect.y = y

    def update(self):
        self.action_left_right(self.speed_x, self.speed_y)

        if self.rect.y > HEIGHT:
            self.kill()

    def action_left_right(self, x, y):
        global COUNT
        global POS
        global IS_DOWN
        global IS_LEFT_RIGHT
        global IS_MIDDLE
        global IS_FALL_DOWN

        if IS_DOWN:
            if COUNT > 0:
                self.rect.y += y
                COUNT -= 1
                return
            COUNT = 2
            IS_DOWN = False
            IS_LEFT_RIGHT = True

        if IS_LEFT_RIGHT:
            if COUNT > 0:
                self.rect.x += x * self.x_direction

                # print('-------')
                # print(self.rect.left, self.rect.right)
                if self.rect.right > WIDTH:
                    self.x_direction = -1
                    self.rect.right = WIDTH
                    COUNT -= 1
                    # print('changed to', self.rect.right)
                elif self.rect.left < 0:
                    self.x_direction = 1
                    self.rect.left = 0
                    COUNT -= 1
                    # print('changed to', self.rect.left)

                return

            IS_LEFT_RIGHT = False
            IS_MIDDLE = True

    # if IS_MIDDLE:
    #     self.rect.x += x * self.x_direction
    #     left_mid = POS - self.rect.width // 2 - 20
    #     right_mid = POS + self.rect.width // 2 + 20
    #     print(POS, left_mid, right_mid)
    #
    #     if self.rect.left > left_mid and self.rect.right < right_mid:
    #         IS_MIDDLE = False
    #         IS_FALL_DOWN = True
    # print(self.rect.left, 0)

    # if IS_FALL_DOWN:
    #     if self.rect.y < HEIGHT:
    #         self.rect.y += y
    # else:
    #     self.kill()


def action_basic(obj, x, y):
    obj.rect.x += x * obj.x_direction
    obj.rect.y += y


def action_zigzag(obj, x, y):
    if obj.zigzag_count > 0:
        action_basic(obj, x, y)
        obj.zigzag_count -= 1
        return
    obj.zigzag_count = ZIG_ZAG_MAX
    obj.x_direction *= -1
    action_zigzag(obj, x, y)
