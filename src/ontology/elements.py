import torch
from torch.nn import functional as F
from ontology.cards import CardSuit, CardFace


# class Location:
#     pass
#
#
# class Pile(Location):
#     def __init__(self):
#         pass


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


class CardSet:
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards: list[Card] = list(cards)

    def to_tensor(self):
        return sum([card.encode() for card in self.cards])

    def __len__(self):
        return len(self.cards)


class Hand(CardSet):

    def __init__(self, cards=None):
        super(Hand, self).__init__(cards=cards)
        self.id = None

    def append(self, cards: []):
        self.cards += cards

    def remove(self, cards: []):
        for card in cards:
            self.cards.remove(card)


class Action(CardSet):
    def __init__(self, player, cards):
        super(Action, self).__init__(cards)
        self.player = player


class FoldAction(Action):
    # when starting game
    def __init__(self,player):
        super(FoldAction, self).__init__(player=player, cards=None)


# class


if __name__ == "__main__":
    card_Q = Card(suit=CardSuit.spade, face=CardFace.Q)
    card_K = Card(suit=CardSuit.spade, face=CardFace.K)
    state = Hand(cards=[card_K, card_Q])
    print(state.to_tensor())
