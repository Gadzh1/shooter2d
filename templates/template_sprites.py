import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    # def update(self):
    #     self.rect.x += 5
    #     if self.rect.left > WIDTH:
    #         self.rect.right = 0


WIDTH = 700
HEIGHT = 400
FPS = 60

BLACK = (0, 100, 250)
pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('test')
clock = pygame.time.Clock()
group_sprite = pygame.sprite.Group()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, '../game/img')
player_img = pygame.image.load(os.path.join(img_folder, 'playerShip2_blue.png')).convert()

player = Player()
group_sprite.add(player)

switch = True
while switch:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            switch = False

    group_sprite.update()

    display.fill(BLACK)
    group_sprite.draw(display)
    pygame.display.flip()

pygame.quit()
