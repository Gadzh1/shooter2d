import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.is_top = True
        self.is_bottom = False

    def set_directions(self, bottom, top):
        self.is_bottom = bottom
        self.is_top = top

    def update(self):
        if self.is_top:
            if self.rect.top - 5 < 0:
                self.set_directions(True, False)
                return
            self.rect.y -= 5
        if self.is_bottom:
            if self.rect.bottom + 5 > HEIGHT:
                self.set_directions(False, True)
                return
            self.rect.y += 5


WIDTH = 700
HEIGHT = 400
FPS = 60

BLACK = (0, 0, 0)
pygame.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('test')
clock = pygame.time.Clock()
group_sprite = pygame.sprite.Group()
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
