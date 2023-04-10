# -*- coding: utf-8 -*-
from agent.abstract_agent import Agent
from core.observation import GameObs
from ontology.elements import Action


class GreedyAgent(Agent):
    def __init__(self):
        super(GreedyAgent, self).__init__(name="greedy", is_human=False)

    def heuristic(self, action: Action):
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
        return [action for action in legal_actions if len(action)==max_length][0]

