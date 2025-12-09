import type { User } from "../../dto/friend"
import globalStyles from "../../global.module.css";

interface RequestProps {
    user: User
    state_update: () => void
}

function OutgoingFriendRequest({user}: RequestProps) {


    return (
        <div className={`${globalStyles.roundedContainer} ${globalStyles.center}`}>
            <p>{user.username}</p>
            <p>{user.online}</p>
        </div>
    )
}

export default OutgoingFriendRequest