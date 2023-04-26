# -*- coding: utf-8 -*-
from abc import ABC
from agent.abstract_agent import Agent
from core.observation import GameObs
from core.rule import Rule, NaiveFxxkLandLord
from core.game import FullGameObs
from ontology.elements import Action


class UnitedAgent(Agent, ABC):
    class SubAgent(Agent):
        def __init__(self, name, superAgent: "UnitedAgent", idx: int):
            super(UnitedAgent.SubAgent, self).__init__(name=name, is_human=False)
            self.super_agent = superAgent
            self.idx = idx

        def action(
                self,
                obs: GameObs,
                legal_actions: list[Action],
                player_state: dict
        ) -> Action:
            self.super_agent.decide(obs, legal_actions, player_state, self.idx)
            return self.super_agent.getAction(self.idx)

    # for farmers
    def __init__(self):
        super(UnitedAgent, self).__init__(name="united", is_human=False)
        self.farmer_1_agent = self.SubAgent(name="farmer_1_sub", superAgent=self, idx=1)
        self.farmer_2_agent = self.SubAgent(name="farmer_2_sub", superAgent=self, idx=2)
        self.to_act: list[Action, Action] = []

    def subAgents(self) -> tuple[Agent, Agent]:
        return self.farmer_1_agent, self.farmer_2_agent

    def decide(self, obs, legal_actions, player_state, idx: int):
        # if subagent calling this function is the first remaining farmer, then update action list;
        # else keep the list;
        if idx == self.remaining_first_player(player_state):
            self.to_act = self.decide_func(obs,legal_actions)
        else:
            return

    def getAction(self, idx: int) -> Action:
        # get the action for subagent from store action list
        return self.to_act[idx - 1]

    @staticmethod
    def remaining_first_player(player_state:dict) -> int:
        if player_state["farmer_1"] == "on_going":
            return 1
        else:
            return 2

    @classmethod
    def decide_func(cls,obs:GameObs, legal_actions:list[Action]) -> list[Action,Action]:
        # to implement in concrete classes
        pass


class TestUnitedAgent(UnitedAgent):
    pass
