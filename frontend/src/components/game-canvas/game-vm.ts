export class Piece {
    col: number;
    row: number;

    yPos: number = 0;
    
    color: string;

    dy: number = 0.0;

    constructor(row: number, col: number, color: string) {
        this.row = row;
        this.col = col;

        this.color = color;
    }
}

export interface SlowState {
    gameId: string;
    startTime: Date;
    currentPlayer: boolean;
}

export interface RealTimeState {
    pieces: Piece[];
    currentPlayer: string;
    gameActive: boolean;
}
