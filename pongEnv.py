from gym import Env
from gym.spaces import Discrete, Box
import numpy as np
import pongGame
import pygame


class PongEnv(Env):

    N_STEPS = 500000

    def __init__(self, side, game=pongGame.Game()):
        super(PongEnv, self).__init__()
        self.action_space = Discrete(3)
        # observations are ball x, ball y, ball vx, ball vy, paddle y
        self.observation_space = Box(low=np.array([0, 0, -pongGame.Ball.MAX_X_VELOCITY, -pongGame.Ball.MAX_Y_VELOCITY, 0]), high=np.array(
            [pongGame.SCREEN_WIDTH, pongGame.SCREEN_HEIGHT, pongGame.Ball.MAX_X_VELOCITY, pongGame.Ball.MAX_Y_VELOCITY, pongGame.SCREEN_HEIGHT]))

        self.reward_range = (-10, 0)

        self.game = game
        self.side = side

        if side == pongGame.LEFT:
            self.paddle = self.game.left
        elif side == pongGame.RIGHT:
            self.paddle = self.game.right
        else:
            raise ValueError("Side must be 0 or 1")

        self.step_number = 0

    def act(self, action):
        if action == 0:
            # move paddle down
            pygame.event.post(pygame.event.Event(
                pygame.KEYDOWN, {"key": self.paddle.down_key}))
        if action == 1:
            # do not move paddle
            pass
        if action == 2:
            # move paddle up
            pygame.event.post(pygame.event.Event(
                pygame.KEYDOWN, {"key": self.paddle.up_key}))

        observation = np.array([self.game.ball.rect.centerx, self.game.ball.rect.centery,
                               self.game.ball.xspeed, self.game.ball.yspeed, self.paddle.rect.centery])
        return observation

    def step(self, action):
        observation = self.act(action)

        reward = 0
        if self.score < self.paddle.losses:
            reward -= 20
            self.score = self.paddle.losses

        for event in pygame.event.get(eventtype=pongGame.BOUNCE):
            if self.side == event.side:
                reward += 10

        if self.step_number == self.N_STEPS:
            done = True
        else:
            done = False

        self.step_number += 1
        self.game.step()

        return observation, reward, done, {}

    def reset(self):
        self.game.reset()
        self.score = 0
        self.step_number = 0

        observation = np.array([self.game.ball.rect.centerx, self.game.ball.rect.centery,
                               self.game.ball.xspeed, self.game.ball.yspeed, self.paddle.rect.centery])
        return observation

    def render(self):
        self.game.render()

    def close(self):
        pass

    def seed(self):
        pass


class PaddleAgent(pongGame.Paddle):
    def __init__(self, model, player):
        super(PaddleAgent, self).__init__(
            player=player, keys=(pygame.K_w, pygame.K_s))
        self.model = model
        self.game = None

    def _observe(self):
        if not self.game:
            raise ValueError("Game must be set")
        else:
            return np.array([self.game.ball.rect.centerx, self.game.ball.rect.centery, self.game.ball.xspeed, self.game.ball.yspeed, self.rect.centery])

    def set_game(self, game: pongGame.Game):
        self.game = game

    def update(self, key=None):
        action, _states = self.model.predict(self._observe())
        if action == 0:
            self.move_down()
        elif action == 2:
            self.move_up()

        return super().update()
