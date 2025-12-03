const PIECE_RADIUS = 30;

export class Piece {
    row: number;
    col: number;

    yPos: number;
    targetY: number;

    dy: number;

    color: string;

    constructor(row: number, col: number, color: string) {
        this.row = row;
        this.col = col;
        this.color = color;

        // Start above column
        this.yPos = -80;
        
        // Where the piece should stop
        this.targetY = row * PIECE_RADIUS * 2;

        // Initial velocity
        this.dy = 0;
    }
}

export interface SlowState {
    game_running: boolean | null;
    active_player: boolean | null;

}

export interface RealTimeState {
    pieces: (Piece | null)[];
    
    player_1_id: string | null;
    player_2_id: string | null;

    active_player: string | null;
    winner_id: string | null;
}
