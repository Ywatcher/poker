# -*- coding: utf-8 -*-
from agent.abstract_agent import Agent
from core.observation import GameObs
from core.rule import Rule, NaiveFxxkLandLord
from core.game import FullGameObs
from ontology.elements import Action


class FullObsGreedyAgent(Agent):
    def __init__(self, player_name: str):
        super(FullObsGreedyAgent, self).__init__(name="greedy", is_human=False)
        self.player_name = player_name
        self.rule = NaiveFxxkLandLord()

    def heuristic(self, obs: FullGameObs, action: Action) -> float:
        if self.player_name == "lord":
            return self.heuristic_of_landlord(obs, action)
        elif self.player_name == "farmer_1":
            return self.heuristic_of_farmer1(obs, action)
        elif self.player_name == "farmer_2":
            return self.heuristic_of_farmer2(obs, action)
        else:
            assert 0

    def heuristic_of_landlord(self, obs, action: Action) -> float:
        # legal actions of farmer1 == 0
        # legal actions of farmer2 == 0 if farmer1 fold
        # legal actions of farmer2 == 0 if farmer1 not fold
        # then good action
        # self need not to fold if farmer1 or farmer2 follow
        # or bad action
        # if bad action, then h(a) = -inf
        # beside use length of self action as h(a)
        pass

    def heuristic_of_farmer1(self, obs, action: Action) -> float:
        # legal actions of lord == 0 no matter what
        pass

    def heuristic_of_farmer2(self, obs, action: Action) -> float:
        # lord must fold
        pass

    def action(
            self,
            obs: GameObs,
            legal_actions: list[Action],
            player_state: dict
    ) -> Action:
        action_lengths = set(
            len(action) for action in legal_actions
        )
        max_length = max(action_lengths)
        return [action for action in legal_actions if len(action) == max_length][0]
