if __name__ == "__main__":
    from ontology.elements import Card,CardFace
    card = Card(suit=None,face=CardFace.Joker,is_wild_card=True)
    print(str(card))
