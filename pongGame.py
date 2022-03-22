from threading import current_thread
import pygame
import random

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_w,
    K_s,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

LEFT = 0
RIGHT = 1

BOUNCE = pygame.event.custom_type()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Paddle(pygame.sprite.Sprite):
    width = 10
    height = 100

    def __init__(self, player: int, keys: tuple, agent=None):
        super(Paddle, self).__init__()
        self.player = player
        self.yspeed = 5
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 0))
        x = self.width/2 if player == LEFT else SCREEN_WIDTH - self.width/2
        self.rect = self.surf.get_rect(
            center=(x, (SCREEN_HEIGHT+self.height)/2))
        self.wins = 0
        self.losses = 0

        self.up_key = keys[0]
        self.down_key = keys[1]

    def move_up(self):
        self.rect.move_ip(0, -1*self.yspeed)

    def move_down(self):
        self.rect.move_ip(0, 1*self.yspeed)

    def update(self, key=None):
        if key == self.up_key:
            self.move_up()
        if key == self.down_key:
            self.move_down()

        # keep paddle from moving off screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


class Ball(pygame.sprite.Sprite):
    width = 8
    height = 8

    MAX_X_VELOCITY = 3
    MAX_Y_VELOCITY = 8

    def __init__(self):
        super(Ball, self).__init__()
        self.xspeed = random.choice(
            [-self.MAX_X_VELOCITY, self.MAX_X_VELOCITY])
        self.yspeed = random.randint(-5, 5)
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((0, 0, 255))

        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    def bounce(self, side):
        if side == RIGHT:
            self.xspeed = -abs(self.xspeed)
        if side == LEFT:
            self.xspeed = abs(self.xspeed)
        self.yspeed = random.randint(
            max(-self.MAX_Y_VELOCITY, self.yspeed - 4), min(self.MAX_Y_VELOCITY, self.yspeed + 4))

    def update(self):
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.yspeed = -self.yspeed
        if self.rect.top < 0:
            self.rect.top = 0
            self.yspeed = -self.yspeed
        self.rect.move_ip(self.xspeed, self.yspeed)


class Game():

    def __init__(self, left_paddle=Paddle(player=LEFT, keys=(K_w, K_s)), right_paddle=Paddle(player=RIGHT, keys=(K_UP, K_DOWN))):
        self.left = left_paddle
        self.right = right_paddle
        self.ball = Ball()
        self.all_sprites = pygame.sprite.Group(
            [self.left, self.right, self.ball])
        self.paddles = pygame.sprite.Group([self.left, self.right])

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.DISPLAY_SCORE = True

    def render(self):
        # Fill the background with white
        self.screen.fill((255, 255, 255))

        # blit all sprites
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        # Flip the display
        pygame.display.flip()
        self.clock.tick(60)

    def reset(self):
        self.left.wins = 0
        self.left.losses = 0
        self.right.wins = 0
        self.right.losses = 0

        self.clock = pygame.time.Clock()
        self.ball.kill()
        self.ball = Ball()
        self.all_sprites.add(self.ball)

    def step(self):
        current_events = pygame.event.get()
        for event in current_events:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == QUIT:
                self.running = False

        # move paddles
        for entity in self.paddles:
            for key in [entity.up_key, entity.down_key]:
                if pygame.key.get_pressed()[key]:
                    entity.update(key)
                elif any(map(lambda event: event.type == KEYDOWN and event.key == key, current_events)):
                    entity.update(key)
                else:
                    entity.update()

        ball_collision = pygame.sprite.spritecollideany(
            self.ball, self.paddles)
        if ball_collision == self.left:
            self.ball.bounce(LEFT)
            pygame.event.post(pygame.event.Event(BOUNCE, {"side": LEFT}))
        elif ball_collision == self.right:
            self.ball.bounce(RIGHT)
            pygame.event.post(pygame.event.Event(BOUNCE, {"side": RIGHT}))

        self.ball.update()

        if self.ball.rect.right < 0:
            self.ball.kill()
            self.ball = Ball()
            self.all_sprites.add(self.ball)
            self.right.wins += 1
            self.left.losses += 1
            if self.DISPLAY_SCORE:
                print(f"Left: {self.left.wins}\tRight: {self.right.wins}")
        if self.ball.rect.left > SCREEN_WIDTH:
            self.ball.kill()
            self.ball = Ball()
            self.all_sprites.add(self.ball)
            self.left.wins += 1
            self.right.losses += 1
            if self.DISPLAY_SCORE:
                print(f"Left: {self.left.wins}\tRight: {self.right.wins}")

    def play(self):
        self.running = True
        while self.running:

            self.step()

            self.render()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.play()
