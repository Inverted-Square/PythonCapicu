YES: int = 1
MAYBE: int = 0
NO: int = -1


class DominoTracker:
    # note that if two_players is False it could be a 3 OR a 4 player game - and it's down to the class user to know
    # what function calls to make to accommodate for this
    def __init__(self, player: int, hand: list[list[int]], two_players: bool = False) -> None:
        dominoes: list[list[int]] = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 1], [1, 2], [1, 3],
                                     [1, 4], [1, 5], [1, 6], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [3, 3], [3, 4],
                                     [3, 5], [3, 6], [4, 4], [4, 5], [4, 6], [5, 5], [5, 6], [6, 6]]
        self.__domino_table: dict[str, list[int]] = {str(domino): [MAYBE, MAYBE, MAYBE, MAYBE] for domino in dominoes}

        self.__hand_sizes: list[int] = [7, 7, 14] if two_players else [7, 7, 7 ,7]
        self.__yes_counts: list[int] = [0, 0, 0] if two_players else [0, 0, 0, 0]
        self.__maybe_counts: list[int] = [28, 28, 28] if two_players else [28, 28, 28, 28]

        for domino in hand:
            self.__domino_known(player, str(domino))

    def player_placed(self, player: int, domino: list[int]) -> None:
        self.__hand_sizes[player] -= 1

        row: list[int] = self.__domino_table[str(domino)]
        players_to_update: list[int] = []
        for p, val in enumerate(row):
            row[p] = NO
            self.__yes_counts[p] -= 1 * (val == YES)
            if val == MAYBE:
                self.__maybe_counts[p] -= 1
                players_to_update.append(p)

        for p in players_to_update:
            self.__update(p)

    def player_has_no(self, player: int, train_ends: list[int]) -> None:
        dominoes_to_update: list[str] = []
        for domino in self.__domino_table.keys():
            if ((str(train_ends[0]) in domino or str(train_ends[1]) in domino) and
                    self.__domino_table[domino][player] == MAYBE):
                self.__domino_table[domino][player] = NO
                self.__maybe_counts[player] -= 1
                dominoes_to_update.append(domino)

        players_to_update: list[int] = [player]
        for d in dominoes_to_update:
            players_to_update.append(self.__last_maybe_check(d))

        for p in players_to_update:
            self.__update(p)

    # only call if it's a two or three player game
    def draw_unknown(self, player: int) -> None:
        self.__hand_sizes[player] += 1
        # for all pieces that may be in the draw pile, set them as MAYBE for the specified player
        #   - ONLY DO THIS IF IT DOESN'T BREAK THE 2 CONDITIONS
        #       1. a YES means all other entries on a row must be NO
        #       2. a MAYBE where the rest on a row are NO is always a YES

    def __update(self, player: int) -> None:
        if self.__maybe_counts[player] == 0:
            return

        if self.__yes_counts[player] == self.__hand_sizes[player]:
            self.__maybe_to_no(player)
        elif self.__yes_counts[player] + self.__maybe_counts[player] == self.__hand_sizes[player]:
            self.__maybe_to_yes(player)

    def __maybe_to_no(self, player: int) -> None:
        dominoes_to_update: list[str] = []
        for domino in self.__domino_table.keys():
            if self.__domino_table[domino][player] == MAYBE:
                self.__domino_table[domino][player] = NO
                self.__maybe_counts[player] -= 1
                dominoes_to_update.append(domino)

        players_to_update: list[int] = [player]
        for d in dominoes_to_update:
            players_to_update.append(self.__last_maybe_check(d))

        for p in players_to_update:
            self.__update(p)

    def __last_maybe_check(self, domino: str) -> int:
        found: bool = False
        player: int = -1
        for p, val in enumerate(self.__domino_table[domino]):
            if val != MAYBE:
                continue

            if found:
                return player

            found = True
            player = p

        self.__set_yes(player, domino)
        return player

    def __set_yes(self, player: int, domino: str) -> None:
        self.__domino_table[domino][player] = YES
        self.__yes_counts[player] += 1
        self.__maybe_counts[player] -= 1

    def __maybe_to_yes(self, player: int) -> None:
        for domino in self.__domino_table.keys():
            if self.__domino_table[domino][player] == MAYBE:
                self.__domino_known(player, domino)

    def __domino_known(self, player: int, domino: str) -> None:
        self.__set_yes(player, domino)
        players_to_update: list[int] = [player]
        for p, val in enumerate(self.__domino_table[domino]):
            if val == MAYBE:
                self.__domino_table[domino][p] = NO
                self.__maybe_counts[p] -= 1
                players_to_update.append(p)

        for p in players_to_update:
            self.__update(p)
