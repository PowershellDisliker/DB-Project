export interface User {
    user_id: string | null;
    username: string | null;
    online: boolean | null;
}

export interface GetFriendResponse {
    friend_ids: Array<string> | null
}

export interface GetFriendRequestsResponse {
    users: Array<User>
}

export interface PostFriendRequest {
    requestor_id: string,
    requestee_id: string,
}

export interface PostFriendResponse {
    success: boolean
}