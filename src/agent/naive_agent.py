# -*- coding: utf-8 -*-
import time

from core.game import Action
from agent.abstract_agent import Agent
from core.observation import GameObs


class NaiveAgent(Agent):
    def __init__(self):
        super().__init__(name="naive", is_human=False)

    def action(self, obs: GameObs, legal_actions: list[Action]) -> Action:
        time.sleep(1)
        # return legal_actions[0]


