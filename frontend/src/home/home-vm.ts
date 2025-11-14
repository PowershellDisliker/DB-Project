import type { FriendProps, OpenGameProps, PreviousGameProps, UserDetails } from "../common/types";

export type HomeViewModel = {
    user_details: UserDetails | null;
    previous_games: PreviousGameProps[] | null;
    open_games: OpenGameProps[] | null;
    friends: FriendProps[] | null;
}

const BACKEND_URL: string = "http://127.0.0.1:8000";

async function fetchFromBackend<T>(route: string) {
    const response: Response = await fetch(BACKEND_URL + route);
    const json_data: object = await response.json();

    return json_data as T;
}   


async function getUserDetails(route: string) {
    return await fetchFromBackend<UserDetails>(route);
}

async function getPreviousGames(route: string) {
    return await fetchFromBackend<PreviousGameProps[]>(route);
}

async function getOpenGames(route: string) {
    return await fetchFromBackend<OpenGameProps[]>(route);
}

async function getFriends(route: string) {
    return await fetchFromBackend<FriendProps[]>(route);
}

export {getUserDetails, getPreviousGames, getOpenGames, getFriends};