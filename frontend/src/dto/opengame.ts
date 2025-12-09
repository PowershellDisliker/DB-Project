export interface OpenGame {
    game_id: string,
    user_1_id: string,
    user_2_id: string | null
}

export interface GetOpenGamesResponse {
    games: Array<string> | null
}

export interface PostOpenGamesResponse {
    success: boolean,
    game_id: string | null
}