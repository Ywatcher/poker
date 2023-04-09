# -*- coding: utf-8 -*-
from agent.abstract_agent import Agent
from core.rule import Rule, NaiveFxxkLandLord
from ontology.elements import Hand, Action
from core.game import GameObs, FullGameObs


class MiniMaxAgent(Agent):
    # for fully obs FxxkLandLord
    # reward:
    # the size of opponent's hand -
    # the size of opponent's legal actions(without fold) -
    # the size of own hand

    # class GameSimulator:
    #     def __init__(self, rule:Rule):
    #         self.rule = rule
    #
    #     def update(self, ):

    def __init__(self, name: str):
        super().__init__(name)
        self.rule = NaiveFxxkLandLord()
        # 1 for max, -1 for min
        if self.name == "lord":
            self.min_max_dict = {
                "lord": 1,
                "farmer_1": -1,
                "farmer_2": -1
            }
        else:
            self.min_max_dict = {
                "lord": -1,
                "farmer_1": 1,
                "farmer_2": 1
            }
        self.search_depth = 10


    def reward_each_step(self, player_hand: dict[str, Hand], action: Action):
        pass

    def action(self, obs: FullGameObs, legal_actions: list[Action], player_state:dict) -> Action:
        player_hand = {}
        for p in obs.hands:
            player_hand.update({p: obs.hands[p].copy()})
        for p in obs.your_own_hand:
            player_hand.update({p: obs.your_own_hand[p].copy()})
        current_player = self.name
        for turn in range(self.search_depth):
            pass # todo
