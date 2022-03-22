from pongEnv import PaddleAgent, PongEnv
from pongGame import Game, LEFT, RIGHT

from stable_baselines3.common.env_checker import check_env
from stable_baselines3 import PPO

left_model = PPO.load("ppo_pong_right")
agent = PaddleAgent(left_model, player=LEFT)
game = Game(left_paddle=agent)
game.DISPLAY_SCORE = False
agent.set_game(game)

env = PongEnv(side=RIGHT, game=game)
# check_env(env)

right_model = PPO("MlpPolicy", env, verbose=1)
right_model.learn(total_timesteps=500000)

right_model.save("Ronda")

obs = env.reset()
while True:
    action, _states = right_model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()

# obs = env.reset()
# n_steps = env.N_STEPS
# for _ in range(n_steps):
#     env.render()
#     # Random action
#     action = env.action_space.sample()
#     obs, reward, done, info = env.step(action)
#     if done:
#         obs = env.reset()
