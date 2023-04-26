from ontology.cards import CardSuit, CardFace
from ontology.elements import Card
from util.repository import root_resource


def card2path(card: Card) -> str:
    filename = "{}-{}.png".format(card.suit.name, card.face.name_())
    return root_resource + filename

def str2path(s:str) -> str:
    return "{}{}.png".format(root_resource,s)


def card2img():
    pass
