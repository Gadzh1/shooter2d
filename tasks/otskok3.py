import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.set_directions(False, True, False, False)
        self.vert = False
        self.hor = True
        self.otskoki = 0

    def set_directions(self, left, right, bottom, top):
        self.is_left = left
        self.is_right = right
        self.is_bottom = bottom
        self.is_top = top

    def horizontally(self):
        if self.is_right:
            if self.rect.right + 5 > WIDTH:
                self.otskoki += 1
                self.set_directions(True, False, False, False)
                return
            self.rect.x += 5
        if self.is_left:
            if self.rect.left - 5 < 0:
                self.otskoki += 1
                self.set_directions(False, True, False, False)
                return
            self.rect.x -= 5

    def vertically(self):
        if self.is_top:
            if self.rect.top - 5 < 0:
                self.otskoki += 1
                self.set_directions(False, False, True, False)
                return
            self.rect.y -= 5
        if self.is_bottom:
            if self.rect.bottom + 5 > HEIGHT:
                self.otskoki += 1
                self.set_directions(False, False, False, True)
                return
            self.rect.y += 5

    def update(self):
        if self.hor:
            self.horizontally()
            if self.otskoki == 2 and self.rect.right == 375:
                self.otskoki = 0
                self.hor = False
                self.vert = True
                self.set_directions(False, False, False, True)
            return
        if self.vert:
            self.vertically()
            if self.otskoki == 2 and self.rect.y == 200:
                self.otskoki = 0
                self.hor = True
                self.vert = False
                self.set_directions(False, True, False, False)
            return


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
