from agents.stablebaselines3_models import *


class DRLAgentPrivate(DRLAgent):
    def __init__(self, *args, **kwars):
        super(DRLAgentPrivate, self).__init__(*args, **kwars)

    def train_model(self, model, tb_log_name, total_timesteps=5000, n_eval_episodes=5):
        model = model.learn(
            total_timesteps=total_timesteps,
            tb_log_name=tb_log_name,
            callback=TensorboardCallback(),
            n_eval_episodes=n_eval_episodes,
        )
        return model
