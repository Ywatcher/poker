# -*- coding: utf-8 -*-

import sys
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from user_interface.AbstractGUI import AbstractGUI
from core.observation import GameObs, FullGameObs
from core.game import GameInfo


class QtGUI(AbstractGUI):
    def __init__(self):
        super(QtGUI, self).__init__()
        self.app = QApplication(sys.argv)
        self.win = self.Window()
        self.backendthread = QThread()
        self.backend = QtGUI.BackendThread()
        self.backend.update_.connect(self.win.handleDisplayDuringGame)
        self.backend.moveToThread(self.backendthread)
        self.backendthread.started.connect(self.backend.run)

    def set_func_get_observation(self, f):
        self.backend.get_observation = f

    def set_func_get_history(self, f):
        self.backend.get_history = f

    def set_func_get_game_info(self, f):
        self.backend.get_game_info = f

    class BackendThread(QObject):

        update_ = pyqtSignal(GameObs, GameInfo)

        def __init__(self):
            super(QtGUI.BackendThread, self).__init__()

        def run(self):
            while True:
                for i in range(1, 11):
                    # print("here")
                    game_info = self.get_game_info()
                    # print(game_info)
                    if not game_info.is_started:
                        # print("not yet")
                        pass
                    elif not game_info.is_ended:
                        # print("started")
                        pass
                        self.update_.emit(self.get_observation(), game_info)
                        time.sleep(0.1)
                    else:
                        pass

        def get_observation(self) -> GameObs:
            pass

        def get_game_info(self) -> GameInfo:
            pass

        def get_history(self):
            pass

    class Window(QDialog):
        def __init__(self):
            super(QtGUI.Window, self).__init__()
            self.setWindowTitle("hhh")
            self.resize(1024, 768)
            self.input = QLabel(self)
            self.input.resize(400, 100)

        def handleDisplayDuringGame(self, obs: GameObs, info: GameInfo):
            self.input.setText(str(obs.nr_players) + info.current_player_name)

        def handleDisplayBeforeGame(self):
            pass

    def mainloop(self):
        self.backendthread.start()
        self.win.show()
        # print("here")
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    gui = QtGUI()
    gui.mainloop()
