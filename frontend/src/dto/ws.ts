export interface WebsocketGameRequest {
    jwt: string;
    game_id: string;
}

export interface WebsocketRequest {
    command_type: "drop_piece" | "register_user" | "get_board_state";
    
    game_id: string | null;
    col: number | null;
    user_id: string | null;
}

export interface WebsocketResponse {
    command_type: "error" | "board_state" | "register_response" | "drop_piece_response";

    error: string | null;

    user_1_id: string | null;
    user_2_id: string | null;
    board_state: Array<string | null> | null;
    active_player: string | null;

    row: number | null;
    col: number | null;
    next_active_player_id: string | null;

    success: boolean | null;
    winner_id: string | null;
}