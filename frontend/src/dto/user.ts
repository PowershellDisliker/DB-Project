export interface GetPublicUserResponse {
    username: string | null,
    online: boolean | null
}

export interface GetPrivateUserResponse {
    user_id: string | null,
    username: string | null,
    online: boolean | null,
    pass_hash: string | null
}