# -*- coding: utf-8 -*-
import torch
from torch.nn import functional as F
from ontology.cards import CardSuit, CardFace


class Card:
    def __init__(self, suit: CardSuit, face: CardFace):
        self.suit = suit
        self.face = face
        self.value = self.face.value * 4 + self.suit.value
        # self.location = location

    def encode(self) -> torch.Tensor:
        tensor = torch.tensor([self.value], dtype=torch.int64)
        return F.one_hot(tensor, num_classes=52)

    def __hash__(self):
        return self.value

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __str__(self):
        return "{}-{}".format(self.suit.name_()[0], self.face.name_())

    def __repr__(self):
        return "{}-{}".format(self.suit.name_(), self.face.name_())

class CardSet:
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards: list[Card] = list(cards)

    def to_tensor(self):
        return sum([card.encode() for card in self.cards])

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return "[" + ", ".join([str(c) for c in self.cards]) + "]"

    def __repr__(self):
        return "CardSet(" + self.__str__() + ")"

    def sort(self, reverse: bool = False):
        self.cards.sort(reverse=reverse)

    def __getitem__(self, item):
        return self.cards[item]


class Hand(CardSet):

    def __init__(self, cards=None):
        super(Hand, self).__init__(cards=cards)
        self.id = None

    def append(self, cards: []):
        self.cards += cards

    def remove(self, cards: []):
        for card in cards:
            self.cards.remove(card)

    def copy(self) -> "Hand":
        return Hand(cards=self.cards.copy())


class UnknownHand:
    def __init__(self, nr_cards:int):
        self.id = None
        self.nr_cards = nr_cards

    def __len__(self):
        return self.nr_cards


class Action(CardSet):
    def __init__(self, player, cards, tag):
        super(Action, self).__init__(cards)
        self.player = player
        self.tag = tag

    def __str__(self):
        return "player: {}, ".format(self.player) + super(Action, self).__str__()

    def __repr__(self):
        return "Action("+self.__str__()+")"

    def copy(self) -> "Action":
        return Action(
            player=self.player,
            cards=self.cards.copy(),
            tag=self.tag
        )


class FoldAction(Action):
    # when starting game
    def __init__(self, player, upon: Action = None):
        super(FoldAction, self).__init__(player=player, cards=None, tag="fold")
        self.upon = upon


if __name__ == "__main__":
    card_Q = Card(suit=CardSuit.spade, face=CardFace.Q)
    card_K = Card(suit=CardSuit.spade, face=CardFace.K)
    state = Hand(cards=[card_K, card_Q])
    print(state.to_tensor())
