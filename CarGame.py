import pygame, sys
from pygame.locals import *
import random

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(GREY)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.svg")
        self.image = pygame.transform.scale_by(self.image, 0.6)
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),-100) 
        self.count = random.randint(40, 120)
        self.down = 10

    def move(self):
        if self.rect.top <= 0 and self.count != 0:
            self.count -= 1
            return None
        self.rect.move_ip(0,self.down)
        if self.rect.bottom > 600:
            self.count = random.randint(40, 120)
            self.rect.top = 0
            self.down = random.randint(8,13)
            self.rect.center = (random.randint(30, 370), -100)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.svg")
        self.image = pygame.transform.scale_by(self.image, 0.12)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN] or pressed_keys[K_s]:
                self.rect.move_ip(0,5) 
        if self.rect.left > 0:
            if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Road(pygame.sprite.Sprite):
    def __init__(self, count):
        super().__init__() 
        self.rect = Rect(SCREEN_WIDTH/2 - 5,-50,10,50)
        self.count = count

    def move(self):
        if self.rect.top <= 0 and self.count != 0:
            self.count -= 1
            return None
        self.rect.move_ip(0,10)
        if self.rect.bottom > 600:
            self.count = 20
            self.rect.top = -50
    
    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


P1 = Player()
Enemies = []
Enemies.append(Enemy())
Enemies.append(Enemy())
Enemies.append(Enemy())
Enemies.append(Enemy())

Roads = []
Roads.append(Road(0))
Roads.append(Road(20))
Roads.append(Road(40))
Roads.append(Road(60))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update()
    for i in range(len(Enemies)):
        Enemies[i].move()
    for i in range(len(Roads)):
        Roads[i].move()

    DISPLAYSURF.fill(GREY)
    P1.draw(DISPLAYSURF)
    for i in range(len(Enemies)):
        Enemies[i].draw(DISPLAYSURF)
    for i in range(len(Roads)):
        Roads[i].draw(DISPLAYSURF)
        

    pygame.display.update()
    FramePerSec.tick(FPS)
