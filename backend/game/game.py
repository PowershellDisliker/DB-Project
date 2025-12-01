import json

BOARD_COLUMNS: int = 7
BOARD_ROWS: int = 6

class node:
    connected: list[edgeNode]
    Piece: Piece # will prolly need this for connecting only the nodes that are from the same player

class edgeNode:
    to: node
    direction: int # could do 0 - 7 for the direction of the connection 1 at top left moving clockwise around

class gameState:
    # object for sending data to the visulaizer in the front end
    # needs the board, player turn, if the game is running, who won
    board: ConnectFourBoard
    winner = -1 # -1 if game is still going
    turn = 0 # start wiht player 1

    def __init__(self, CurrentBoard):
        self.board = CurrentBoard

    def updateTurn():
        # swap to the next turn
        if(turn == 0): 
            turn = 1    
        else:
            turn = 0

    def setWinner(self, outcome: int):
        # set the winner to correct player
        self.winner = outcome
    
    def toJson(self):
        # convert to a json serialization to send to the front end
        return json.dumps(self)
    
    def update(self, jsonString : str):
        # update the game state based on the json input string
        jsonDict = json.loads(jsonString) # convert the json string into a dictionary
        self.winner = jsonDict["winner"]
        self.turn = jsonDict["turn"]
        self.board = jsonDict["board"]

class Piece:
    owner_number: int | None
    piece_type: int
    def __init__(self, player: int, type: int):
        self.owner_number = player
        self.piece_type = type
        

class ConnectFourBoard:
    # board object that holds the possitions of the chips
    player_1_id: int
    player_2_id: int
    positions: list[list[Piece]] = [[None for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)] # should fill the matrix with "blank" pieces

    
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


    def check_for_winner(self) -> int:
        """
        Checks the board to see if there is a winner, returns the winner's player number
        if there is a winner or -1 if there is not currently a winner.
        """
        #idea for checking the winner
        """dfs for traversing the matrix like a graph
        would need to keep track of the direction the the connection is made could prolly get it done with indexes"""

        return -1
    
    def dfsWinner(positions: list[list[Piece]], moveCount: int):
        # should return true if a winner is found

        return 

    def print_board(self) -> None:
        """
        low-level visual representation of the current board state for debugging
        """
        for row in self.positions:
            for value in row:
                print(value.owner_number, end=" ")
            print()
        