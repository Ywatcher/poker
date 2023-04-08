# -*- coding: utf-8 -*-
import torch
from torch.nn import functional as F

from ontology.elements import Hand, Action, CardSet
from core.rule import Rule


class GameObs:
    def __init__(self):
        pass

    @classmethod
    def encode(cls):
        pass


class FullGameObs(GameObs):
    def __init__(
            self,
            hands: dict[str, Hand],
            your_own_hand: dict[str, Hand],
            last_action: Action,
            nr_players: int,
            encoder: Rule.PlayerEncoder
    ):
        super(FullGameObs, self).__init__()
        self.nr_players = nr_players
        self.hands = hands
        self.your_own_hand = your_own_hand
        self.last_action = last_action
        self.encoder = encoder

    def encode(self):
        """
        :return: tuple of three tensors: hands; own hand; and last action
        """
        pass


class PartialGameObs(GameObs):
    pass
