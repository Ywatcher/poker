# -*- coding: utf-8 -*-
from user_interface.AbstractGUI import AbstractGUI

from user_interface.QtGUI import QtGUI

# from utils import global_config


class UI_types:
    NONE = "DoNothingGUI"
    NaiveTkinter = "NaiveTkinterGUI"
    PyQt = "PyQt"
    CML = "CML_GUI"
    ALL_TYPES = [NaiveTkinter, NONE, CML, PyQt]


class GUIFactory:

    def __init__(
            self,
            # config: global_config.GlobalConfigTable
    ):
        self.__tk_root = None
        # self.__config = config

    def getGUIObject(self, ui_type: str) -> AbstractGUI:
        assert ui_type in UI_types.ALL_TYPES
        UI = None
        if ui_type == UI_types.PyQt:
            # self.__tk_root = tk.Tk()
            UI = QtGUI()
            # UI = NaiveTkinterGUI(self.__tk_root, self.__config)

        # elif ui_type == UI_types.CML:
        #     UI = CML_GUI(self.__config)

        return UI
