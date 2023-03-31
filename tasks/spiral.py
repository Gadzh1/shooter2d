import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 100, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (0, 25)
        self.is_right = True
        self.is_bottom = False
        self.is_left = False
        self.is_top = False
        self.right = WIDTH
        self.left = 0
        self.top = 0
        self.bottom = HEIGHT

    def update(self):
        if self.is_right:
            if self.rect.right + 5 > self.right:
                self.is_right = False
                self.is_bottom = True
                self.top += 60
                return
            self.rect.right += 5

        if self.is_bottom:
            if self.rect.bottom + 5 > self.bottom:
                self.is_bottom = False
                self.is_left = True
                self.right -= 110
                return
            self.rect.bottom += 5

        if self.is_left:
            if self.rect.left - 5 < self.left:
                self.is_left = False
                self.is_top = True
                self.bottom -= 60
                return
            self.rect.left -= 5

        if self.is_top:
            if self.rect.top - 5 < self.top:
                self.is_top = False
                self.is_right = True
                self.left += 110
                return
            self.rect.top -= 5







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
