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

    def __init__(self, player_name: str, depth: int = 10):
        super().__init__(name="minimax", is_human=False)
        self.player_name = player_name
        self.rule = NaiveFxxkLandLord()
        # 1 for max, -1 for min

        self.search_depth = depth
        self.search_problem = MiniMaxAgent.MiniMaxSearchProblem(
            max_depth=self.search_depth,
            player=self.player_name,
            rule=self.rule
        )

    def reward_each_step(self, player_hand: dict[str, Hand], action: Action):
        pass

    def action(self, obs: FullGameObs, legal_actions: list[Action], player_state: dict) -> Action:
        player_hand = {}
        for p in obs.hands:
            player_hand.update({p: obs.hands[p].copy()})
        for p in obs.your_own_hand:
            player_hand.update({p: obs.your_own_hand[p].copy()})
        starting_state = MiniMaxAgent.GameSearchState(
            player=self.player_name,
            player_state=player_state,
            player_hands=player_hand,
            last_action=None,
            legal_actions=legal_actions
        )
        root = MiniMaxAgent.MinimaxNode(
            parent=None,
            game_state=starting_state,
            costdif=0,
            problem=self.search_problem
        )
        root.minimax(alpha=-np.inf, beta=np.inf)
        return root.get_best_action()

    class GameSearchState:
        def __init__(
                self,
                player,
                player_state,
                player_hands,
                last_action=None,
                legal_actions=None,
                is_end=False
        ):
            self.player = player
            self.player_state = player_state
            self.player_hands = player_hands
            self.last_action = last_action
            self.legal_actions = legal_actions
            self.is_end = is_end

        def __repr__(self):
            return "GameSearchState(\nplayer: {}, player state: {}, \nplayer hand: {},\nlast_action: {}, is_end: {}\n)".format(
                self.player, self.player_state, self.player_hands, self.last_action, self.is_end
            )

    class MinimaxNode:
        def __init__(
                self,
                parent: "MiniMaxAgent.MinimaxNode",
                game_state: "MiniMaxAgent.GameSearchState",
                costdif: float,
                problem: "MiniMaxAgent.MiniMaxSearchProblem",
        ):
            assert isinstance(game_state, MiniMaxAgent.GameSearchState)
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

        def __expand(self):
            self.expanded = True
            if self.is_leaf():  # __expand() will not be called (in minimax()) if the node is a leaf
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
                self.score = self.problem.score(self.game_state)
                return alpha, beta, self.score
            else:
                if len(self.get_children()) == 0:  # not possible for this problem
                    assert 0
                    # self.score = - np.inf
                    # return alpha, beta, self.score
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
            assert self.best_child.game_state.last_action is not None
            return self.best_child.game_state.last_action

    class MiniMaxSearchProblem:
        def __init__(
                self,
                max_depth: int,
                # ret_depth: int,
                player: str,
                rule: Rule
        ):
            self.max_depth = max_depth
            self.rule = rule
            self.player = player
            if self.player == "lord":
                self.min_max_dict = {
                    "lord": 1,
                    "farmer_1": -1,
                    "farmer_2": -1
                }
                self.score = self.score_of_lord
            else:
                self.min_max_dict = {
                    "lord": -1,
                    "farmer_1": 1,
                    "farmer_2": 1
                }
                self.score = self.score_of_farmer
            # self.factor_opponent_choices = 1
            self.factor_opponent_cards = 1
            self.factor_team_cards = 10
            self.factor_win = 500
            self.factor_lose = -100

        def get_successors(
                self,
                search_state: "MiniMaxAgent.GameSearchState"
        ) -> list["MiniMaxAgent.GameSearchState"]:
            if search_state.legal_actions is None:
                assert search_state.last_action is not None
                legal_actions = self.rule.legal_actions(
                    last_action=search_state.last_action,
                    own_hand=search_state.player_hands[search_state.player],
                    player_name=search_state.player,
                    player_state=search_state.player_state
                )
            else:
                assert search_state.legal_actions is not None
                legal_actions = search_state.legal_actions
            successors = []
            assert len(legal_actions) != 0
            for action in legal_actions:
                next_player_hand = {
                    p: search_state.player_hands[p].copy()
                    for p in search_state.player_hands
                }
                next_player_hand[search_state.player].remove(action.cards)
                next_player_state, next_player, is_end = self.rule.judge(
                    search_state.player_state.copy(),
                    search_state.player,
                    next_player_hand
                )
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
                    self.player in self.rule.get_winner(game_state.player_state):
                return True
            else:
                return False

        def is_to_maximize(self, player: str) -> bool:
            if self.min_max_dict[player] == 1:
                return True
            else:
                return False

        def score(self, game_state: "MiniMaxAgent.GameSearchState") -> float:
            pass

        def score_of_farmer(self, game_state: "MiniMaxAgent.GameSearchState") -> float:
            if not game_state.is_end:
                return (
                        self.factor_opponent_cards * len(game_state.player_hands["lord"])
                        - self.factor_team_cards * len(game_state.player_hands["farmer_1"])
                        - self.factor_team_cards * len(game_state.player_hands["farmer_2"])
                )
            else:
                if self.is_goal_state(game_state):
                    return self.factor_win
                else:
                    return self.factor_lose

        def score_of_lord(self, game_state: "MiniMaxAgent.GameSearchState") -> float:
            if not game_state.is_end:
                return (
                        - self.factor_team_cards * len(game_state.player_hands["lord"])
                        + self.factor_opponent_cards * len(game_state.player_hands["farmer_1"])
                        + self.factor_opponent_cards * len(game_state.player_hands["farmer_2"])
                )
            else:
                if self.is_goal_state(game_state):
                    return self.factor_win
                else:
                    return self.factor_lose
