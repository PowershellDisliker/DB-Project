from typing import Tuple
import json
import uuid

# Holup
ROW_COUNT: int = 6
COL_COUNT: int = 7

class ConnectFourBoard:
    user_1_id: uuid.UUID
    user_2_id: uuid.UUID

    active_player: uuid.UUID

    positions: list[uuid.UUID | None]

    
    def __init__(self, user_1_id: uuid.UUID, user_2_id: uuid.UUID) -> None:
        self.user_1_id = user_1_id
        self.user_2_id = user_2_id

        self.positions = [None for _ in range(COL_COUNT * ROW_COUNT)]


    def drop_piece(self, piece_owner: uuid.UUID, col: int) -> Tuple[bool, uuid.UUID | None]:
        """
        Attempts to drop a connect 4 piece into the board at a specific column.

        Returns true if possible and successful, false otherwise, and the UUID of the winner if there is one.
        """

        # If we're outside of the bounds
        if col < 0 or col >= COL_COUNT:
            return (False, None)

        # Get the available row
        for row in range(0, ROW_COUNT):
            last_available_row = None

            if self.positions[row * COL_COUNT + col] is None:
                last_available_row = row

        # Return if column is full
        if last_available_row is None:
            return (False, None)

        # Place the piece
        new_piece_index: int = last_available_row * COL_COUNT + col
        self.positions[new_piece_index] = piece_owner

        # Check for winner and return
        winner = self.__check_for_winner(new_piece_index)

        if winner is None:
            return (True, None)
        return (True, winner)


    def json_board_state(self) -> str:
        return json.dumps({
            "positions": self.positions,
            "current_player": self.active_player,
        })


    def __check_for_winner(self, recent_piece_index: int) -> uuid.UUID | None:
        """
        returns winner's uuid if there is a winner, or None if there isn't
        """

        def check_col() -> uuid.UUID | None:
            pass

        def check_row() -> uuid.UUID | None:
            pass

        def check_dia() -> uuid.UUID | None:
            pass

        col_winner = check_col()
        row_winner = check_row()
        dia_winner = check_dia()


    def __print_board(self) -> None:
        """
        low-level visual representation of the current board state for debugging
        """

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLUMNS):
                print(self.positions[row * BOARD_COLUMNS + col], end=" ")
            print()
        