# -*- coding: utf-8 -*-
from abc import ABC

from agent.abstract_agent import Agent
from ontology.elements import Hand, Action, FoldAction
from rule import Rule
from observation import GameObs, FullGameObs


class GameRecordsBuffer:
    def __init__(self):
        self.rounds = 0
        self.buffer: list[Action] = []

    def add_record(self, record: Action):
        self.rounds += 1
        self.buffer.append(record)


class Game(ABC):
    def __init__(self, rule):
        self.rule = rule
        self.hands: dict[str, Hand] = {
            p: None for p in rule.player_list()
        }
        # record of game
        self.log = GameRecordsBuffer()
        # discarded cards
        self.player_states = rule.init_state()
        self.player_hands: dict[str, Hand] = {}
        self.is_end = False
        self.player_observations = {}
        self.info = None
        self.player_agents: dict[str, Agent] = {}
        # self.table_cards = set()

    def set_agent(self, agent: Agent, player_name: str):
        self.player_agents.update({player_name: agent})

    def run(self):
        self.player_hands = {
            p: Hand(self.rule.deal()[p])
            for p in self.rule.player_list()
        }
        # no bet
        current_player_name = self.rule.first_player()
        self.update_observations(action=FoldAction("start"))
        while not self.is_end:
            obs = self.get_observation(player_name=current_player_name)
            # play
            action = self.player_agents[current_player_name].action(obs)
            self.update_observations(action)
            self.player_states, current_player_name, self.is_end = self.rule.judge(
                self.player_states, current_player_name, self.player_hands
            )

    @classmethod
    def update_observations(cls, action: Action):
        pass

    def get_observation(self, player_name: str) -> GameObs:
        return self.player_observations[player_name]


class FullObsGame(Game):
    def __init__(self, rule: Rule):
        super(FullObsGame, self).__init__(rule)

    def update_observations(self, action: Action):
        self.player_observations = {
            player_name: FullGameObs(
                hands={p: self.hands[p] for p in self.player_hands.keys() if p != player_name},
                your_own_hand=self.player_hands[player_name],
                last_action=action,
                nr_players=len(self.player_states)
            ) for player_name in self.player_states.keys()
        }
