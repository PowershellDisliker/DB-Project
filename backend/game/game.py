import json

BOARD_COLUMNS: int = 7
BOARD_ROWS: int = 6

class Piece:
    owner_number: int | None
    piece_type: int
    

class ConnectFourBoard:
    player_1_id: int
    player_2_id: int
    positions: list[list[Piece]] = [Piece(None, 0) * BOARD_ROWS for _ in range(BOARD_COLUMNS)]

    
    def __init__(self, p1_id: int, p2_id: int) -> None:
        self.player_1_id = p1_id
        self.player_2_id = p2_id


    def drop_piece(self, piece_owner: int, piece_type: int, column: int) -> bool:
        """
        Attempts to drop a connect 4 piece into the board at a specific column.

        Returns true if possible and successful, false otherwise.
        """
        if column < 0 or column >= BOARD_COLUMNS:
            return False


    def json_board_state() -> str:
        return json.dumps(positions)


    def check_for_winner(self) -> int:
        """
        Checks the board to see if there is a winner, returns the winner's player number
        if there is a winner or -1 if there is not currently a winner.
        """

        return -1


    def print_board(self) -> None:
        """
        low-level visual representation of the current board state for debugging
        """
        for row in self.positions:
            for value in row:
                print(value.owner_number, end=" ")
            print()
        