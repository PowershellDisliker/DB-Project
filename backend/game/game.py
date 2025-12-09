from typing import Tuple
from dto import BoardState, DropPieceResponse
import uuid
from datetime import datetime

# Holup
ROW_COUNT: int = 6
COL_COUNT: int = 7

class ConnectFourBoard:
    def __init__(self, user_1_id: uuid.UUID) -> None:
        print(user_1_id)
        self.user_1_id: uuid.UUID | None = user_1_id
        self.user_2_id: uuid.UUID | None = None

        self.active_player: uuid.UUID = user_1_id
        self.winner_id: uuid.UUID | None = None

        self.start_time = datetime.now()

        self.positions: list[uuid.UUID | None] = [None for _ in range(COL_COUNT * ROW_COUNT)]


    def register_player(self, user_id: uuid.UUID) -> bool:
        if self.user_1_id == user_id or self.user_2_id == user_id:
            return False

        if self.user_1_id is None:
            self.user_1_id = user_id

            if self.active_player is None:
                self.active_player = user_id
            return True

        if self.user_2_id is None:
            self.user_2_id = user_id
            return True
        return False


    def drop_piece(self, piece_owner: uuid.UUID, col: int) -> DropPieceResponse:
        """
        Attempts to drop a connect 4 piece into the board at a specific column.

        Returns true if possible and successful, false otherwise, and the UUID of the winner if there is one.
        """
        # Only allow if both players are present
        if self.user_1_id is None or self.user_2_id is None:
            return DropPieceResponse(
                success=False
            )

        # If the player placing the piece isn't currently in the game
        if piece_owner != self.user_1_id and piece_owner != self.user_2_id:
            return DropPieceResponse(
                success=False
            )

        # If we're outside of the bounds
        if col < 0 or col >= COL_COUNT:
            return DropPieceResponse(
                success=False
            )

        # If the active player isn't the piece_owner
        if self.active_player != piece_owner:
            return DropPieceResponse(
                success=False
            )

        last_available_row = None
        
        # Get the available row
        for row in reversed(range(ROW_COUNT)):
            if self.positions[self.__get_index(row, col)] is None:
                last_available_row = row
                break

        # Return if column is full
        if last_available_row is None:
            return DropPieceResponse(
                success=False
            )

        # Place the piece
        new_piece_index: int = self.__get_index(last_available_row, col)
        self.positions[new_piece_index] = piece_owner

        # Check for winner and return
        winner = self.__check_for_winner(new_piece_index)

        if winner is None:
            self.active_player = self.user_1_id if piece_owner != self.user_1_id else self.user_2_id
            return DropPieceResponse(
                success=True,
                coords=(last_available_row, col),
                next_active_player_id=self.active_player
            )
        self.winner_id = winner
        return DropPieceResponse(
            success=True,
            winner_id=winner,
            coords=(last_available_row, col),
            next_active_player_id=self.active_player
        )


    def get_board_state(self) -> BoardState:
        return BoardState(
            user_1_id=self.user_1_id,
            user_2_id=self.user_2_id,
            positions=self.positions,
            active_player=self.active_player,
            winner_id=self.winner_id
        )


    def get_players(self) -> Tuple[uuid.UUID | None, uuid.UUID | None]:
        return (self.user_1_id, self.user_2_id)


    def get_active_player(self) -> uuid.UUID | None:
        return self.active_player

    def deregister_player(self, user_id: uuid.UUID) -> None:
        if self.user_1_id == user_id:
            self.user_1_id = None

        elif self.user_2_id == user_id:
            self.user_2_id = None


    def __get_index(self, row: int, col: int) -> int:
        return row * COL_COUNT + col


    def __check_for_winner(self, recent_piece_index: int) -> uuid.UUID | None:
        """
        Returns the winner's UUID if there is a winner, or None if there isn't.
        Uses the last played piece to check all 8 directions for 4 in a row.
        """
    
        player = self.positions[recent_piece_index]
        if player is None:
            return None
    
        row = recent_piece_index // COL_COUNT
        col = recent_piece_index % COL_COUNT
    
        # Directions: (delta_row, delta_col)
        directions = [
            (0, 1),   # horizontal right
            (1, 0),   # vertical down
            (1, 1),   # diagonal down-right
            (1, -1),  # diagonal down-left
        ]
    
        for dr, dc in directions:
            count = 1  # Count the current piece
    
            # Check in the positive direction
            r, c = row + dr, col + dc
            while 0 <= r < ROW_COUNT and 0 <= c < COL_COUNT and self.positions[r * COL_COUNT + c] == player:
                count += 1
                r += dr
                c += dc
    
            # Check in the negative direction
            r, c = row - dr, col - dc
            while 0 <= r < ROW_COUNT and 0 <= c < COL_COUNT and self.positions[r * COL_COUNT + c] == player:
                count += 1
                r -= dr
                c -= dc
    
            if count >= 4:
                return player
    
        return None


    def __print_board(self) -> None:
        """
        low-level visual representation of the current board state for debugging
        """

        for row in range(ROW_COUNT):
            for col in range(COL_COUNT):
                val = self.positions[self.__get_index(row, col)]

                if val is None:
                    print("0", end=" ")
                else:
                    print("1" if val == self.user_1_id else "2", end=" ")
            print()
        