# -*- coding: utf-8 -*-
from core.observation import GameObs
from ontology.elements import Action


class Agent:
    def __init__(self, name: str, is_human=True):
        self.name = name
        self.is_human = is_human

    def action(self, obs: GameObs, legal_actions: list[Action]) -> Action:
        pass
