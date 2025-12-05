import type { User } from "../../dto/friend";


interface RequetsProps {
    user: User
}

function IncomingFriendRequest({user}: RequetsProps) {


    return (
        <div>
            <p>{user.username}</p>
            <p>{user.online}</p>
        </div>
    )
}

export default IncomingFriendRequest;