# -*- coding: utf-8 -*-
import sys
import time
# from builtins import function
from typing import Union

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (
    QWidget, QApplication, QSizePolicy, QLabel,
    QFrame, QVBoxLayout, QHBoxLayout, QSplitter,
    QScrollArea, QMainWindow
)

from user_interface.AbstractGUI import AbstractGUI
from core.observation import GameObs, FullGameObs
from core.game import GameInfo, GameRecordsBuffer
from user_interface.graphic_util import card2path
from ontology.cards import CardSuit, CardFace
from ontology.elements import Card, CardSet, Action
from util.repository import root_resource

# todo: garbage collect


class QtGUI(AbstractGUI):
    def __init__(self):
        super(QtGUI, self).__init__(is_observer=True)
        self.app = QApplication(sys.argv)
        self.win = self.Window()
        self.backendthread = QThread()
        self.backend = QtGUI.BackendThread()
        self.backend.update_.connect(self.win.handleDisplayDuringGame)
        self.backend.moveToThread(self.backendthread)
        self.backendthread.started.connect(self.backend.run)

    def mainloop(self):
        self.win.history_field.history = self.backend.get_history()
        self.backendthread.start()
        self.win.show()
        sys.exit(self.app.exec_())

    def set_func_get_observation(self, f):
        """
        :param f: function, this function is used for getting game obs generally, \
        regardless of whether self behaves like an observer
        """
        self.backend.get_observation = f

    def set_func_get_history(self, f):
        """
        :param f: function, this function is used for getting game history generally, \
        regardless of whether self behaves like an observer
        """
        self.backend.get_history = f

    def set_func_get_game_info(self, f):
        """
        :param f: function, this function is used for getting game info generally, \
        regardless of whether self behaves like an observer
        """
        self.backend.get_game_info = f

    def update_as_observer(self, record: Action):
        self.win.history_field.update_once(record)

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

        def get_history(self) -> GameRecordsBuffer:
            pass

    class CardSetWidget(QWidget):

        pass

    # class HistoryCardSetWidget(QWidget):
    #     pass

    class ObsCardSetWigdet(QWidget):
        def __init__(self, parent, name, pixmap: dict[str, QPixmap]):
            super(QtGUI.ObsCardSetWigdet, self).__init__(parent)
            self.buffer_len = 24
            # self.h_ = 128
            self.w_label = 64
            # self.w_ = 68*self.buffer_len + self.w_label
            # self.setFixedHeight(self.h_)
            # self.setFixedWidth(self.w_)
            self.card_set = CardSet()
            self.name = name
            self.pixmap = pixmap
            self.hbox = QHBoxLayout(self)

            self.name_widget = QWidget(self)
            # QWidget.setSizePolicy()
            self.name_vb = QVBoxLayout(self.name_widget)

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
            self.name_widget.setFixedWidth(self.w_label)

            # self.name_label.setFixedWidth(64)
            self.card_set_buffer = []

            for id_pos in range(self.buffer_len):
                self.card_set_buffer.append(QLabel(self))
                self.hbox.addWidget(self.card_set_buffer[-1])
            self.setLayout(self.hbox)
            self.is_current = False

        def update(self) -> None:
            for c in range(self.buffer_len):
                if c < len(self.card_set):
                    card = self.card_set[c]
                    self.card_set_buffer[c].setPixmap(self.pixmap[str(card)])
                else:
                    self.card_set_buffer[c].clear()
            super(QtGUI.ObsCardSetWigdet, self).update()

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

        def set_label_font(self, font: QFont):
            self.name_label.setFont(font)

        def set_player_name(self, player_name: str):
            self.name = player_name
            self.name_label.setText(self.name)

    class ObsField(QFrame):

        def initUI(self):
            vbox = QVBoxLayout(self)
            splitter = QSplitter(Qt.Vertical)
            self.widget_top = QWidget(self)
            vbox_top = QVBoxLayout(self.widget_top)
            self.widget_bot = QWidget(self)
            self.player_frames = {
                p: QtGUI.ObsCardSetWigdet(parent=self, name=p, pixmap=self.pixmap) for p in self.player_names
            }

            for p in self.player_names:
                vbox_top.addWidget(self.player_frames[p])
            splitter.addWidget(self.widget_top)
            splitter.addWidget(self.widget_bot)
            # self.bottom_field = QFrame
            vbox.addWidget(splitter)
            self.setLayout(vbox)
            self.widget_top.setMaximumHeight(128 * self.nr_players)
            self.setMaximumWidth(1300)

        def __init__(self, pixmap, parent=None):
            super(QtGUI.ObsField, self).__init__(parent)
            self.pixmap = pixmap
            self.nr_players = 3
            self.player_names = [  # fixme: to decouple
                "lord", "farmer_1", "farmer_2"
            ]
            self.player_frames: dict[str, QtGUI.ObsCardSetWigdet] = None
            self.initUI()

        def update(self, obs: GameObs, current_player: str):
            # update own hand:
            for p in self.player_names:
                if p == current_player:
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

    class HistoryField(QMainWindow):

        def initUI(self):
            self.vbox = QVBoxLayout(self)
            # self.setLayout(self.vbox)
            self.scroll_widget.setLayout(self.vbox)
            self.scroll_area.setWidget(self.scroll_widget)
            self.setCentralWidget(self.scroll_area)
            # self.scroll_area.sev

        def __init__(self, pixmap, parent=None):
            # super(QtGUI.HistoryField, self).__init__(parent)
            # QFrame.__init__(parent)
            # QMainWindow.__init__(parent)
            super(QtGUI.HistoryField, self).__init__(parent)
            self.scroll_area = QScrollArea(self)
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.scroll_area.setWidgetResizable(True)

            self.scroll_widget = QWidget()

            # self.scroll_area.resize(self.width(),self.height())
            # todo to smoothen scroll area
            self.pixmap = pixmap
            self.history: GameRecordsBuffer = None  # initialized at the start of mainloop
            self.buffer_size = 128
            self.widgets_buffer = [
                QtGUI.ObsCardSetWigdet(
                    parent=self,
                    pixmap=self.pixmap,
                    name=""
                ) for i in range(self.buffer_size)
            ]
            vertical_policy = QSizePolicy()
            vertical_policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
            for widget in self.widgets_buffer:
                # widget.setVerticalPolicy(QSizePolicy.Policy.Fixed)
                widget.setSizePolicy(vertical_policy)
            self.buffer_top = 0

            self.initUI()

        def update_once(self, record: Action):
            self.widgets_buffer[self.buffer_top].set_player_name("{}:{}".format(self.buffer_top,record.player))
            self.widgets_buffer[self.buffer_top].set_cardset(record)
            self.vbox.addWidget(self.widgets_buffer[self.buffer_top])
            self.widgets_buffer[self.buffer_top].update()
            self.buffer_top += 1
            self.update()

    class Window(QWidget):

        def initUI(self):
            hbox = QHBoxLayout(self)
            topbar = QFrame(self)
            topbar.setFrameShape(QFrame.StyledPanel)

            mainleft = QtGUI.ObsField(pixmap=self.pixmap, parent=self)
            mainleft.setFrameShape(QFrame.StyledPanel)
            self.obs_field = mainleft
            mainright = QtGUI.HistoryField(pixmap=self.pixmap, parent=self)
            # mainright.setFrameShape(QFrame.StyledPanel)
            mainright.setStyleSheet(
                "background-color:green"
            )
            self.history_field = mainright

            splitter1 = QSplitter(Qt.Horizontal)
            splitter1.addWidget(mainleft)
            splitter1.addWidget(mainright)

            splitter2 = QSplitter(Qt.Vertical)
            splitter2.addWidget(topbar)
            splitter2.addWidget(splitter1)
            topbar.setFixedHeight(32)

            hbox.addWidget(splitter2)
            self.setLayout(hbox)

            self.setGeometry(30, 30, self.w, self.h)

        def __init__(self):
            super().__init__()
            self.setWindowTitle("poker")
            self.w = 1024 * 2
            self.h = 768 * 2
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
