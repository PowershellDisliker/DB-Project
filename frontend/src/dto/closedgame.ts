export interface GetClosedGameResponse {
    game_id: string,
    user_1_id: string,
    user_2_id: string,
    winner: string,
    duration: string
}

export interface PostClosedGameRequest {
    game_id: string,
    winner: string
}

export interface PostClosedGameResponse {
    success: boolean,
    game_id: string | null
}