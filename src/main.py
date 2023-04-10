# -*- coding: utf-8 -*-
import threading

from core.game import FullObsGame
from core.game_manager import GameManager
from core.rule import NaiveFxxkLandLord
from user_interface.GUI_manager import GUIFactory, UI_types
from agent.naive_agent import NaiveAgent
from agent.minimax_agent import MiniMaxAgent
from agent.greedy_agent import GreedyAgent


def main():
    rule = NaiveFxxkLandLord()
    game = FullObsGame(rule)
    game.sleep_time = 2
    game_manager = GameManager()
    gui_factory = GUIFactory()
    gui = gui_factory.getGUIObject(UI_types.PyQt)
    game_manager.setGame(game)
    game_manager.setGUI(gui, "lord")
    # for name in ["lord", "farmer_1", "farmer_2"]:
    #     game_manager.setAgent(NaiveAgent(), name)
    # for name in ["farmer_1", "farmer_2"]:
    #     game_manager.setAgent(NaiveAgent(), name)
    # game_manager.setAgent(MiniMaxAgent(player_name="lord",depth=10),"lord")
    for name in ["farmer_1", "farmer_2"]:
        game_manager.setAgent(MiniMaxAgent(name, depth=10), name)
    # game_manager.setAgent(NaiveAgent(),"lord")
    game_manager.setAgent(GreedyAgent(), "lord")
    thread = threading.Thread(target=game.run)
    thread.start()
    gui.mainloop()


if __name__ == "__main__":
    main()
