# -*- coding: utf-8 -*-
import time
from abc import ABC

from agent.abstract_agent import Agent
from ontology.elements import Hand, Action, FoldAction
from core.rule import Rule
from core.observation import GameObs, FullGameObs
from util.observer import Event


class GameRecordsBuffer:
    def __init__(self):
        self.rounds = 0
        self.buffer: list[Action] = []
        self.observers = []

    def add_record(self, record: Action):
        self.rounds += 1
        self.buffer.append(record)
        self.notify(Event(
            event_type=Event.Type.updateHistory,
            record=record
        ))

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify(self, event:Event):
        for observer in self.observers:
            observer.update_as_observer(event)


class GameInfo:
    def __init__(self, is_started, is_ended, current_player_name=None):
        self.is_started = is_started
        self.is_ended = is_ended
        self.current_player_name = current_player_name
        self.iter = 0

    def __repr__(self):
        return "is started: {}, is ended: {} current player: {}".format(
            self.is_started, self.is_ended, self.current_player_name
        )


class Game(ABC):

    def __init__(self, rule):
        self.rule = rule
        self.player_encoder = rule.get_encoder()
        # self.hands: dict[str, Hand] = {
        #     p: None for p in rule.player_list()
        # }
        # record of game
        self.log = GameRecordsBuffer()
        # discarded cards
        self.player_states = rule.init_state()
        self.player_hands: dict[str, Hand] = {}
        self.player_observations = {}
        self.info = GameInfo(is_started=False, is_ended=False)
        self.player_agents: dict[str, Agent] = {}
        self.observers = []
        self.sleep_time=0

    def add_game_obs_observer(self, observer, player_name):
        self.observers.append((observer,player_name))

    def notify(self, events:dict[str,Event]):
        # print("not")
        for observer,player in self.observers:
            observer.update_as_observer(events[player])


    def set_agent(self, agent: Agent, player_name: str):
        self.player_agents.update({player_name: agent})

    def run(self):
        self.player_hands = {
            p: Hand(self.rule.deal()[p])
            for p in self.rule.player_list()
        }
        # no bet
        self.info.current_player_name = self.rule.first_player()
        last_action = FoldAction("start")
        self.update_observations(action=last_action)
        self.info.is_started = True
        time.sleep(self.sleep_time)
        while not self.info.is_ended:
            obs = self.get_observation(player_name=self.info.current_player_name)
            # play
            legal_actions = self.rule.legal_actions(
                last_action=last_action,
                player_name=self.info.current_player_name,
                own_hand=self.player_hands[self.info.current_player_name],
                player_state=self.player_states
            )
            action = self.player_agents[self.info.current_player_name].action(obs, legal_actions,
                                                                              self.player_states.copy())
            self.update_state(action)
            self.update_observations(action)
            self.player_states, self.info.current_player_name, self.info.is_ended = self.rule.judge(
                self.player_states, self.info.current_player_name, self.player_hands
            )
            self.info.iter = self.info.iter + 1
            last_action = action
        print("end, winner:", self.rule.get_winner(player_state=self.player_states))
        # self.update_state(last_action)
        self.update_observations(last_action)

    @classmethod
    def update_observations(cls, action: Action):
        pass

    def get_observation(self, player_name: str) -> GameObs:
        return self.player_observations[player_name]

    @classmethod
    def update_state(cls, action: Action):
        pass


class FullObsGame(Game):
    def __init__(self, rule: Rule):
        super(FullObsGame, self).__init__(rule)

    def update_observations(self, action: Action):
        self.player_observations = {
            player_name: FullGameObs(
                hands={p: self.player_hands[p].copy() for p in self.player_hands.keys() if p != player_name},
                your_own_hand={player_name: self.player_hands[player_name].copy()},
                last_action=action,
                nr_players=len(self.player_states),
                encoder=self.player_encoder
            ) for player_name in self.player_states.keys()
        }
        self.notify(events=
            {p:Event(
                event_type=Event.Type.updateObs,
                obs=self.player_observations[p],
                current_player=action.player
            ) for p in self.player_observations}
        )

    def update_state(self, action: Action):
        current_player = action.player
        self.player_hands[current_player].remove(cards=action.cards)
        self.log.add_record(record=action)
        print(action, action.tag)
        print(self.player_hands)


class PartialObsGame(Game):
    pass
