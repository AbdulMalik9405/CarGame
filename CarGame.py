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
        self.rect = self.image.get_rect() #108,60
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),10)
        self.count = random.randint(40, 120)
        self.down = 10
        self.rect2 = self.image.get_rect().scale_by(1,12)

    def move(self):
        self.spawn()
        if self.rect.top <= 0 and self.count != 0: #Wait random time when respawning
            self.count -= 1
            return None
        self.rect.move_ip(0,self.down)

    def draw(self, surface):
        # pygame.draw.rect(surface, WHITE, self.rect2)
        surface.blit(self.image, self.rect)

    def spawn(self):
        if self.rect.bottom > 600:
            self.count = random.randint(40, 120)
            self.rect.top = 0
            self.down = random.randint(8,13)
            self.rect.center = (random.randint(30, 370), 10)
            self.rect2.center = self.rect.center
        for enemy in Enemies:
            if self.rect2.colliderect(self.rect):
                continue
            collide = True
            while collide is True:
                for enemy in Enemies:
                    if self.rect2.colliderect(self.rect):
                        continue
                    if self.rect2.colliderect(enemy.rect):
                        self.rect.center = (random.randint(30, 370), 10)
                        self.rect2.center = self.rect.center
                        collide = True
                else:
                    collide = False
        # collide = True
        # while collide is True:
        #     for enemy in Enemies:
        #         if self.rect2.colliderect(self.rect):
        #             continue
        #         if self.rect2.colliderect(enemy):
        #             self.rect.center = (random.randint(30, 370), -100)
        #             self.rect2.center = self.rect.center
        #             collide = True
        #         else:
        #             collide = False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.svg")
        self.image = pygame.transform.scale_by(self.image, 0.12)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        self.time = 0

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
        # pygame.draw.rect(surface, WHITE, self.rect)

    def collision(self):
        for enemy in Enemies:
            if P1.rect.colliderect(enemy):
                print("Collision Detected. Game Over")
                print("Time Score:", self.time)
                file = open("highscore.txt", "a")
                file.write(str(self.time) + ",lose" + "\n")
                file.close()
                highscoreTrack()
                print("TOP 3 HIGHSCORES")
                for i in range(3):
                    if len(lose) > i:
                        print(f"{i+1}: {lose[i]:.2f} seconds")
                    else:
                        print("Not enough scores")
                pygame.quit()
                sys.exit()

    def win(self):
        if P1.rect.top <= 0:
            print("Made it to the end of the road. Game Win")
            print("Time Score:", self.time)
            file = open("highscore.txt", "a")
            file.write(str(self.time) + ",win" + "\n")
            file.close()
            highscoreTrack()
            print("TOP 3 WIN HIGHSCORES")
            for i in range(3):
                if len(win) > i:
                    print(f"{i+1}: {win[i]:.2f} seconds")
                else:
                    print("Not enough scores")
            pygame.quit()
            sys.exit()

    def powerupcollision(self):
        for power in PowerUps:
            if P1.rect.colliderect(power):
                if self.rect.width >= 20:
                    power.playercollision()
                    self.image = pygame.transform.scale_by(self.image, 0.8)
                    current = self.rect.center
                    self.rect = self.image.get_rect()
                    self.rect.center = current
                    print("Powerup collision")
                else:
                    print("Car too small for powerup")
                    power.playercollision()
        for badPower in BadPowerUps:
            if P1.rect.colliderect(badPower):
                enemyChoice = random.choice(Enemies)
                if enemyChoice.rect.width <= 80:
                    badPower.playercollision()
                    enemyChoice.image = pygame.transform.scale_by(enemyChoice.image, 1.2)
                    current = enemyChoice.rect.center
                    enemyChoice.rect = enemyChoice.image.get_rect()
                    enemyChoice.rect.center = current
                    enemyChoice.rect2 = enemyChoice.rect.scale_by(1,12)
                    print("Powerup collision")
                else:
                    print("Car too big for powerup")
                    badPower.playercollision()

    def set_time(self, time):
        self.time += time

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

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("powerup.png")
        self.image = pygame.transform.scale_by(self.image, 0.08)
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
            self.rect.center = (random.randint(30, 370), -100)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def playercollision(self):
        if P1.rect.colliderect(self):
            self.rect.top = -50
            self.rect.center = (random.randint(30, 370), -100)

class BadPowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("badpower.webp")
        self.image = pygame.transform.scale_by(self.image, 0.05)
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
            self.rect.center = (random.randint(30, 370), -100)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def playercollision(self):
        if P1.rect.colliderect(self):
            self.rect.top = -50
            self.rect.center = (random.randint(30, 370), -100)

def highscoreTrack():
    global win, lose

    file = open("highscore.txt", "r")
    for line in file:
        timelist = line.strip().split(",")
        if timelist[1] == "win":
            win.append(float(timelist[0]))
        else:
            lose.append(float(timelist[0]))
    win.sort()
    lose.sort(reverse=True)
    file.close()

P1 = Player()
Enemies = []
Enemies.append(Enemy())
Enemies.append(Enemy())
# Enemies.append(Enemy())
# Enemies.append(Enemy())

Roads = []
Roads.append(Road(0))
Roads.append(Road(20))
Roads.append(Road(40))
Roads.append(Road(60))

PowerUps = []
PowerUps.append(PowerUp())
PowerUps.append(PowerUp())

BadPowerUps = []
BadPowerUps.append(BadPowerUp())
BadPowerUps.append(BadPowerUp())

time = 0
win = []
lose = []
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.powerupcollision()
    P1.update()
    for i in range(len(Enemies)):
        Enemies[i].move()
    for i in range(len(PowerUps)):
        PowerUps[i].move()
    for i in range(len(BadPowerUps)):
        BadPowerUps[i].move()
    for i in range(len(Roads)):
        Roads[i].move()

    DISPLAYSURF.fill(GREY)
    for i in range(len(Roads)):
        Roads[i].draw(DISPLAYSURF)
    P1.draw(DISPLAYSURF)
    for i in range(len(Enemies)):
        Enemies[i].draw(DISPLAYSURF)
    for i in range(len(PowerUps)):
        PowerUps[i].draw(DISPLAYSURF)
    for i in range(len(BadPowerUps)):
        BadPowerUps[i].draw(DISPLAYSURF)

    P1.collision()
    P1.win()

    time = 1/FPS
    P1.set_time(time)
    pygame.display.update()
    FramePerSec.tick(FPS)
