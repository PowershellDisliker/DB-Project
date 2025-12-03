export interface AuthRequest {
    username: string,
    password: string
}

export interface AuthResponse {
    success: boolean,
    token: string | null
}

export interface C4JWT {
    su: string
}