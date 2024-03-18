import os
import random
import pygame

from constants import IMG_FOLDER, WIDTH, HEIGHT

zig_zag_max = 55
count = 30
pos = random.randrange(0, WIDTH - 70, 6)

action_order = 1

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
        self.zigzag_count = zig_zag_max

        rand_num = random.randrange(50, WIDTH - 50, 20)

        self.rect.centerx = x
        self.rect.y = y

    def update(self):
        self.action_left_right(self.speed_x, self.speed_y)

        if self.rect.y > HEIGHT:
            self.kill()

    def action_left_right(self, x, y):
        global count, pos, action_order

        if action_order == 1:
            if count > 0:
                self.rect.y += y
                count -= 1
                return
            count = random.randint(5, 20)
            action_order += 1

        if action_order == 2:
            self.rect.x += x * self.x_direction

            if self.rect.right > WIDTH:
                self.x_direction = -1
                self.rect.right = WIDTH
                count -= 1
                return

            if self.rect.left < 0:
                self.x_direction = 1
                self.rect.left = 0
                count -= 1
                return

            if count == 0:
                action_order += 1
                return


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
    obj.zigzag_count = zig_zag_max
    obj.x_direction *= -1
    action_zigzag(obj, x, y)
