import pygame
import random

from constants import *
from bullet import Bullet
from mob import Mob
from player import Player
from explosion import Explosion
from health import Health


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


def add_mob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


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
        display.blit(red_ball, red_rect)
    else:
        display.blit(green_ball, green_rect)


def check_keys_state():
    global score
    keys_state = pygame.key.get_pressed()
    if keys_state[pygame.K_s]:
        shoot()
    if keys_state[pygame.K_w]:
        if score >= LASER_PRICE:
            score -= LASER_PRICE
            create_bullet('red', player, shoot_sounds, all_sprites, bullets)


last_shot = pygame.time.get_ticks()

pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('shooter')
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

chances = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

snd_dir = os.path.join(GAME_FOLDER, 'snd')

background = pygame.image.load(os.path.join(IMG_FOLDER, 'blue.png')).convert()

shield_img = pygame.image.load(os.path.join(IMG_FOLDER, 'sp_bar_health_strip12.png')).convert()
shield_img.set_colorkey((0, 0, 0))
size = shield_img.get_size()
shield_img = pygame.transform.scale(shield_img, (size[0] * 2.5, size[1] * 2.5))

green_surf = pygame.image.load(os.path.join(IMG_FOLDER, 'green.png')).convert()
red_surf = pygame.image.load(os.path.join(IMG_FOLDER, 'red.png')).convert()

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
# pygame.mixer.music.play(loops=-1)


background_rect = background.get_rect()

chance_x = 410
for _ in range(3):
    chance_x -= 50
    hp = Health((chance_x, 80))
    chances.add(hp)

for i in range(8):
    mob = Mob()
    all_sprites.add(mob)
    mobs.add(mob)

player = Player()
all_sprites.add(player)

score = 0
switch = True

while switch:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            switch = False

    check_keys_state()

    for i in mobs:
        if i.rect.top > HEIGHT or i.rect.right < 0 or i.rect.left > WIDTH:
            i.kill()
            add_mob()

    all_sprites.update()

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= hit.damage
        print(player.health)
        hit.kill()
        add_mob()
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

                if 0 <= mob.size < 2:
                    t = 'sm'

                elif mob.size == 2:
                    t = 'lg'

                exp = Explosion(mob.rect.center, t)
                all_sprites.add(exp)

            for b in hits[mob]:
                b.kill()
        elif bulls[0].type == 'red':
            mob.kill()
            add_mob()
            hit_sound.play()

    display.fill((0, 0, 0))
    display.blit(background, background_rect)
    all_sprites.draw(display)
    chances.draw(display)

    draw_text(f'score: {score}', 30, display, 10, 15)
    draw_bar(display, shield_img, player.health)
    draw_capabilities()

    pygame.display.flip()

pygame.quit()
