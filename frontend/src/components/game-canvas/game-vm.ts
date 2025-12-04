export class Piece {
    row: number;
    col: number;

    yPos: number;

    dy: number;

    color: string;

    constructor(row: number, col: number, color: string, isStatic: boolean) {
        this.row = row;
        this.col = col;
        this.color = color;

        // Start above column
        this.yPos = isStatic ? 0 : -80;

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
