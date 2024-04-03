"""_summary_
"""

import copy
import os
import sys
from typing import List, Any, Tuple, Optional


import matplotlib.pyplot as plt
import numpy as np
import pygame
from ding.envs import BaseEnv, BaseEnvTimestep
from ding.utils import ENV_REGISTRY
from ditk import logging
from easydict import EasyDict
from gymnasium import spaces

from zoo.board_games.mcts_bot import MCTSBot


@ENV_REGISTRY.register("mpad")
class MPADEnv(BaseEnv):
    config = dict(
        # (str) The name of the environment registered in the environment registry.
        env_id="Connect4",
        # (str) The mode of the environment when take a step.
        battle_mode="self_play_mode",
        # (str) The mode of the environment when doing the MCTS.
        battle_mode_in_simulation_env="self_play_mode",
        # (str) The render mode. Options are 'None', 'state_realtime_mode', 'image_realtime_mode' or 'image_savefile_mode'.
        # If None, then the game will not be rendered.
        render_mode=None,
        # (str or None) The directory in which to save the replay file. If None, the file is saved in the current directory.
        replay_path=None,
        # (str) The type of the bot of the environment.
        bot_action_type="rule",
        # (bool) Whether to let human to play with the agent when evaluating. If False, then use the bot to evaluate the agent.
        agent_vs_human=False,
        # (float) The probability that a random agent is used instead of the learning agent.
        prob_random_agent=0,
        # (float) The probability that an expert agent(the bot) is used instead of the learning agent.
        prob_expert_agent=0,
        # (float) The probability that a random action will be taken when calling the bot.
        prob_random_action_in_bot=0.0,
        # (float) The scale of the render screen.
        screen_scaling=9,
        # (bool) Whether to use the 'channel last' format for the observation space. If False, 'channel first' format is used.
        channel_last=False,
        # (bool) Whether to scale the observation.
        scale=False,
        # (float) The stop value when training the agent. If the evalue return reach the stop value, then the training will stop.
        stop_value=2,
    )

    @classmethod
    def default_config(cls: type) -> EasyDict:
        cfg = EasyDict(copy.deepcopy(cls.config))
        cfg.cfg_type = cls.__name__ + "Dict"
        return cfg

    def __init__(self, cfg: dict = None) -> None:
        # load the conifguration
        self.cfg = cfg

        # Set the format of the observation.
        self.channel_last = self.cfg.channel_last
        self.scale = cfg.scale

        # Set the parameters about replay render.
        self.screen_scaling = cfg.screen_scaling
        # options = {None, 'state_realtime_mode', 'image_realtime_mode', 'image_savefile_mode'}
        self.render_mode = cfg.render_mode
        self.replay_name_suffix = "test"
        self.replay_path = cfg.replay_path
        self.replay_format = "gif"
        self.screen = None
        self.frames = []

        # Set the mode of interaction between the agent and the environment.
        # options = {'self_play_mode', 'play_with_bot_mode', 'eval_mode'}
        self.battle_mode = cfg.battle_mode
        assert self.battle_mode in ["self_play_mode", "play_with_bot_mode", "eval_mode"]
        # The mode of MCTS is only used in AlphaZero.
        self.battle_mode_in_simulation_env = "self_play_mode"

        # In ``eval_mode``, we can choose to play with the agent.
        self.agent_vs_human = cfg.agent_vs_human

        self.prob_random_agent = cfg.prob_random_agent
        self.prob_expert_agent = cfg.prob_expert_agent
        assert (self.prob_random_agent >= 0 and self.prob_expert_agent == 0) or (
            self.prob_random_agent == 0 and self.prob_expert_agent >= 0
        ), f"self.prob_random_agent:{self.prob_random_agent}, self.prob_expert_agent:{self.prob_expert_agent}"

        # The board state is saved as a one-dimensional array instead of a two-dimensional array for ease of computation in ``step()`` function.
        self.board = [0] * (6 * 7)

        # Changes to match Anomoly Detection
        self.players = [1]
        self._current_player = 1
        self._env = self

        # Set the bot type and add some randomness.
        # options = {'rule, 'mcts'}
        self.bot_action_type = cfg.bot_action_type
        self.prob_random_action_in_bot = cfg.prob_random_action_in_bot
        if self.bot_action_type == "mcts":
            cfg_temp = EasyDict(cfg.copy())
            cfg_temp.save_replay = False
            cfg_temp.bot_action_type = None
            env_mcts = MPADEnv(EasyDict(cfg_temp))
            self.mcts_bot = MCTSBot(env_mcts, "mcts_player", 50)
        elif self.bot_action_type == "rule":
            self.rule_bot = MPADEnv(self, self._current_player)

        # Render the beginning state of the game.
        if self.render_mode is not None:
            self.render(self.render_mode)

    
    # Define the legal actions
    @property
    def legal_actions(self) -> List[int]:
        return [i for i in range(2) if self.board[i] == 0]
    
    def _player_step(self, action: int, flag: int) -> BaseEnvTimestep:
        """
        Overview:
            A function that implements the transition of the environment's state. \
            After taking an action in the environment, the function transitions the environment to the next state \
            and returns the relevant information for the next time step.
        Arguments:
            - action (:obj:`int`): A value from 0 to 1 indicating the prediction to make .
            - flag (:obj:`str`): A marker indicating the source of an action, for debugging convenience.
        Returns:
            - timestep (:obj:`BaseEnvTimestep`): A namedtuple that records the observation and obtained reward after taking the action, \
            whether the game is terminated, and some other information. 
        """
        if action in self.legal_actions:
            piece = self.players.index(self._current_player) + 1
            for i in list(filter(lambda x: x % 2 == action, list(range(1, -1, -1)))):
                if self.board[i] == 0:
                    self.board[i] = piece
                    break
        else:
            print(np.array(self.board).reshape(6, 7))
            logging.warning(
                f"You input illegal action: {action}, the legal_actions are {self.legal_actions}. "
                f"flag is {flag}."
                f"Now we randomly choice a action from self.legal_actions."
            )
            action = self.random_action()
            print("the random action is", action)
            piece = self.players.index(self._current_player) + 1
            for i in list(filter(lambda x: x % 7 == action, list(range(41, -1, -1)))):
                if self.board[i] == 0:
                    self.board[i] = piece
                    break

        # Check if there is a winner.
        done, winner = self.get_done_winner()
        if not winner == -1:
            reward = np.array(1).astype(np.float32)
        else:
            reward = np.array(0).astype(np.float32)

        info = {}

        self._current_player = self.next_player

        obs = self.observe()

        # Render the new step.
        if self.render_mode is not None:
            self.render(self.render_mode)
        if done:
            info['eval_episode_return'] = reward
            if self.render_mode == 'image_savefile_mode':
                self.save_render_output(replay_name_suffix=self.replay_name_suffix, replay_path=self.replay_path,
                                        format=self.replay_format)

        return BaseEnvTimestep(obs, reward, done, info)


    def reset(self):
        return self.env.reset()

    def step(self, action):
        return self.env.step(action)

    def render(self, mode="human"):
        return self.env.render(mode)

    def close(self):
        return self.env.close()

    def seed(self, seed=None):
        return self.env.seed(seed)

    def __del__(self):
        self.close()
