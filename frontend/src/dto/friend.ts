export interface GetFriendResponse {
    friend_ids: Array<[string, boolean]> | null
}

export interface PostFriendRequest {
    user_1_id: string,
    user_2_id: string,
}

export interface PostFriendResponse {
    success: boolean
}