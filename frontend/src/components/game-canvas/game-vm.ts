export class Piece {
    row: number;
    col: number;

    dy: number = 0.0;

    constructor(row: number, col:number) {
        this.row = row;
        this.col = col;
    }
}

export interface SlowState {
    game_id: string;
    start_time: Date;
    current_player: boolean;
}

export interface RealTimeState {
    pieces: Piece[];
    current_player: string;
    game_active: boolean;
}
