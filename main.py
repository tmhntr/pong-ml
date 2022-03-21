import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_s,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Paddle(pygame.sprite.Sprite):
    width = 10
    height = 100

    def __init__(self, player, yspeed = 0):
        super(Paddle, self).__init__()
        self.player = player
        self.yspeed = yspeed
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 0))
        x = self.width/2 if player == 1 else SCREEN_WIDTH - self.width/2 
        self.rect = self.surf.get_rect(center=(x, (SCREEN_HEIGHT+self.height)/2))

    def update(self, pressed_keys):
        if self.player == 1:
            if pressed_keys[K_w]:
                self.rect.move_ip(0, -1*self.yspeed)
            if pressed_keys[K_s]:
                self.rect.move_ip(0, 1*self.yspeed)
        elif self.player == 2:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -1*self.yspeed)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 1*self.yspeed)
        
        # keep paddle from moving off screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


class Ball(pygame.sprite.Sprite):
    width = 8
    height = 8
    def __init__(self):
        super(Ball, self).__init__()
        self.xspeed = random.choice([-3, 3])
        self.yspeed = random.randint(-5, 5)
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 255))

        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    def bounce(self):
        self.xspeed = -self.xspeed
        self.yspeed = random.randint(max(-8, self.yspeed - 4), min(8, self.yspeed + 4))


    def update(self):
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.yspeed = -self.yspeed
        if self.rect.top < 0:
            self.rect.top = 0
            self.yspeed = -self.yspeed
        self.rect.move_ip(self.xspeed, self.yspeed)

        
            
        


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

p1 = Paddle(1, yspeed=5)
p2 = Paddle(2, yspeed=5)
ball = Ball()

all_sprites = pygame.sprite.Group()
paddles = pygame.sprite.Group()

paddles.add(p1)
paddles.add(p2)
all_sprites.add(p1)
all_sprites.add(p2)
all_sprites.add(ball)

clock = pygame.time.Clock()
# Run until quit
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    # update players
    pressed_keys = pygame.key.get_pressed()
    for entity in paddles:
        entity.update(pressed_keys)
        if pygame.sprite.collide_rect(ball, entity):
            ball.bounce()
            

    ball.update()

    if ball.rect.right < 0 or ball.rect.left > SCREEN_WIDTH:
        ball.kill()
        ball = Ball()
        all_sprites.add(ball)


    # Fill the background with white
    screen.fill((255, 255, 255))

    # blit all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Flip the display
    pygame.display.flip()
    
    clock.tick(60)
# Done! Time to quit.
pygame.quit()
