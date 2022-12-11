#!/usr/bin/python
# -*- coding: UTF-8 -*-

from typing import Any, Tuple, Union

import numpy as np
from keras.engine.training import Model
from numpy import ndarray
from pandas import DataFrame
from stockprediction.base.compatibility import screen_input
from stockprediction.base.logger_configurator import LoggerConfigurator
from stockprediction.environment.stockenv import StockTradingEnvPrivate

from agents.stablebaselines3_models import DRLAgent, TensorboardCallback


class DRLAgentPrivate(DRLAgent):
    def __init__(self, *args, **kwars):
        super(DRLAgentPrivate, self).__init__(*args, **kwars)
        logconfigur = LoggerConfigurator("DRLAgentPrivate", './log',
                                         'DRLAgentPrivate.log', 
                                         level='debug')
        self.logger = logconfigur.get_logger()

    def train_model(self, model, tb_log_name, total_timesteps=5000, n_eval_episodes=5):
        model = model.learn(
            total_timesteps=total_timesteps,
            tb_log_name=tb_log_name,
            callback=TensorboardCallback(),
            n_eval_episodes=n_eval_episodes,
        )
        return model

    @staticmethod
    def DRL_prediction(model, environment):
        test_env, test_obs = environment.get_sb_env()
        """make a prediction"""
        account_memory = []
        actions_memory = []
        test_env.reset()
        for day_idx in range(len(environment.df.index.unique())):
            action, _states = model.predict(test_obs)
            # account_memory = test_env.env_method(method_name="save_asset_memory")
            # actions_memory = test_env.env_method(method_name="save_action_memory")
            test_obs, rewards, dones, info = test_env.step(action)
            if day_idx == (len(environment.df.index.unique()) - 2):
                account_memory = test_env.env_method(
                    method_name="save_asset_memory")
                actions_memory = test_env.env_method(
                    method_name="save_action_memory")
            if dones[0]:
                self.logger.info("hit end!")
                break
        return account_memory[0], actions_memory[0]

    def rnn_prediction(self, model: Union[Model, Any], 
                       environment: StockTradingEnvPrivate, 
                       rnn_test_ndarray: ndarray) -> Tuple:
        """make a prediction
        
        Args:
            model:
            environment:
            rnn_test_ndarray:
        
        Returns:
            account_memory:
            actions_memory:
        """

        test_env, test_obs = environment.get_sb_env()
        account_memory = []
        actions_memory = []
        test_env.reset()
        # self.logger.debug(f"len of daily test df: {len(environment.df)}")
        # self.logger.debug(f"type of environment.df: {type(environment.df)}")
        # self.logger.debug(f"len of rnn_test_ndarray: {len(rnn_test_ndarray)}")
        # self.logger.debug(f"type of rnn_test_ndarray: {type(rnn_test_ndarray)}")
        days = environment.df.index.unique()
        # self.logger.debug(f"days: {days}")
        for day_idx in days:
            # self.logger.debug(f"day_idx: {day_idx}")
            day = environment.day
            # self.logger.debug(f"day: {day}")
            obs = rnn_test_ndarray[day:day+1]
            # self.logger.debug(f"type of obs: {type(obs)}")
            # self.logger.debug(f"obs: {obs}")
            # self.logger.debug(f"environment.df.loc[day_idx]: {environment.df.loc[day_idx]}")
            if day+1 < len(rnn_test_ndarray):
                scaled_nextdayprice = rnn_test_ndarray[day+1][-1][-1]
                # self.logger.debug(f"scaled_nextdayprice: {scaled_nextdayprice}")
                # screen_input()
            else:
                scaled_nextdayprice = None
            actions = model.predict(obs, scaled_nextdayprice)
            # self.logger.debug(f"actions: {actions}")
            # self.logger.debug(f"1type of actions: {type(actions)}")
            # actions = np.asarray([actions])
            test_obs, rewards, dones, info = test_env.step(actions)
            if day_idx == days[-2]:
                account_memory = test_env.env_method(
                    method_name="save_asset_memory")
                actions_memory = test_env.env_method(
                    method_name="save_action_memory")
            if dones[0]:
                self.logger.info("hit end!")
                break
        
        self.logger.info(f"account_memory: {account_memory}, type: {type(account_memory)}")
        self.logger.info(f"actions_memory: {actions_memory}, type: {type(actions_memory)}")
        return account_memory[0], actions_memory[0], info
