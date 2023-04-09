# -*- coding: utf-8 -*-
from typing import Union

import torch
from torch.nn import functional as F

from ontology.elements import Hand, Action, CardSet, UnknownHand
from core.rule import Rule


class GameObs:
    def __init__(
            self,
            hands: dict[str, Union[Hand, UnknownHand]],
            your_own_hand: dict[str, Hand],
            last_action: Action,
            nr_players: int,  # number of all players; including passed players; used for encoding
            encoder: Rule.PlayerEncoder):
        self.nr_players = nr_players
        self.hands = hands
        self.your_own_hand = your_own_hand
        self.last_action = last_action
        self.encoder = encoder

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
        super(FullGameObs, self).__init__(
            hands,
            your_own_hand,
            last_action,
            nr_players,
            encoder
        )

    def encode(self):
        """
        :return: tuple of three tensors: hands; own hand; and last action
        """
        pass


class PartialGameObs(GameObs):
    pass
