type GameResult = {
    duration: number;
    winner: number;
}

type OpenGame = {
    game_id: string;
    
}

type Friend = {
    username: string;
    status: number;
    profile_picture: Object;
}

export type HomeViewModel = {
    username: string;
    previous_games: GameResult[];
    open_games: OpenGame[];
    friends: Friend[];
}
