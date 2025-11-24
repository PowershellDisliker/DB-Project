// This file contains all functions to that the frontend uses to query the backend

import { type OpenGameProps, type UserDetails, type FriendProps, type LoginAttempt} from "../common/types";

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

export const AttemptLogin = async (username: string, password: string): Promise<LoginAttempt> => {
    return RequestFromServer<LoginAttempt>("/api/login", {user: username, passw: password});
}

export const GetUserInfo = async (token: string): Promise<UserDetails> => {
    return RequestFromServer<UserDetails>("/api/userinfo", {token: token});
}

export const GetOpenGames = async (): Promise<OpenGameProps[]> => {
    return RequestFromServer<OpenGameProps[]>("/api/opengames", {});
}

export const GetFriends = async (userid: string): Promise<FriendProps[]> => {
    return RequestFromServer<FriendProps[]>("/api/friends", {userid: userid});
}