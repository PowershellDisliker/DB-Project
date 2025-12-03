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
    active_player: boolean | null;
}

export interface RealTimeState {
    pieces: (Piece | null)[];
    
    player_1_id: string | null;
    player_2_id: string | null;

    active_player: string | null;

    gameActive: boolean;
}
