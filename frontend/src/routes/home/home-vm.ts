import type { GetClosedGameResponse, GetOpenGamesResponse, GetPublicUserResponse } from "../../dto";
import type { User } from "../../dto/friend";
import type { OpenGameProps } from "../../dto/opengame";

export type HomeViewModel = {
    user_details: GetPublicUserResponse | null;
    closed_games: GetClosedGameResponse | null;
    open_games: Array<OpenGameProps> | null;
    friends: Array<User> | null;
    outgoing_friend_requests: Array<User> | null;
    incoming_friend_requests: Array<User> | null;

    failed_to_create_game: boolean;
    failed_to_post_friend: boolean;

    need_to_update: boolean;

    username_input: string;
}