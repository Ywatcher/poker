# -*- coding: utf-8 -*-
from enum import Enum
from torch.nn import functional as F


class CardFace(Enum):
    _3 = 0
    _4 = 1
    _5 = 2
    _6 = 3
    _7 = 4
    _8 = 5
    _9 = 6
    _10 = 7
    J = 8
    Q = 9
    K = 10
    A = 11
    _2 = 12

    def name_(self) -> str:
        return self.name.strip('_')

    def __le__(self, other):
        return self.value<=other.value

    def __lt__(self, other):
        return self.value<other.value


class CardSuit(Enum):
    spade = 0  # "Spade"
    heart = 1  # "Heart"
    club = 2  # "Club"
    diamond = 3  # "Diamond"

    def name_(self) -> str:
        # if self == 0:
        #     return "Spade"
        # elif self == 1:
        #     return "Heart"
        # elif self == 2:
        #     return "Club"
        # else:
        #     return "Diamond"

        return self.name[0].capitalize() + self.name[1:]


if __name__ == "__main__":
    spade = CardSuit.spade
    print(spade.value)
    for i in range(13):
        f = CardFace(i)
        print(f.name)
    print(CardSuit(1))
