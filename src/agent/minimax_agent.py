# -*- coding: utf-8 -*-
import numpy as np

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

    def action(self, obs: FullGameObs, legal_actions: list[Action], player_state: dict) -> Action:
        player_hand = {}
        for p in obs.hands:
            player_hand.update({p: obs.hands[p].copy()})
        for p in obs.your_own_hand:
            player_hand.update({p: obs.your_own_hand[p].copy()})
        player_to_go = self.name
        for turn in range(self.search_depth):
            pass  # todo

    class GameSearchState:
        def __init__(
                self,
                player,
                player_state,
                player_hands,
                last_action,
                is_end
        ):
            self.player = player
            self.player_state = player_state
            self.player_hands = player_hands
            self.last_action = last_action
            self.is_end = is_end

    class MinimaxNode:
        def __init__(
                self,
                # player_hands: dict[str:Hand],
                parent: "MiniMaxAgent.MinimaxNode",
                game_state: "MiniMaxAgent.GameSearchState",
                # lastAction: Action,
                costdif: float,
                # player: str,
                # player_state: dict,
                problem: "MiniMaxAgent.MiniMaxSearchProblem",
                # is_end:bool,
                # max_depth:int
        ):
            self.parent: "MiniMaxAgent.MinimaxNode" = parent
            self.costdif = costdif
            self.depth: int = 0
            self.problem = problem
            if parent is not None:
                self.depth = parent.depth + 1
            self.expanded = False
            self.__children: list["MiniMaxAgent.MinimaxNode"] = []
            self.game_state = game_state
            self.traversed = False
            self.score = 0
            self.best_child: "MiniMaxAgent.MinimaxNode" = None

        def is_leaf(self):
            return self.depth == self.problem.max_depth or self.game_state.is_end

        # def get_successors(self):

        def __expand(self):
            self.expanded = True
            if self.is_leaf():
                assert False
            else:
                successors = self.problem.get_successors(self.game_state)
                self.__children = set(
                    MiniMaxAgent.MinimaxNode(
                        game_state=succ,
                        parent=self,
                        costdif=0,  # fixme
                        problem=self.problem
                    )
                    for succ in successors
                )

                # costdif = 0  # fixme
                #
                # succ = MiniMaxAgent.MinimaxNode(
                #     lastAction=action,
                #     player_state=next_player_state,
                #     player_hands=next_player_hand,
                #     parent=self,
                #     player=next_player,
                #     costdif=costdif,
                #     rule=self.rule,
                #     is_end=is_end,
                #     max_depth=self.max_depth
                # )
                # self.__children.append(succ)

        def get_children(self):
            if not self.expanded:
                self.__expand()
            return self.__children

        def minimax(self, alpha: float, beta: float) -> tuple[float, float, float]:
            """
            pruning condition: alpha >= beta
            :param alpha: best for maximizer for pruning
            :param beta: best for minimizer for pruning
            :return: (updated alpha, updated beta, self's minimax score)
            """
            self.traversed = True
            if self.is_leaf():
                self.score = 0  # fixme: assign with func
                return alpha, beta, self.score
            else:
                if len(self.get_children()) == 0:
                    assert 0
                    self.score = - np.inf
                    return alpha, beta, self.score
                if self.problem.is_to_maximize(self.game_state.player):  # for minimizer
                    maxEva = -np.inf
                    for child in self.get_children():
                        alpha, beta, eva = child.minimax(alpha, beta)
                        if eva > maxEva:
                            self.best_child = child
                            maxEva = eva
                            # i.e. maxEva = max(maxEva, eva)
                        alpha_ = max(maxEva, alpha)
                        if beta <= alpha:  # prune
                            break
                        alpha = alpha_
                    self.score = maxEva
                    return alpha, beta, self.score
                else:  # for maximizer
                    minEva = np.inf
                    for child in self.get_children():
                        alpha, beta, eva = child.minimax(alpha, beta)
                        if eva < minEva:
                            self.best_child = child
                            minEva = eva
                            # i.e. minEva = min(minEva, eva)
                        beta_ = min(beta, minEva)
                        if beta_ <= alpha:  # prune
                            break
                        beta = beta_
                    self.score = minEva
                    return alpha, beta, self.score

        def get_best_action(self) -> Action:
            assert self.traversed
            return self.best_child.game_state.last_action

    class MiniMaxSearchProblem:
        def __init__(
                self,
                max_depth: int,
                ret_depth: int,
                starting_search_state: "MiniMaxAgent.GameSearchState",
                rule: Rule
        ):
            self.max_depth = max_depth
            self.ret_depth = min(ret_depth, max_depth)
            # self.starting_player_state = starting_player_state
            # self.starting_player = starting_player
            # self.starting_player_hands = starting_player_hand
            self.rule = rule
            # self.last_action = last_action
            self.starting_search_state = starting_search_state

        def get_successors(
                self,
                search_state: "MiniMaxAgent.GameSearchState"
        ):
            legal_actions = self.rule.legal_actions(
                last_action=search_state.last_action,
                own_hand=search_state.player_hands[search_state.player],
                player_name=search_state.player,
                player_state=search_state.player_state
            )
            successors = []
            assert len(legal_actions) != 0
            for action in legal_actions:
                next_player_hand = {
                    p: search_state.player_hands[p].copy()
                    for p in search_state.player_hands
                }
                next_player_hand[search_state.player].remove(action.cards)
                next_player, next_player_state, is_end = self.rule.judge(
                    search_state.player_state,
                    search_state.player,
                    next_player_hand
                )
                successors.append((
                    next_player,
                    next_player_state,
                    search_state.player_hands,
                    action
                ))
                successors.append(MiniMaxAgent.GameSearchState(
                    player=next_player,
                    player_hands=next_player_hand,
                    player_state=next_player_state,
                    last_action=action,
                    is_end=is_end
                ))
            return successors

        def is_goal_state(self, game_state: "MiniMaxAgent.GameSearchState"):
            if game_state.is_end and \
                    self.starting_search_state.player in self.rule.get_winner(game_state.player_state):
                return True
            else:
                return False

        def is_to_maximize(self, player: str) -> bool:
            pass

        # def get_actions_minimax(self, root: "MinimaxNode"):
