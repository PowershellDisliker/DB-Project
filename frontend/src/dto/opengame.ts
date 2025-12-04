export interface OpenGame {
    game_id: string,
    user_1_id: string,
    can_join: boolean
}

export interface GetOpenGamesResponse {
    games: Array<OpenGame>
}

export interface PostOpenGamesResponse {
    success: boolean,
    game_id: string | null
}