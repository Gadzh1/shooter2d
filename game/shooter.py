import os
import random
import pygame

WIDTH = 400
HEIGHT = 600
FPS = 60
LASER_PRICE = 5

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('test')
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (70, 50))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = 30
        self.shield = 12

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
        if keys_state[pygame.K_s]:
            self.shoot()
        if keys_state[pygame.K_w]:
            if score >= LASER_PRICE:
                score -= LASER_PRICE
                create_bullet('red')

        if self.rect.right + 5 > WIDTH:
            self.rect.x -= 5

        if self.rect.left - 5 < 0:
            self.rect.x += 5

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            create_bullet('blue')

        # if event.key == pygame.K_w:
        #     if score >= LASER_PRICE:
        #         score -= LASER_PRICE
        #         create_bullet('red')
        #
        # else:
        #     if event.key == pygame.K_s:
        #         create_bullet('blue')


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


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        rand_num = random.randrange(0, 3)

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

        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()
            add_mob()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size_name):
        pygame.sprite.Sprite.__init__(self)
        self.size_name = size_name
        self.image = explosion_anim[size_name][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()

        if now - self.last_update >= self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size_name]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size_name][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


def add_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_bar(surf, image, healths):
    # 1ый кортеж (2 параметра) - расстояние от левого края того экрана, на котором рисуем (то есть это наш главный экран - display)
    # 1 значение - сколько слева отступ
    # 2 значение - сколько вниз отступ

    # 2ой кортеж (4 параметра)
    # первые 2 значения - расстояние от левого края картинки (тут как раз и нужен наш отступ,
    # для нас это количество жизней по факту, и еще кое-что)
    # следующие 2 значения - размеры самой картинки

    part_width = image.get_width() / 12
    offset_x = part_width * (healths - 1)

    surf.blit(image, (230, 10), (offset_x, 0, part_width, image.get_height()))


font_name = pygame.font.match_font('arial')


def draw_text(text, size, surf, x, y):
    font = pygame.font.Font(font_name, size)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect()
    text_rect.x = x
    text_rect.y = y
    surf.blit(text_surf, text_rect)


def draw_capabilities():
    global score
    if score < LASER_PRICE:
        display.blit(red_ball, red_rect)
    else:
        display.blit(green_ball, green_rect)


def create_bullet(btype):
    bullet = Bullet(player.rect.centerx, player.rect.top, btype)
    random.choice(shoot_sounds).play()
    all_sprites.add(bullet)
    bullets.add(bullet)


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

shield_img = pygame.image.load(os.path.join(img_folder, 'sp_bar_health_strip12.png')).convert()
shield_img.set_colorkey((0, 0, 0))
size = shield_img.get_size()
shield_img = pygame.transform.scale(shield_img, (size[0] * 2.5, size[1] * 2.5))

meteor_images = []
meteor_list = [('meteorBrown_small2.png',
                'meteorBrown_small1.png'),

               ('meteorBrown_med1.png',
                'meteorBrown_med3.png'),

               ('meteorBrown_big1.png',
                'meteorBrown_big3.png')]

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
img_exp = os.path.join(game_folder, 'img', 'exploation')

for i in range(9):
    filename = f'regularExplosion0{i}.png'
    png = pygame.image.load(os.path.join(img_exp, filename)).convert()
    png.set_colorkey((0, 0, 0))
    large = pygame.transform.scale(png, (75, 75))
    explosion_anim['lg'].append(large)
    small = pygame.transform.scale(png, (75, 75))
    explosion_anim['sm'].append(small)

green_surf = pygame.image.load(os.path.join(img_folder, 'green.png')).convert()
red_surf = pygame.image.load(os.path.join(img_folder, 'red.png')).convert()

red_ball = pygame.transform.scale(red_surf, (70, 70))
red_rect = red_surf.get_rect()
red_rect.center = (300, 160)

green_ball = pygame.transform.scale(green_surf, (70, 70))
green_rect = green_surf.get_rect()
green_rect.center = (300, 160)

red_ball.set_colorkey((255, 255, 255))
green_ball.set_colorkey((255, 255, 255))

shoot_sound_1 = pygame.mixer.Sound(os.path.join(snd_dir, 'Laser_Shoot.wav'))
shoot_sound_2 = pygame.mixer.Sound(os.path.join(snd_dir, 'Laser_Shoot3.wav'))
shoot_sound_3 = pygame.mixer.Sound(os.path.join(snd_dir, 'Laser_Shoot4.wav'))
hit_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'Hit_Hurt.wav'))

shoot_sounds = [shoot_sound_1,
                shoot_sound_2,
                shoot_sound_3]

# pygame.mixer.music.load(os.path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
# pygame.mixer.music.set_volume(0.4)

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

# pygame.mixer.music.play(loops=-1)

switch = True

while switch:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            switch = False

    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.damage
        print(player.shield)
        hit.kill()
        add_mob()
        exp = Explosion(hit.rect.center, 'sm')
        all_sprites.add(exp)
        if player.shield <= 0:
            switch = False

    hits = pygame.sprite.groupcollide(mobs, bullets, False, False)
    for mob, bulls in hits.items():
        if bulls[0].type == 'blue':
            mob.hp -= bulls[0].damage
            if mob.hp <= 0:
                mob.kill()
                add_mob()
                score += 50 - mob.radius
                hit_sound.play()
                bulls[0].kill()
                exp = Explosion(mob.rect.center, 'lg')
                all_sprites.add(exp)
            for b in hits[mob]:
                b.kill()
        elif bulls[0].type == 'red':
            mob.kill()
            add_mob()
            hit_sound.play()

    display.fill((0, 0, 0))
    display.blit(background, background_rect)
    # display.blit(health_bar.image, (704, 0))
    all_sprites.draw(display)

    draw_text(f'score: {score}', 30, display, 10, 15)
    draw_bar(display, shield_img, player.shield)
    draw_capabilities()

    pygame.display.flip()

pygame.quit()
