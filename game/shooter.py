import os
import random
import pygame

WIDTH = 400
HEIGHT = 600
FPS = 60

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('test')
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (80, 60))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = 30

        self.rect.center = (WIDTH / 2, HEIGHT - 50)
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speed_x = -5
        if keys[pygame.K_d]:
            self.speed_x = 5
        self.rect.x += self.speed_x

        if self.rect.right + 5 > WIDTH:
            self.rect.x -= 5

        if self.rect.left - 5 < 0:
            self.rect.x += 5


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 25))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = 5

    def update(self):
        self.rect.y -= self.speed_y
        if self.rect.bottom - 5 < 0:
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img, (30, 30))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.9 / 2)

        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(2, 4)
        self.speed_x = random.randrange(-1, 2)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.y = random.randrange(-100, -40)
            self.rect.x = random.randrange(WIDTH - self.rect.width)

            self.speed_y = random.randrange(1, 3)
            self.speed_x = random.randrange(-1, 2)


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

player_img = pygame.image.load(os.path.join(img_folder, 'playerShip2_blue.png')).convert()
mob_img = pygame.image.load(os.path.join(img_folder, 'meteorBrown_small1.png')).convert()
bullet_img = pygame.image.load(os.path.join(img_folder, 'laserBlue02.png')).convert()
background = pygame.image.load(os.path.join(img_folder, 'blue.png')).convert()

background_rect = background.get_rect()

for i in range(8):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)

player = Player()
all_sprites.add(player)

switch = True
while switch:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            switch = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    all_sprites.update()
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        switch = False

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for i in hits:
        mob = Mob()
        all_sprites.add(mob)
        mobs.add(mob)

    display.fill((0, 0, 0))
    display.blit(background, background_rect)
    all_sprites.draw(display)
    pygame.display.flip()

pygame.quit()
