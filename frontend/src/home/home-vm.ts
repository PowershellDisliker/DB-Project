import type { FriendProps, OpenGameProps, PreviousGameProps } from "../common/types";

export type HomeViewModel = {
    username: string;
    previous_games: PreviousGameProps[];
    open_games: OpenGameProps[];
    friends: FriendProps[];
}
