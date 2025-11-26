import type { FriendProps, OpenGameProps, PreviousGameProps, UserDetails } from "../common/types";

export type HomeViewModel = {
    user_details: UserDetails | null;
    previous_games: PreviousGameProps[] | null;
    open_games: OpenGameProps[] | null;
    friends: FriendProps[] | null;
}