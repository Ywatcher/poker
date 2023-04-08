# -*- coding: utf-8 -*-
from abc import ABC
import random

import torch

from ontology.elements import CardSuit, CardFace, Card, Action, Hand, FoldAction, CardSet


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
    single = "single"
    suited = "suited"
    three = "3"
    three_plus_1 = "3+1"
    three_plus_2 = "3+2"
    bomb = "bomb"
    four_plus_2 = "4+2"
    straight = "straight"

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

        self.search_dict = {
            self.single: self.search_single,
            self.suited: self.search_suited,
            self.three: self.search_three,
            self.three_plus_1: self.search_three_plus_1,
            self.three_plus_2: self.search_three_plus_2,
            self.bomb: self.search_bomb,
            self.four_plus_2: self.search_four_plus_2,
            self.straight: self.search_straight
        }

    def all_cards(self) -> set[Card]:
        return set(self.cards)

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
        # nr_card_for_each_player = [18, 17, 17]
        deal = {
            "lord": [self.cards[i] for i in shuffle_index[0:18]],
            "farmer_1": [self.cards[i] for i in shuffle_index[18:18 + 17]],
            "farmer_2": [self.cards[i] for i in shuffle_index[18 + 17:18 + 17 + 17]]
        }
        return deal

    def judge(self, player_state: dict, current_player, hands) -> tuple:
        assert player_state[current_player] == "on_going"
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
        own_hand.sort()
        if isinstance(last_action, FoldAction):
            action_fold_upon = last_action.upon
            print("last was fold upon", action_fold_upon)
            if last_action.player == "start" or action_fold_upon.player == player_name:
                # call
                # cannot fold
                actions = []
                for tag in self.search_dict.keys():
                    actions += [Action(player=player_name, cards=c, tag=tag)
                                for c in self.search_dict[tag](own_hand)]
                return actions
            else:
                return self.legal_actions(
                    last_action=action_fold_upon,
                    own_hand=own_hand,
                    player_name=player_name
                )
        else:
            # follow
            if last_action.tag in self.search_dict:
                actions = [
                    Action(player=player_name, cards=c, tag=last_action.tag)
                    for c in self.search_dict[last_action.tag](own_hand, greater_than=last_action)
                ]
            else:
                assert False
            actions.append(FoldAction(player=player_name, upon=last_action))
            return actions

    # functions below: assume sorted
    @staticmethod
    def search_single(card_set: CardSet, greater_than: Action = None) -> list[CardSet]:
        # print(type(card_set))
        if greater_than is not None:
            last_action_card = greater_than[0]
            return [
                CardSet([card]) for card in card_set.cards if card > last_action_card
            ]
        else:
            return [
                CardSet([card]) for card in card_set.cards
            ]

    @staticmethod
    def search_suited(card_set: CardSet, greater_than: Action = None) -> list[CardSet]:
        nr_cards = len(card_set)
        if greater_than is not None:
            last_action_card = greater_than[0]
            return [
                CardSet([card_set[i], card_set[i + 1]]) for i in range(nr_cards - 1)
                if card_set[i] > last_action_card and
                   card_set[i].face == card_set[i + 1].face
            ]
        else:
            return [
                CardSet([card_set[i], card_set[i + 1]]) for i in range(nr_cards - 1)
                if card_set[i].face == card_set[i + 1].face
            ]

    @staticmethod
    def search_three(card_set: CardSet, greater_than: Action = None) -> list[CardSet]:
        nr_cards = len(card_set)
        if greater_than is not None:
            last_action_card = greater_than[0]
            return [
                CardSet(card_set.cards[i:i + 3]) for i in range(nr_cards - 2)
                if card_set[i] > last_action_card and
                   card_set[i].face == card_set[i + 2].face
            ]
        else:
            return [
                CardSet(card_set.cards[i:i + 3]) for i in range(nr_cards - 2)
                if card_set[i].face == card_set[i + 2].face
            ]

    @staticmethod
    def search_three_plus_1(card_set: CardSet, greater_than: Action = None) -> list[CardSet]:
        nr_cards = len(card_set)
        if greater_than is not None:
            paired_value = NaiveFxxkLandLord.get_paired_value(greater_than, pair_size=3)
            return [CardSet(
                card_set.cards[i:i + 3] + [card_set[j]]
            ) for i in range(nr_cards - 2) for j in range(nr_cards)
                if card_set[i].face > paired_value and
                   card_set[i].face == card_set[i + 2].face and
                   card_set[i].face != card_set[j].face
            ]
        else:
            return [CardSet(
                card_set.cards[i:i + 3] + [card_set[j]]
            ) for i in range(nr_cards - 2) for j in range(nr_cards)
                if card_set[i].face == card_set[i + 2].face and
                   card_set[i].face != card_set[j].face
            ]

    @staticmethod
    def search_three_plus_2(card_set: CardSet, greater_than: Action = None) -> list[CardSet]:
        nr_cards = len(card_set)
        if greater_than is not None:
            paired_value = NaiveFxxkLandLord.get_paired_value(greater_than, pair_size=3)
            return [CardSet(
                card_set.cards[i:i + 3] + card_set.cards[j:j + 2]
            ) for i in range(nr_cards - 2) for j in range(nr_cards - 1)
                if card_set[i].face > paired_value and
                   card_set[i].face == card_set[i + 2].face and
                   card_set[j].face == card_set[j + 1].face and
                   card_set[i].face != card_set[j].face
            ]
        else:
            return [CardSet(
                card_set.cards[i:i + 3] + card_set.cards[j:j + 2]
            ) for i in range(nr_cards - 2) for j in range(nr_cards - 1)
                if card_set[i].face == card_set[i + 2].face and
                   card_set[j].face == card_set[j + 1].face and
                   card_set[i].face != card_set[j].face
            ]

    @staticmethod
    def search_bomb(card_set: CardSet, greater_than: Action = None) -> list[CardSet]:
        nr_cards = len(card_set)
        if greater_than is not None:
            last_action_card = greater_than[0]
            return [CardSet(
                card_set.cards[i:i + 4]
            ) for i in range(nr_cards - 3)
                if card_set[i].face == card_set[i + 3].face and
                   card_set[i] > last_action_card
            ]
        else:
            return [CardSet(
                card_set.cards[i:i + 4]
            ) for i in range(nr_cards - 3)
                if card_set[i].face == card_set[i + 3].face
            ]

    @staticmethod
    def search_four_plus_2(card_set: CardSet, greater_than: Action = None) -> list[CardSet]:
        nr_cards = len(card_set)
        if greater_than is not None:
            paired_value = NaiveFxxkLandLord.get_paired_value(greater_than, pair_size=4)
            return [CardSet(
                card_set.cards[i:i + 4] + card_set.cards[j:j + 2]
            ) for i in range(nr_cards - 3) for j in range(nr_cards - 1)
                if card_set[i].face == card_set[i + 3].face and
                   card_set[i].face > paired_value and
                   card_set[i].face != card_set[j].face and
                   card_set[j].face == card_set[j + 1].face
            ]
        else:
            return [CardSet(
                card_set.cards[i:i + 4] + card_set.cards[j:j + 2]
            ) for i in range(nr_cards - 3) for j in range(nr_cards - 1)
                if card_set[i].face == card_set[i + 3].face and
                   card_set[i].face != card_set[j].face and
                   card_set[j].face == card_set[j + 1].face
            ]

    @staticmethod
    def search_straight(card_set: CardSet, greater_than: Action = None) -> list[CardSet]:
        # prune the search space since there are no difference among the four suits
        # min: 34567
        # max: 10JQKA
        suit_eliminated = [
            card_set[i] for i in range(len(card_set))
            if i == 0 or card_set[i] > card_set[i - 1] and
               card_set[i].face != CardFace._2
        ]
        nr_faces = len(suit_eliminated)
        if greater_than is not None:
            size_of_straight = len(greater_than)
            return [
                CardSet(suit_eliminated[i:i + size_of_straight])
                for i in range(nr_faces - size_of_straight + 1)
                if suit_eliminated[i] > greater_than[0] and
                   suit_eliminated[i] + size_of_straight - 1 == suit_eliminated[i + size_of_straight - 1]
            ]
        else:
            valid_sets = []
            for size_of_straight in range(5, nr_faces + 1):
                valid_set_of_this_size = [
                    CardSet(suit_eliminated[i:i + size_of_straight]) for i in range(nr_faces - size_of_straight + 1)
                    if
                    suit_eliminated[i].value + size_of_straight - 1 == suit_eliminated[i + size_of_straight - 1].value
                ]
                if len(valid_set_of_this_size) == 0:
                    break
                valid_sets += valid_set_of_this_size
            return valid_sets

    @staticmethod
    def get_paired_value(card_set: CardSet, pair_size: int) -> CardFace:
        face_values = [
            card.face for card in card_set.cards
        ]
        for face in list(set(face_values)):
            if face_values.count(face) == pair_size:
                return face
        assert False


