# -*- coding: utf-8 -*-
from abc import ABC
import random

import torch

from ontology.elements import CardSuit, CardFace, Card


class Rule(ABC):
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
        :param player_state:
        :param current_player:
        :return:  next state, next player;is end
        """
        pass

    @classmethod
    def player_encode(cls):
        # "start" always encode to zero
        pass


class NaiveFxxkLandLord(Rule):
    def __init__(self, seed: int = 0):
        self.seed = seed
        # without joker
        self.cards = [
            Card(suit=CardSuit(i), face=CardFace(j))
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
            "farmer1": shuffle_index[18:18 + 17],
            "farmer2": shuffle_index[18 + 17:18 + 17 + 17]
        }

        return deal

    def judge(self, player_state: dict, current_player, hands) -> tuple:
        assert player_state[current_player] == "ongoing"
        if "pass_1" in player_state.values():
            two_passed = True
        else:
            two_passed = False
        if "pass_0" in player_state.values():
            one_passed = True
        else:
            one_passed = False
        if len(hands[current_player]) == 0:
            if two_passed:
                player_state[current_player] = "pass_2"
            elif one_passed:
                player_state[current_player] = "pass_1"
                two_passed = True
            else:
                player_state[current_player] = "pass_0"

        if two_passed or player_state["lord"] != "ongoing":
            is_end = True
        else:
            is_end = False
        if is_end:
            return player_state, current_player, is_end
        if current_player == "lord":
            if player_state["farmer1"] == "ongoing":
                next_player = "farmer1"
            else:
                next_player = "farmer2"
        elif current_player == "farmer1":
            if player_state["farmer2"] == "ongoing":
                next_player = "farmer2"
            else:
                next_player = "lord"
        else:
            assert player_state["lord"] == "ongoing"
            next_player = "lord"
        return player_state, next_player, is_end

    def first_player(self):
        return "lord"
