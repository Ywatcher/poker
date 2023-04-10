# -*- coding: utf-8 -*-
from core.game import Game
from agent.abstract_agent import Agent
from agent.human_agent import HumanAgent
from user_interface import AbstractGUI


class GameManager:
    def __init__(self):
        self.game = None
        self.guis = {}
        self.clis = {}

    def setGame(self, game: Game):
        self.game = game

    def setGUI(self, GUI: AbstractGUI, player_name):
        self.guis.update({player_name: GUI})
        # print("setting")
        GUI.set_func_get_observation(f=lambda: self.game.get_observation(player_name))
        GUI.set_func_get_history(f=lambda: self.game.log)
        GUI.set_func_get_game_info(f=lambda: self.game.info)
        if GUI.as_observer():
            self.game.log.add_observer(GUI)

    def setAgent(self, agent: Agent, player_name):
        self.game.set_agent(agent=agent, player_name=player_name)
        if agent.is_human:
            assert isinstance(agent, HumanAgent)
            agent.set_gui(self.guis[player_name])
