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
    def __init__(self, x, y, btype='blue'):
        pygame.sprite.Sprite.__init__(self)

        if btype == 'blue':
            self.image = pygame.transform.scale(blue_bullet_img, (10, 25))
        elif btype == 'red':
            self.image = pygame.transform.scale(red_bullet_img, (15, 30))

        self.type = btype
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = 5

        self.damage = random.randrange(30, 51)

    def update(self):
        self.rect.y -= self.speed_y
        if self.rect.bottom - 5 < 0:
            self.kill()


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        rand_num = random.randrange(0, 3)

        self.image_orig = random.choice(meteor_images[rand_num])
        self.image_orig.set_colorkey((0, 0, 0))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.9 / 2)

        if rand_num == 0:
            self.hp = random.randrange(30, 71)
        elif rand_num == 1:
            self.hp = random.randrange(70, 101)
        elif rand_num == 2:
            self.hp = random.randrange(100, 151)

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

        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()
            add_mob()


def add_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


font_name = pygame.font.match_font('arial')


def draw_text(text, size, surf, x, y):
    font = pygame.font.Font(font_name, size)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect()
    text_rect.x = x
    text_rect.y = y
    surf.blit(text_surf, text_rect)


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')
snd_dir = os.path.join(game_folder, 'snd')

player_img = pygame.image.load(os.path.join(img_folder, 'playerShip2_blue.png')).convert()
blue_bullet_img = pygame.image.load(os.path.join(img_folder, 'laserBlue02.png')).convert()
red_bullet_img = pygame.image.load(os.path.join(img_folder, 'laserRed04.png')).convert()
background = pygame.image.load(os.path.join(img_folder, 'blue.png')).convert()

meteor_images = []
meteor_list = [('meteorBrown_small2.png',
                'meteorBrown_small1.png'),

               ('meteorBrown_med1.png',
                'meteorBrown_med3.png'),

               ('meteorBrown_big1.png',
                'meteorBrown_big3.png')]

shoot_sound_1 = pygame.mixer.Sound(os.path.join(snd_dir, 'Laser_Shoot.wav'))
shoot_sound_2 = pygame.mixer.Sound(os.path.join(snd_dir, 'Laser_Shoot3.wav'))
shoot_sound_3 = pygame.mixer.Sound(os.path.join(snd_dir, 'Laser_Shoot4.wav'))
hit = pygame.mixer.Sound(os.path.join(snd_dir, 'Hit_Hurt.wav'))

shoot_sounds = [shoot_sound_1,
                shoot_sound_2,
                shoot_sound_3]

pygame.mixer.music.load(os.path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

for img in meteor_list:
    temp = []
    for i in img:
        temp.append(pygame.image.load(os.path.join(img_folder, i)).convert())
    meteor_images.append(temp)

background_rect = background.get_rect()

for i in range(8):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)

player = Player()
all_sprites.add(player)

score = 0

pygame.mixer.music.play(loops=-1)

switch = True
while switch:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            switch = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                random.choice(shoot_sounds).play()
                all_sprites.add(bullet)
                bullets.add(bullet)

    all_sprites.update()
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        switch = False

    hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
    for i in hits:
        if hits[i][0].type == 'blue':
            i.hp -= hits[i][0].damage
            if i.hp <= 0:
                i.kill()
                add_mob()
                score += 50 - i.radius
                hit.play()
        elif hits[i][0].type == 'red':
            i.kill()
            add_mob()
            hit.play()

    display.fill((0, 0, 0))
    display.blit(background, background_rect)
    all_sprites.draw(display)

    draw_text(f'score: {score}', 30, display, 10, 0)

    pygame.display.flip()

pygame.quit()
