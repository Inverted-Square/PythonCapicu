from Board import Board


def main() -> None:
    board: Board = Board()
    board.set_up_first()
    overall_result: str = ""
    while not overall_result:
        round_result: str = ""
        while not round_result:
            round_result = board.play_turn()

        board.display_hands()
        print(round_result)
        if board.overall_winner():
            overall_result = board.overall_winner()
            continue

        board.set_up()

    print(overall_result)


if __name__ == "__main__":
    main()
