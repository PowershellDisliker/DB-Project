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
        returns winner's uuid if there is a winner, or None if there isn't

        check the 8 piece around the last played piece then if there is one by the same user check the next two 
        the board is held in posititons and it is just a linear list so each new row will be after 7 pieces or indieces
        
        the first col will be index%7 and the last col will be index%6
        """
        def check_col() -> uuid.UUID | None:
            # check the col or left and right
            right = 0
            left = 0
            for i in range(3):
                if((recent_piece_index + 3) % 7 <= 3): # possible on the right
                    if(self.positions[recent_piece_index] == self.positions[recent_piece_index + i]): # check right
                        right = right + 1
                if((recent_piece_index - 3) % 7 >= 3): # possible on the left
                    if(self.positions[recent_piece_index] == self.positions[recent_piece_index - i]): # check left
                        left = left + 1
            if(right >= 4):
                return self.positions[recent_piece_index]
            if(left >= 4):
                return self.positions[recent_piece_index]
            if(right < 4 & left < 4):
                return None
            
        def check_row() -> uuid.UUID | None:
            # check the up or down and right
            up = 0
            down = 0
            for i in range(3):
                if(recent_piece_index // 7 >= 3): # up is possible
                    if(self.positions[recent_piece_index] == self.positions[recent_piece_index + (i * 7)]): # check down
                        up = up + 1
                if(recent_piece_index // 7 <= 2): # down is possible
                    if(self.positions[recent_piece_index] == self.positions[recent_piece_index - (i * 7)]): # check up
                        down = down + 1
            if(up >= 4):
                return self.positions[recent_piece_index]
            if(down >= 4):
                return self.positions[recent_piece_index]
            if(up < 4 & down < 4):
                return None
            
        def check_dia() -> uuid.UUID | None:
            # check the diagonals
            upperleft = 0
            upperright = 0
            lowerleft = 0
            lowerright = 0
            for i in range(3):
                if(recent_piece_index // 7 >= 3): # upper diagonals
                    # now we check if there is enough room on the sides
                    if((recent_piece_index + 3) % 7 <= 3): # check right
                        if(self.positions[recent_piece_index] == self.positions[recent_piece_index + 1 - 7]):
                            upperright = upperright + 1
                    if((recent_piece_index - 3) % 7 <= 3): # check left
                        if(self.positions[recent_piece_index] == self.positions[recent_piece_index - 1 - 7]):
                            upperleft = upperleft + 1
                if(recent_piece_index // 7 <= 2): # lower diagonals
                    if((recent_piece_index + 3) % 7 <= 3): # check right
                        if(self.positions[recent_piece_index] == self.positions[recent_piece_index + 1 + 7]):
                            lowerright = lowerright + 1
                    if((recent_piece_index - 3) % 7 <= 3): # check left
                        if(self.positions[recent_piece_index] == self. positions[recent_piece_index -1 + 7]):
                            lowerleft = lowerleft + 1
            if(upperleft >= 4):
                return self.positions[recent_piece_index]
            if(upperright >= 4):
                return self.positions[recent_piece_index]
            if(lowerleft >= 4):
                return self.positions[recent_piece_index]
            if(upperright >= 4):
                return self.positions[recent_piece_index]
            return None
                            

        col_winner = check_col()
        row_winner = check_row()
        dia_winner = check_dia()

        if col_winner:
            return col_winner

        if row_winner:
            return row_winner
        
        if dia_winner:
            return dia_winner
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
        