from core.game import FullObsGame
from core.game_manager import GameManager
from core.rule import NaiveFxxkLandLord
from user_interface.GUI_manager import GUIFactory, UI_types
from agent.naive_agent import NaiveAgent


def main():
    rule = NaiveFxxkLandLord()
    game = FullObsGame(rule)
    game_manager = GameManager()
    gui_factory = GUIFactory()
    gui = gui_factory.getGUIObject(UI_types.PyQt)
    game_manager.setGame(game)
    game_manager.setGUI(gui, "lord")
    for name in ["lord", "farmer_1", "farmer_2"]:
        game_manager.setAgent(NaiveAgent(), name)
