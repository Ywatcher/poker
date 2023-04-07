import torch
from torch.nn import functional as F

from ontology.elements import Hand, Action, CardSet


class GameObs:
    def __init__(self):
        pass

    @classmethod
    def encode(cls):
        pass


class FullGameObs(GameObs):
    def __init__(self, hands: dict[str, Hand], your_own_hand: Hand, last_action: Action, nr_players:int):
        super(FullGameObs, self).__init__()
        self.nr_players = nr_players
        self.hands = hands
        self.your_own_hand = your_own_hand
        self.last_action = last_action

    def encode(self):
        pass
