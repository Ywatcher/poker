# -*- coding: utf-8 -*-

import torch
from torch import nn

from agent.abstract_agent import Agent
from core.observation import FullGameObs
from ontology.elements import Action

from util.repository import root_model


class FullObsDeepQAgent(Agent):
    # for fully obs FxxkLandLord

    class Decider(nn.Module):
        class FcObsEncoder(nn.Module):
            pass

        class FcQ(nn.Module):
            pass

        def __init__(self):
            super(FullObsDeepQAgent.Decider, self).__init__()
            # in:
            # from opponent hands -> hidden1
            # from self hands -> hidden2
            # from each possible action -> hidden3
            # using convolution?

            # out:
            # hidden1 || hidden2 || hidden3 -> Q score
            # training :

        def encode_obs(self, opponent_hands: torch.Tensor, self_hand: torch.Tensor) -> torch.Tensor:
            pass

        def Q(self, obs_encoding: torch.Tensor, action: torch.Tensor) -> torch.Tensor:
            pass

    def __init__(self, player_name: str):
        super(FullObsDeepQAgent, self).__init__(name="full obs Q", is_human=False)
        self.decider = FullObsDeepQAgent.Decider()
        self.player_name = player_name

    def action(
            self,
            obs: FullGameObs,
            legal_actions: list[Action],
            player_state: dict
    ) -> Action:
        pass

    def load_model(self, tag: str):
        pass

    def save_model(self, tag: str):
        pass


def trainFullObsDeepQAgent():
    pass


if __name__ == "__main__":
    trainFullObsDeepQAgent()
