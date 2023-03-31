import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, h, r, g, b):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((700, 133))
        self.image.fill((r, g, b))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, h)


WIDTH = 700
HEIGHT = 400
FPS = 60

BLACK = (0, 0, 0)
pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('test')
clock = pygame.time.Clock()
group_sprite = pygame.sprite.Group()
white = Player(66, 255, 255, 255)
blue = Player(198, 0, 100, 250)
red = Player(330, 255, 0, 0)
group_sprite.add(white, blue, red)

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
