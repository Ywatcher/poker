# -*- coding: utf-8 -*-
from abc import ABC


class AbstractGUI(ABC):
    # def __init__(self):

    @classmethod
    def mainloop(cls):
        pass

    @classmethod
    def set_func_get_observation(cls, f):
        pass

    @classmethod
    def set_func_get_history(cls, f):
        pass

    @classmethod
    def set_func_get_game_info(cls, f):
        pass

    @classmethod
    def set_hands(cls):
        pass

    # @classmethod
    # def set_
    # todo: events
