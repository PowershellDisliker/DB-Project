import {
    type AuthRequest, type AuthResponse,
    type GetClosedGameResponse, type PostClosedGameRequest, type PostClosedGameResponse,
    type PostFriendRequest, type PostFriendResponse,
    type GetMessageResponse, type PostMessageRequest, type PostMessageResponse,
    type GetOpenGamesResponse, type PostOpenGamesResponse,
    type GetPublicUserResponse, type GetPrivateUserResponse,
    type OpenGameProps
} from "../dto";
import type { GetFriendRequestsResponse } from "../dto/friend";

async function postBackend<T>(backend_url: string, route: string, request: unknown, jwt: string | null = null) {

    const res = await fetch(
        backend_url + route,
        {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${jwt}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(request)
        }
    )

    if (!res.ok) {
        throw new Error(`${backend_url}${route}: ${res.status}`);
    }

    const jsonData = await res.json();

    return jsonData as T;
}

async function getBackend<T>(backend_url: string, route: string, jwt: string | null = null) {
    const res = await fetch(
        backend_url + route,
        {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${jwt}`,
                "Content-Type": "application/json"
            }
        }
    )

    if (!res.ok) {
        throw new Error(`${backend_url}${route}: ${res.status}`);
    }

    const jsonData = await res.json();

    return jsonData as T;
}

export const attemptLogin = async (backend_url: string, username: string, password: string): Promise<AuthResponse> => {
    return postBackend<AuthResponse>(backend_url, "/api/login", {username: username, password: password} as AuthRequest);
}

export const attemptRegister = async (backend_url: string, username: string, password: string): Promise<AuthResponse> => {
    return postBackend<AuthResponse>(backend_url, "/api/register", {username: username, password: password} as AuthRequest);
}

export const getClosedGames = async (backend_url: string, jwt: string): Promise<GetClosedGameResponse> => {
    return getBackend<GetClosedGameResponse>(backend_url, "/api/closedgames", jwt);
}

export const postClosedGame = async (backend_url: string, jwt: string, request: PostClosedGameRequest): Promise<PostClosedGameResponse> => {
    return postBackend<PostClosedGameResponse>(backend_url, "/api/closedgames", request, jwt);
}

export const getFriends = async (backend_url: string, jwt: string): Promise<GetFriendRequestsResponse> => {
    return getBackend<GetFriendRequestsResponse>(backend_url, "/api/friends", jwt);
}

export const getIncomingFriendRequests = async (backend_url: string, jwt: string): Promise<GetFriendRequestsResponse> => {
    return getBackend<GetFriendRequestsResponse>(backend_url, "/api/friends/incoming", jwt);
}

export const getOutgoingFriendRequests = async (backend_url: string, jwt: string): Promise<GetFriendRequestsResponse> => {
    return getBackend<GetFriendRequestsResponse>(backend_url, "/api/friends/outgoing", jwt);
}

export const postFriend = async (backend_url: string, jwt: string, request: PostFriendRequest): Promise<PostFriendResponse> => {
    return postBackend(backend_url, "/api/friends", request, jwt)
}

export const removeFriend = async (backend_url: string, jwt: string, request: PostFriendRequest): Promise<PostFriendResponse> => {
    return postBackend(backend_url, "/api/friends/reject", request, jwt);
}

export const getMessages = async (backend_url: string, jwt: string): Promise<GetMessageResponse> => {
    return getBackend(backend_url, "/api/messages", jwt)
}

export const postMessage = async (backend_url: string, jwt: string, request: PostMessageRequest): Promise<PostMessageResponse> => {
    return postBackend(backend_url, "/api/messages", request, jwt)
}

export const getOpenGames = async (backend_url: string, jwt: string): Promise<GetOpenGamesResponse> => {
    return getBackend<GetOpenGamesResponse>(backend_url, "/api/opengames", jwt);
}

export const getOpenGameDetails = async (backend_url: string, jwt: string, game_id: string): Promise<OpenGameProps> => {
    return getBackend<OpenGameProps>(backend_url, `/api/opengamedetails?game_id=${game_id}`, jwt);
}

export const postOpenGame = async (backend_url: string, jwt: string): Promise<PostOpenGamesResponse> => {
    return postBackend<PostOpenGamesResponse>(backend_url, "/api/opengames", {}, jwt)
}

export const getPublicUser = async (backend_url: string, jwt: string, user_id: string): Promise<GetPublicUserResponse> => {
    return getBackend<GetPublicUserResponse>(backend_url, `/api/user/public/id?query_user_id=${user_id}`, jwt);
}

export const getPublicUserFromUsername = async (backend_url: string, jwt: string, username: string): Promise<GetPublicUserResponse> => {
    return getBackend<GetPublicUserResponse>(backend_url, `/api/user/public/username?query_username=${username}`, jwt);
}

export const getPrivateUser = async (backend_url: string, jwt: string, user_id: string): Promise<GetPrivateUserResponse> => {
    return getBackend<GetPrivateUserResponse>(backend_url, `/api/user/private?query_user_id=${user_id}`, jwt)
}
