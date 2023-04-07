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
        GUI.get_observation = lambda s: self.game.get_observation(player_name)
        GUI.get_history = lambda s: self.game.log
        GUI.get_game_info = lambda s: self.game.info

    def setAgent(self, agent:Agent, player_name):
        self.game.set_agent(agent=agent,player_name=player_name)
        if agent.is_human:
            assert isinstance(agent, HumanAgent)
            agent.set_gui(self.guis[player_name])

