import type { GetFriendResponse, GetOpenGamesResponse, GetClosedGameResponse, GetPublicUserResponse } from "../../dto";

export type HomeViewModel = {
    user_details: GetPublicUserResponse | null;
    closed_games: GetClosedGameResponse | null;
    open_games: GetOpenGamesResponse | null;
    friends: Array<GetPublicUserResponse> | null;

    failed_to_create_game: boolean;
}