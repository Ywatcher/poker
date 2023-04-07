# -*- coding: utf-8 -*-
from abc import ABC
import random

import torch

from ontology.elements import CardSuit, CardFace, Card, Action, Hand


class Rule(ABC):
    class PlayerEncoder(ABC):
        def encode(self, player_name: str) -> torch.Tensor:
            pass

    @classmethod
    def get_encoder(cls) -> "Rule.PlayerEncoder":
        return cls.PlayerEncoder()

    @classmethod
    def all_cards(cls) -> set[Card]:
        pass

    @classmethod
    def get_init_state(cls, *args) -> list[Card]:
        pass

    @classmethod
    def deal(cls) -> dict:
        pass

    @classmethod
    def player_list(cls) -> list:
        pass

    @classmethod
    def player_states(cls) -> list:
        pass

    @classmethod
    def init_state(cls) -> dict:
        pass

    @classmethod
    def first_player(cls):
        pass

    @classmethod
    def judge(cls, player_state, current_player, hands) -> tuple:
        """
        judge after each player plays
        :param hands:
        :param player_state:
        :param current_player:
        :return:  next state, next player;is end
        """
        pass

    @classmethod
    def legal_actions(cls, last_action: Action, own_hand: Hand, player_name: str) -> list[Action]:
        pass


class NaiveFxxkLandLord(Rule):
    class PlayerEncoder(Rule.PlayerEncoder):
        def __init__(self):
            self.dict = {
                "start": torch.Tensor([0., 0., 0.]),
                "lord": torch.Tensor([1., 0., 0.]),
                "farmer_1": torch.Tensor([0., 1., 0.]),
                "farmer_2": torch.Tensor([0., 0., 1.])
            }

        def encode(self, player_name: str) -> torch.Tensor:
            return self.dict[player_name]

    def __init__(self, seed: int = 0):
        self.seed = seed
        # without joker
        self.cards = [
            Card(suit=CardSuit(j), face=CardFace(i))
            for i in range(13) for j in range(4)
        ]
        self.nr_cards = 52
        # 3 player_hands
        # landlord: the agent (forced assignment)
        self.players = ["lord", "farmer_1", "farmer_2"]
        self.nr_players = 3
        self.states = [
            "on_going", "pass_0", "pass_1", "pass_2"
        ]
        self._init_state = {
            p: "on_going" for p in self.players
        }

    def player_list(self) -> list:
        return self.players

    def player_states(self) -> list:
        return self.states

    def init_state(self) -> dict:
        return self._init_state

    def deal(self) -> dict:
        shuffle_index = list(range(self.nr_cards))
        random.seed(self.seed)
        random.shuffle(shuffle_index)
        nr_card_for_each_player = [18, 17, 17]
        deal = {
            "lord": shuffle_index[0:18],
            "farmer_1": shuffle_index[18:18 + 17],
            "farmer_2": shuffle_index[18 + 17:18 + 17 + 17]
        }

        return deal

    def judge(self, player_state: dict, current_player, hands) -> tuple:
        # print(player_state)
        assert player_state[current_player] == "on_going"
        if "pass_1" in player_state.values():
            # print("1pass")
            two_passed = True
        else:
            # print("2pass")
            two_passed = False
        if "pass_0" in player_state.values():
            # print("1pass")
            one_passed = True
        else:
            one_passed = False
        # print(1)
        if len(hands[current_player]) == 0:
            # print("he")
            if two_passed:
                player_state[current_player] = "pass_2"
            elif one_passed:
                player_state[current_player] = "pass_1"
                two_passed = True
            else:
                player_state[current_player] = "pass_0"
        if two_passed or player_state["lord"] != "on_going":
            is_end = True
        else:
            is_end = False
        if is_end:
            return player_state, current_player, is_end
        if current_player == "lord":
            if player_state["farmer_1"] == "on_going":
                next_player = "farmer_1"
            else:
                next_player = "farmer_2"
        elif current_player == "farmer_1":
            if player_state["farmer_2"] == "on_going":
                next_player = "farmer_2"
            else:
                next_player = "lord"
        else:
            assert player_state["lord"] == "on_going"
            next_player = "lord"
        return player_state, next_player, is_end

    def first_player(self):
        return "lord"

    def legal_actions(
            self,
            last_action: Action,
            own_hand: Hand,
            player_name: str
    ) -> list[Action]:
        # todo
        pass
