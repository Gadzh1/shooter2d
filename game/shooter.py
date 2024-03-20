import pygame
import random

from constants import *
from bullet import Bullet
from meteor import Meteor
from player import Player
from explosion import Explosion
from health import Health
from powerup import Powerup
from enemy import Enemy, action_basic, action_zigzag


def create_bullet(btype, player, shoot_sounds, all_sprites, bullets):
    bullet = Bullet(player.rect.centerx, player.rect.top, btype)
    random.choice(shoot_sounds).play()
    all_sprites.add(bullet)
    bullets.add(bullet)


def shoot():
    global last_shot
    now = pygame.time.get_ticks()
    if now - last_shot > SHOOT_DELAY:
        last_shot = now
        create_bullet('blue', player, shoot_sounds, all_sprites, bullets)


def add_meteor():
    global current_meteors
    print('meteors: ' + str(len(meteors)))
    print('all sprites: ' + str(len(all_sprites)))

    if len(meteors) <= METEORS_AMOUNT:
        m = Meteor()
        all_sprites.add(m)
        meteors.add(m)
        current_meteors += 1


def kill_meteor(m):
    global current_meteors

    m.kill()

    # if current_meteors > 0:
    #     current_meteors -= 1


def draw_bar(surf, image, bar_healths):
    part_width = image.get_width() / 12
    offset_x = part_width * (bar_healths - 1)

    surf.blit(image, (230, 10), (offset_x, 0, part_width, image.get_height()))


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
        display.blit(red_circle, red_rect)
    else:
        display.blit(green_circle, green_rect)


def check_keys_state():
    global score
    keys_state = pygame.key.get_pressed()
    if keys_state[pygame.K_s]:
        shoot()
    if keys_state[pygame.K_w]:
        if score >= LASER_PRICE:
            score -= LASER_PRICE
            create_bullet('red', player, shoot_sounds, all_sprites, bullets)


def create_entity():
    chance_x = 410

    for _ in range(3):
        chance_x -= 50
        hp = Health((chance_x, 80))
        chances.add(hp)

    for i in range(METEORS_AMOUNT):
        global current_meteors

        mob = Meteor()
        all_sprites.add(mob)
        meteors.add(mob)
        current_meteors += 1

    global player
    player = Player()
    all_sprites.add(player)

    # enemy = Enemy()
    # all_sprites.add(enemy)
    # meteors.add(enemy)


player = object()

last_shot = pygame.time.get_ticks()

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('shooter')
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

chances = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

snd_dir = os.path.join(GAME_FOLDER, 'snd')

background = pygame.image.load(os.path.join(IMG_FOLDER, 'blue.png')).convert()

shield_img = pygame.image.load(os.path.join(IMG_FOLDER, 'sp_bar_health_strip12.png')).convert()
shield_img.set_colorkey((0, 0, 0))
size = shield_img.get_size()
shield_img = pygame.transform.scale(shield_img, (size[0] * 2.5, size[1] * 2.5))

green_surf = pygame.image.load(os.path.join(IMG_FOLDER, 'green.png')).convert()
red_surf = pygame.image.load(os.path.join(IMG_FOLDER, 'red.png')).convert()

red_circle = pygame.transform.scale(red_surf, (70, 70))
red_rect = red_surf.get_rect()
red_rect.center = (300, 160)

green_circle = pygame.transform.scale(green_surf, (70, 70))
green_rect = green_surf.get_rect()
green_rect.center = (300, 160)

red_circle.set_colorkey((255, 255, 255))
green_circle.set_colorkey((255, 255, 255))

shoot_sound_1 = pygame.mixer.Sound(os.path.join(snd_dir, 'Laser_Shoot.wav'))
shoot_sound_2 = pygame.mixer.Sound(os.path.join(snd_dir, 'Laser_Shoot3.wav'))
shoot_sound_3 = pygame.mixer.Sound(os.path.join(snd_dir, 'Laser_Shoot4.wav'))
hit_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'Hit_Hurt.wav'))

shoot_sounds = [shoot_sound_1,
                shoot_sound_2,
                shoot_sound_3]

# pygame.mixer.music.load(os.path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
# pygame.mixer.music.set_volume(0.4)
# pygame.mixer.music.play(loops=-1)


background_rect = background.get_rect()

current_meteors = 0
create_entity()

score = 0
switch = True
last_enemy_created = 0
enemy_interval = random.randint(7000, 15000)
enemy_interval = 1000

while switch:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            switch = False

    check_keys_state()

    for i in meteors:
        if i.rect.top > HEIGHT or i.rect.right < 0 or i.rect.left > WIDTH:
            kill_meteor(i)
            add_meteor()

    all_sprites.update()

    time = pygame.time.get_ticks()
    if time - last_enemy_created >= enemy_interval:
        last_enemy_created = time - 1
        enemy_obj = Enemy(5, 5, WIDTH / 2, -50)
        all_sprites.add(enemy_obj)
        meteors.add(enemy_obj)

    hits = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.damage
        kill_meteor(hit)
        add_meteor()
        exp = Explosion(hit.rect.center, 'sm')
        all_sprites.add(exp)

        if player.health <= 0:
            if GAME_CHANCES == 1:
                switch = False
            else:
                chances.empty()
                GAME_CHANCES -= 1

                chance_x = 410
                for i in range(GAME_CHANCES):
                    chance_x -= 50
                    hp = Health((chance_x, 80))
                    chances.add(hp)

                player.health = 12

    hits = pygame.sprite.groupcollide(meteors, bullets, False, False)
    for mob, bulls in hits.items():
        for b in bulls:

            if b.type == 'red':
                kill_meteor(mob)
                print('------')
                print('after kill ' + str(current_meteors))
                hit_sound.play()
                add_meteor()
                print('after add ' + str(current_meteors))
                break

            if b.type == 'blue':
                mob.hp -= b.damage
                if mob.hp <= 0:
                    x = mob.rect.x
                    y = mob.rect.y

                    kill_meteor(mob)
                    add_meteor()
                    score += 50 - mob.radius
                    hit_sound.play()

                    if 0 <= mob.size < 2:
                        t = 'sm'
                    else:
                        t = 'lg'

                    exp = Explosion(mob.rect.center, t)
                    all_sprites.add(exp)

                    num = random.randint(0, 3)
                    if num:
                        if num == 1:
                            powerup = Powerup(x, y, 'shield')
                            powerups.add(powerup)
                            all_sprites.add(powerup)
                        else:
                            powerup = Powerup(mob.rect.x, mob.rect.y, 'gun')
                            powerups.add(powerup)
                            all_sprites.add(powerup)

                b.kill()

    hits = pygame.sprite.groupcollide(player, powerups, False, False)
    for player, power in hits.items():
        if power.type == 'shield':
            player.health += random.randint()

            # power.kill()


    display.fill((0, 0, 0))
    display.blit(background, background_rect)
    all_sprites.draw(display)
    chances.draw(display)

    draw_text(f'score: {score}', 30, display, 10, 15)
    draw_bar(display, shield_img, player.health)
    draw_capabilities()

    pygame.display.flip()

pygame.quit()
