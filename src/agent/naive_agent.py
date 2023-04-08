# -*- coding: utf-8 -*-
import time
import random

from core.game import Action
from agent.abstract_agent import Agent
from core.observation import GameObs


class NaiveAgent(Agent):
    def __init__(self):
        super().__init__(name="naive", is_human=False)

    def action(self, obs: GameObs, legal_actions: list[Action]) -> Action:
        time.sleep(1)
        # return legal_actions[0]
        # print("legal actions",legal_actions)
        index = random.randint(0,len(legal_actions)-1)
        # print("index",index)
        return legal_actions[index]

