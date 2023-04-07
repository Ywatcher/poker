from abc import ABC


class AbstractGUI(ABC):
    def __init__(self):
        self.get_observation=None
        self.get_history=None
        self.get_game_info=None

    @classmethod
    def mainloop(cls):
        pass

    @classmethod
    def set_hands(cls):
        pass

    # @classmethod
    # def set_
    # todo: events
