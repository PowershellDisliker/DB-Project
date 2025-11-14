// Previous Games
type GameResult = {
    duration: number;
    winner: number;
}

// Open Games
type OpenGame = {
    game_id: string;
    
}

export type HomeViewModel = {
    user_name: string;
    previous_games: GameResult[];
    open_games: OpenGame[];
}
