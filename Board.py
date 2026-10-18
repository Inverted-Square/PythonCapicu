from random import shuffle


class Board:
    def __init__(self, goal: int = 200) -> None:
        self.__player_hands: list[list[list[int]]] = [[], [], [], []]
        self.__player_totals: list[int] = [0, 0, 0, 0]
        self.__deal_dominoes()
        self.__train_ends: list[int] = [-1, -1]
        self.__turn: int = -1
        self.__prev_winner: int = -1
        self.__team_scores: list[int] = [0, 0]
        self.__goal = goal

    def __deal_dominoes(self) -> None:
        self.__player_hands = [[], [], [], []]
        self.__player_totals = [0, 0, 0, 0]
        dominoes: list[list[int]] = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 1], [1, 2], [1, 3],
                                     [1, 4], [1, 5], [1, 6], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [3, 3], [3, 4],
                                     [3, 5], [3, 6], [4, 4], [4, 5], [4, 6], [5, 5], [5, 6], [6, 6]]
        shuffle(dominoes)
        for i, hand in enumerate(self.__player_hands):
            for _ in range(7):
                domino: list[int] = dominoes.pop()
                self.__player_totals[i] += sum(domino)
                hand.append(domino)

    def set_up_first(self) -> None:
        self.__train_ends = [6, 6]
        for turn in range(4):
            if self.__train_ends in self.__player_hands[turn]:
                print(f"Player {turn + 1} has the double 6 and starts the game.")
                self.__player_hands[turn].remove(self.__train_ends)
                self.__player_totals[turn] -= 12
                self.__turn = turn
                self.__update_turn()
                return

    def set_up(self) -> None:
        if self.__prev_winner == -1:
            raise Exception("No rounds on this board have been played yet. Call set_up_first() instead.")

        print("=======================================================\n")
        self.__deal_dominoes()
        self.__turn = self.__prev_winner
        print(f"Player {self.__turn + 1}, choose a domino from your hand to place to start off the game.")
        domino_idx: int = self.__select_domino()
        self.__train_ends = self.__player_hands[self.__turn].pop(domino_idx)
        self.__player_totals[self.__turn] -= sum(self.__train_ends)
        self.__update_turn()

    def play_turn(self) -> str:
        print(f"\nIt's now player {self.__turn + 1}'s turn.\n"
              f"The current ends of the train are {self.__train_ends[0]} and {self.__train_ends[1]}.\n"
              f"The sizes of each hand is:\n"
              f"Player 1 - {len(self.__player_hands[0])}\n"
              f"Player 2 - {len(self.__player_hands[1])}\n"
              f"Player 3 - {len(self.__player_hands[2])}\n"
              f"Player 4 - {len(self.__player_hands[3])}")

        domino_idx: int = self.__select_domino()
        domino: list[int] = self.__player_hands[self.__turn][domino_idx]
        while self.__train_ends[0] not in domino and self.__train_ends[1] not in domino:
            print(f"Please select a domino that can be placed at either end ({self.__train_ends[0]} or "
                  f"{self.__train_ends[1]}).")
            domino_idx = self.__select_domino()
            domino = self.__player_hands[self.__turn][domino_idx]

        self.__player_hands[self.__turn].remove(domino)
        self.__player_totals[self.__turn] -= sum(domino)

        capicu: bool = (self.__train_ends[0] != self.__train_ends[1] and domino[0] != domino[1] and
                        domino[0] in self.__train_ends and domino[1] in self.__train_ends)
        if not self.__player_hands[self.__turn]:
            if capicu:
                print(f"\nCAPICU! (+25 points)")

            self.__team_scores[self.__turn % 2] += sum(self.__player_totals) + capicu * 25
            self.__prev_winner = self.__turn
            print(f"\nPlayer {self.__turn + 1} placed their last domino, so the round is over.")
            return (f"\n\nPlayer {self.__turn + 1} on team {(self.__turn % 2) + 1} wins. The round scores are:\n"
                    f"Team 1: {self.__team_scores[0]}\n"
                    f"Team 2: {self.__team_scores[1]}\n")

        if capicu:  # not really capicu as it's not the end of the game, but the if statement logic is the same
            end_idx: int = self.__select_end()
            self.__train_ends[end_idx] = self.__train_ends[1 - end_idx]
        elif domino[0] == self.__train_ends[0]:
            self.__train_ends[0] = domino[1]
        elif domino[0] == self.__train_ends[1]:
            self.__train_ends[1] = domino[1]
        elif domino[1] == self.__train_ends[0]:
            self.__train_ends[0] = domino[0]
        elif domino[1] == self.__train_ends[1]:
            self.__train_ends[1] = domino[0]

        return self.__update_turn()

    def __select_domino(self) -> int:
        self.__display_hand()
        hand_size: int = len(self.__player_hands[self.__turn])
        domino_idx: int = -1
        while domino_idx < 0 or domino_idx >= hand_size:
            try:
                range_str: str = f"[1-{hand_size}]" if hand_size != 1 else "[1]"
                domino_idx = int(input(f"Please type {range_str} to place a domino: ")) - 1
            except ValueError:
                print("Please input just a whole number.")

        return domino_idx

    def __select_end(self) -> int:
        print(f"Which end of the train would you like to place on?\n"
              f"1: {self.__train_ends[0]}\n"
              f"2: {self.__train_ends[1]}")
        end_idx: int = -1
        while end_idx not in [0, 1]:
            try:
                end_idx = int(input(f"Please type either 1 or 2 to select a train end: ")) - 1
            except ValueError:
                print("Please input just a whole number.")

        return end_idx

    def __display_hand(self):
        print(f"\nPlayer {self.__turn + 1}'s dominoes:")
        for i, domino in enumerate(self.__player_hands[self.__turn]):
            print(f"{i + 1}: | {domino[0]} | {domino[1]} |")

    def __update_turn(self) -> str:
        for _ in range(4):
            self.__turn = (self.__turn + 1) % 4
            if self.__can_play():
                return ""

            print(f"\nPlayer {self.__turn + 1} cannot play.")

        team1_total: int = self.__player_totals[0] + self.__player_totals[2]
        team2_total: int = self.__player_totals[1] + self.__player_totals[3]
        print("\nEveryone has passed, so the round is over.\n"
              f"Team 1's total pip count is {team1_total}\n"
              f"Team 2's total pip count is {team2_total}")
        if team1_total == team2_total:
            self.__team_scores[self.__turn] = team1_total + team2_total
            self.__prev_winner = self.__turn
        else:
            winning_team: int = team2_total < team1_total
            self.__team_scores[winning_team] = team1_total + team2_total
            self.__prev_winner = self.__turn if winning_team == self.__turn % 2 else (self.__turn + 1) % 4

        return (
            f"\n\nPlayer {self.__prev_winner + 1} on team {(self.__prev_winner % 2) + 1} wins. The round scores are:\n"
            f"Team 1: {self.__team_scores[0]}\n"
            f"Team 2: {self.__team_scores[1]}\n")

    def __can_play(self) -> bool:
        for domino in self.__player_hands[self.__turn]:
            if self.__train_ends[0] in domino or self.__train_ends[1] in domino:
                return True

        return False

    def display_hands(self) -> None:
        for i, hand in enumerate(self.__player_hands):
            print(f"\nPlayer {i + 1}'s hand (total pip count: {self.__player_totals[i]}):", end=" ")
            for domino in hand:
                print(f"| {domino[0]} | {domino[1]} |", end="   ")

    def overall_winner(self) -> str:
        if self.__team_scores[0] >= self.__goal:
            return "Team 1 wins!"
        elif self.__team_scores[1] >= self.__goal:
            return "Team 2 wins!"
        else:
            return ""
