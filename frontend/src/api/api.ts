// This file contains all functions to that the frontend uses to query the backend

import { type OpenGameProps, type UserDetails, type FriendProps } from "../common/types";

async function RequestFromServer<T>(route: string, request: Object) {
    const URI: string = "http://127.0.0.1:8000";

    const res = await fetch(
        URI + route,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(request)
        }
    )

    if (!res.ok) {
        throw new Error(`Error Contacting backend: ${res.status}`);
    }

    const jsonData = await res.json();

    return jsonData as T;
}

export const AttemptLogin = async (username: string, password: string): Promise<Boolean> => {
    return RequestFromServer<Boolean>("/api/login", {username: username, password: password});
}

export const GetUserInfo = async (token: string) => {
    return RequestFromServer<UserDetails>("/api/userinfo", {token: token});
}

export const GetOpenGames = async () => {
    return RequestFromServer<OpenGameProps[]>("/api/opengames", {});
}

export const GetFriends = async (userid: string) => {
    return RequestFromServer<FriendProps[]>("/api/friends", {userid: userid});
}