import random

import pygame

from constants import *
from bullet import Bullet
from meteor import Meteor
from player import Player
from explosion import Explosion
from health import Health
from powerup import Powerup
from enemy import Enemy


def create_bullet(btype, obj, shoot_sounds, all_sprites, bullets):
    bullet = Bullet(obj.rect.centerx, obj.rect.top, btype)
    # random.choice(shoot_sounds).play()
    all_sprites.add(bullet)
    bullets.add(bullet)


def create_enemies_bullet(obj, shoot_sounds, speed):
    bullet = Bullet(obj.rect.centerx, obj.rect.bottom, 'green')
    bullet.speed_y = speed
    # random.choice(shoot_sounds).play()
    all_sprites.add(bullet)
    enemies_bullets.add(bullet)


def shoot(btype, speed=5):
    global last_shot_blue
    global last_shot_green

    if btype == 'blue':
        now = pygame.time.get_ticks()
        if now - last_shot_blue > SHOOT_DELAY:
            last_shot_blue = now
            create_bullet('blue', player, shoot_sounds, all_sprites, bullets)

    elif btype == 'green':
        en = enemies.sprites()[0]

        now = pygame.time.get_ticks()
        if now - last_shot_green > 500:
            last_shot_green = now
            create_enemies_bullet(en, shoot_sounds, speed)


def create_meteor():
    if len(meteors) <= METEORS_AMOUNT:
        m = Meteor()
        all_sprites.add(m)
        meteors.add(m)


def draw_bar(surf, image, bar_healths):
    part_width = image.get_width() / 12
    offset_x = part_width * (bar_healths - 1)

    surf.blit(image, (230, 10), (offset_x, 0, part_width, image.get_height()))


def draw_text(text, size_value, surf, x, y):
    font = pygame.font.Font(font_name, size_value)
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
        shoot('blue')
    if keys_state[pygame.K_w]:
        if score >= LASER_PRICE:
            score -= LASER_PRICE
            create_bullet('red', player, shoot_sounds, all_sprites, bullets)


def create_basic_entities():
    chance_x = 410

    for _ in range(HEALTH_AMOUNT):
        chance_x -= 50
        hp = Health((chance_x, 80))
        chances.add(hp)

    for i in range(METEORS_AMOUNT):
        mob = Meteor()
        all_sprites.add(mob)
        meteors.add(mob)

    global player
    player = Player()
    all_sprites.add(player)


def collide_player_to_obj(player_obj, meteors_gr):
    global GAME_CHANCES, is_playing

    hit_meteors = pygame.sprite.spritecollide(player_obj, meteors_gr, True, pygame.sprite.collide_circle)
    for m in hit_meteors:
        player_obj.health -= m.damage
        m.kill()
        create_meteor()
        exp = Explosion(m.rect.center, 'sm')
        all_sprites.add(exp)

        if player_obj.health <= 0:
            if GAME_CHANCES == 1:
                is_playing = False
            else:
                chances.empty()
                GAME_CHANCES -= 1

                chance_x = 410
                for i in range(GAME_CHANCES):
                    chance_x -= 50
                    hp = Health((chance_x, 80))
                    chances.add(hp)

                player_obj.health = 12


def collide_bullets_to_obj(bullets_gr, meteors_gr):
    global score

    hits = pygame.sprite.groupcollide(meteors_gr, bullets_gr, False, False)
    for meteor, bulls in hits.items():
        for b in bulls:

            if b.type == 'red':
                meteor.kill()
                # hit_sound.play()
                create_meteor()
                break

            if b.type == 'blue':
                x = meteor.rect.centerx
                y = meteor.rect.y
                if IS_POWER_ON:
                    meteor.kill()
                    create_meteor()
                    b.kill()
                    if 0 <= meteor.size < 2:
                        t = 'sm'
                    else:
                        t = 'lg'
                    exp = Explosion(meteor.rect.center, t)
                    all_sprites.add(exp)
                    return

                meteor.hp -= b.damage
                if meteor.hp <= 0:

                    # rand = random.randint(1, 3)
                    # if rand == 3:
                    #     powerup = Powerup(meteor.rect.x, meteor.rect.y)

                    meteor.kill()
                    create_meteor()
                    score += 50 - meteor.radius
                    # hit_sound.play()

                    if 0 <= meteor.size < 2:
                        t = 'sm'
                    else:
                        t = 'lg'

                    exp = Explosion(meteor.rect.center, t)
                    all_sprites.add(exp)

                    rand = random.randint(0, 1)
                    if not rand:
                        powerup = Powerup(x, y)
                        all_sprites.add(powerup)
                        powerups.add(powerup)

            b.kill()


def collide_bullets_to_player(player, bullets):
    global GAME_CHANCES, is_playing

    hits = pygame.sprite.spritecollide(player, bullets, True, pygame.sprite.collide_circle)
    for b in hits:
        player.health -= b.damage

        exp = Explosion(b.rect.center, 'sm')
        all_sprites.add(exp)

        if player.health <= 0:
            if GAME_CHANCES == 1:
                is_playing = False
            else:
                chances.empty()
                GAME_CHANCES -= 1

                chance_x = 410
                for i in range(GAME_CHANCES):
                    chance_x -= 50
                    hp = Health((chance_x, 80))
                    chances.add(hp)

                player.health = 12


def collide_powerups_to_player(powerup, player):
    hits = pygame.sprite.spritecollide(player, powerup, True, pygame.sprite.collide_circle)
    for p in hits:
        if p.type == 'shield':
            player.health += 3
            if player.health > 12:
                player.health = 12
            p.kill()
        else:
            global IS_POWER_ON, TIMER
            IS_POWER_ON = True
            TIMER = pygame.time.get_ticks()


def create_enemy():
    global last_enemy_created

    time = pygame.time.get_ticks()
    if time - last_enemy_created >= enemy_interval:
        last_enemy_created = time - 1
        enemy = Enemy(3, 5, WIDTH / 2, -50)
        all_sprites.add(enemy)
        enemies.add(enemy)


# start of the main ------------------------------
player = object()

last_shot_blue = pygame.time.get_ticks()
last_shot_green = pygame.time.get_ticks()

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('shooter')
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

# groups ------------------------
chances = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
enemies_bullets = pygame.sprite.Group()
# images ------------------------
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

# sounds ------------------------
snd_dir = os.path.join(GAME_FOLDER, 'snd')
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
# ---------------------------------


background_rect = background.get_rect()
create_basic_entities()

score = 0
is_playing = True
last_enemy_created = 0
# enemy_interval = random.randint(7000, 15000)
enemy_interval = 10000

while is_playing:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_playing = False

    check_keys_state()

    for m in meteors:
        if m.rect.top > HEIGHT or m.rect.right < 0 or m.rect.left > WIDTH:
            m.kill()
            create_meteor()

    if len(enemies) == 0:
        create_enemy()

    for en in enemies.sprites():

        if en.action_order > 1:
            speed = 5
            if en.action_order == 4:
                speed = 10
            shoot('green', speed)
    global IS_POWER_ON
    if IS_POWER_ON:
        global TIMER
        if pygame.time.get_ticks() - TIMER > 10000:
            IS_POWER_ON = False

    all_sprites.update()

    # collides ------------------------
    collide_player_to_obj(player, meteors)
    collide_player_to_obj(player, enemies)
    collide_bullets_to_obj(bullets, meteors)
    collide_bullets_to_obj(bullets, enemies)
    collide_bullets_to_player(player, enemies_bullets)
    collide_powerups_to_player(powerups, player)
    # ---------------------------------

    display.fill((0, 0, 0))
    display.blit(background, background_rect)
    all_sprites.draw(display)
    chances.draw(display)

    draw_text(f'score: {score}', 30, display, 10, 15)
    draw_bar(display, shield_img, player.health)
    draw_capabilities()

    pygame.display.flip()

pygame.quit()
