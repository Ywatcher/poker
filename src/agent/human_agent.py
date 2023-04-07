# -*- coding: utf-8 -*-
from agent.abstract_agent import Agent
from user_interface import AbstractGUI


class HumanAgent(Agent):
    def __init__(self):
        super().__init__(name="human", is_human=True)
        self.interfaces = {"GUI": None, "CLI": None}

    def set_gui(self, interface: AbstractGUI):
        self.interfaces["GUI"] = interface
