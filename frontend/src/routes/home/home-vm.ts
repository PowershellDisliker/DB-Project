import type { OpenGame, GetPublicUserResponse } from "../../dto";
import type { ClosedGame } from "../../dto/closedgame";
import type { User } from "../../dto/friend";

export type HomeViewModel = {
    user_details: GetPublicUserResponse | null;
    open_games: Array<OpenGame> | null;
    closed_games: Array<ClosedGame> | null;
    friends: Array<User> | null;
    outgoing_friend_requests: Array<User> | null;
    incoming_friend_requests: Array<User> | null;

    failed_to_create_game: boolean;
    failed_to_post_friend: boolean;

    need_to_update: boolean;

    username_input: string;
}