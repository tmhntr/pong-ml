from stable_baselines3 import PPO
from pongEnv import PongEnv, PaddleAgent
import pongGame

# env = PongEnv(up_key={'unicode': 'w', 'key': 119, 'mod': 0, 'scancode': 26, 'window': None}, down_key={'unicode': 's', 'key': 115, 'mod': 0, 'scancode': 22, 'window': None}, side=0)

model = PPO.load("ppo_pong_right")

# obs = env.reset()
# while True:
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     env.render()

agent = PaddleAgent(model, player=pongGame.LEFT)
game = pongGame.Game(left_paddle=agent)
agent.set_game(game)

game.play()
