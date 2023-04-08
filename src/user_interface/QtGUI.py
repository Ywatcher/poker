# -*- coding: utf-8 -*-

import sys
import time
from typing import Union

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from user_interface.AbstractGUI import AbstractGUI
from core.observation import GameObs, FullGameObs
from core.game import GameInfo
from user_interface.graphic_util import card2path
from ontology.cards import CardSuit, CardFace
from ontology.elements import Card, CardSet
from util.repository import root_resource


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

        # self.mainloop()

    def mainloop(self):
        self.backendthread.start()
        self.win.show()
        # print("here")
        sys.exit(self.app.exec_())

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

    class CardSetWigdet(QWidget):
        def __init__(self, parent, name, pixmap: dict[str, QPixmap]):
            super(QtGUI.CardSetWigdet, self).__init__(parent)
            self.card_set = CardSet()
            self.name = name
            self.pixmap = pixmap
            self.hbox = QHBoxLayout(self)

            self.name_widget = QWidget(self)
            self.name_vb = QVBoxLayout(self)

            # name and dot
            self.name_label = QLabel(self)
            self.dot_label = QLabel(self)
            self.name_vb.addWidget(self.name_label)
            self.name_vb.addWidget(self.dot_label)
            self.name_widget.setLayout(self.name_vb)
            self.hbox.addWidget(self.name_widget)
            self.name_label.setText(self.name)
            self.name_label.setFont(QFont('Arial', 9))
            self.dot_label.setPixmap(self.pixmap["grey-dot"])

            # self.name_label.setFixedWidth(64)
            self.card_set_buffer = []
            self.buffer_len = 24
            for id_pos in range(self.buffer_len):
                self.card_set_buffer.append(QLabel(self))
                self.hbox.addWidget(self.card_set_buffer[-1])
            self.setLayout(self.hbox)
            self.is_current = False

        def update(self) -> None:
            # todo : marker for current player
            for c in range(self.buffer_len):  # todo : no pixmap for pos > len
                if c < len(self.card_set):
                    card = self.card_set[c]
                    self.card_set_buffer[c].setPixmap(self.pixmap[str(card)])
                else:
                    self.card_set_buffer[c].clear()
            super(QtGUI.CardSetWigdet, self).update()

        def set_cardset(self, cardset: Union[CardSet, list[Card]]):
            if cardset is not None:
                self.card_set = cardset
            else:
                self.card_set = CardSet()

        def set_current(self, is_current: bool):
            self.is_current = is_current
            if is_current:
                self.dot_label.setPixmap(self.pixmap["red-dot"])
            else:
                self.dot_label.setPixmap(self.pixmap["grey-dot"])

        # def set_label_size(self, size):
        #     pass

        def set_label_font(self, font):
            pass

    class ObsField(QFrame):

        def initUI(self):
            vbox = QVBoxLayout(self)
            splitter = QSplitter(Qt.Vertical)
            self.widget_top = QWidget(self)
            vbox_top = QVBoxLayout(self.widget_top)
            self.widget_bot = QWidget(self)
            self.player_frames = {
                p: QtGUI.CardSetWigdet(parent=self, name=p, pixmap=self.pixmap) for p in self.player_names
            }
            for p in self.player_names:
                vbox_top.addWidget(self.player_frames[p])
            splitter.addWidget(self.widget_top)
            splitter.addWidget(self.widget_bot)
            # self.bottom_field = QFrame
            vbox.addWidget(splitter)
            self.setLayout(vbox)

        def __init__(self, pixmap, parent=None):
            super(QtGUI.ObsField, self).__init__(parent)
            self.pixmap = pixmap
            self.nr_players = 3
            self.player_names = [  # fixme: to decouple
                "lord", "farmer_1", "farmer_2"
            ]
            self.player_frames: dict[str, QtGUI.CardSetWigdet] = None
            self.initUI()

        def update(self, obs: FullGameObs, current_player:str):
            # update own hand:
            for p in self.player_names:
                if p== current_player:
                    self.player_frames[p].set_current(True)
                else:
                    self.player_frames[p].set_current(False)
            for p in obs.your_own_hand:  # todo : add marker for current action
                if obs.your_own_hand[p] is not None:
                    self.player_frames[p].set_cardset(cardset=obs.your_own_hand[p].cards)

                self.player_frames[p].update()
            for p in obs.hands:
                if obs.hands[p] is not None:
                    self.player_frames[p].set_cardset(cardset=obs.hands[p].cards)

                self.player_frames[p].update()

    class Window(QWidget):

        def initUI(self):
            hbox = QHBoxLayout(self)
            topbar = QFrame(self)
            topbar.setFrameShape(QFrame.StyledPanel)

            mainleft = QtGUI.ObsField(pixmap=self.pixmap, parent=self)
            mainleft.setFrameShape(QFrame.StyledPanel)
            self.obs_field = mainleft
            mainright = QFrame(self)
            mainright.setFrameShape(QFrame.StyledPanel)
            mainright.setStyleSheet(
                "background-color:green"
            )

            splitter1 = QSplitter(Qt.Horizontal)
            splitter1.addWidget(mainleft)
            splitter1.addWidget(mainright)

            splitter2 = QSplitter(Qt.Vertical)
            splitter2.addWidget(topbar)
            splitter2.addWidget(splitter1)
            topbar.setFixedHeight(32)

            # splitter2.setStretchFactor(10,10)
            hbox.addWidget(splitter2)
            self.setLayout(hbox)

            self.setGeometry(30, 30, self.w, self.h)
            # topbar.resize(self.w, 32)

        def __init__(self):
            super().__init__()
            self.setWindowTitle("poker")
            self.w = 1024
            self.h = 768
            self.resize(self.w, self.h)
            self.card_png_path = {}
            for suit_val in range(4):
                for face_val in range(13):
                    card = Card(suit=CardSuit(suit_val), face=CardFace(face_val))
                    self.card_png_path.update({str(card): card2path(card)})
            self.card_pixmap = {
                key: QPixmap(self.card_png_path[key]) for key in self.card_png_path.keys()
            }
            self.dot_pixmap = {
                "grey-dot": QPixmap(root_resource + "grey-dot.png"),
                "red-dot": QPixmap(root_resource + "red-dot.png")
            }
            self.pixmap = {}
            self.pixmap.update(self.card_pixmap)
            self.pixmap.update(self.dot_pixmap)
            self.initUI()

        def handleDisplayDuringGame(self, obs: GameObs, info: GameInfo):
            self.obs_field.update(obs, info.current_player_name)

        def handleDisplayBeforeGame(self):
            pass


if __name__ == "__main__":
    gui = QtGUI()
    gui.mainloop()
