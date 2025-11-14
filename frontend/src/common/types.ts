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

export type {FriendProps, OpenGameProps, PreviousGameProps};