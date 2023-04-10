# -*- coding: utf-8 -*-
from abc import ABC


class AbstractGUI(ABC):
    def __init__(self, is_observer=False):
        self.is_observer = is_observer

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

    def observe_history(self, history_buffer):
        history_buffer.add_observer(self)

    def observe_observation(self, obs):  # todo
        obs.add_observer(self)

    # @classmethod
    def as_observer(self) -> bool:
        """
        :return: whether self behaves as an observer; if the return value is true, \
        then the game manager will set self as an observer to game obs, history and \
        info during initialization
        todo: now it only deals with game history, need to handle obs and info in the future
        """
        return self.is_observer
