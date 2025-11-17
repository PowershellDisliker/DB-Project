interface UserDetails {
    username: string;
    account_created: string;
    total_wins: number;
    total_losses: number;
}

interface FriendProps {
    username: string;
    online: boolean;
}

interface OpenGameProps {
    id: string;
}

interface PreviousGameProps {
    id: string;
}

export type {FriendProps, OpenGameProps, PreviousGameProps, UserDetails};