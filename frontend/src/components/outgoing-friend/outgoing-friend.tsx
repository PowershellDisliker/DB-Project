import type { User } from "../../dto/friend"

interface RequestProps {
    user: User
}

function OutgoingFriendRequest({user}: RequestProps) {


    return (
        <div>
            <p>{user.username}</p>
            <p>{user.online}</p>
        </div>
    )
}

export default OutgoingFriendRequest