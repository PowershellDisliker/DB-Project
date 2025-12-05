import { useContext } from "react";
import type { PostFriendRequest, User } from "../../dto/friend";
import { AuthContext, ConfigContext } from "../../context";
import { postFriend } from "../../api";
import { removeFriend } from "../../api/api";


interface RequetsProps {
    user: User
}

function IncomingFriendRequest({user}: RequetsProps) {

    const auth = useContext(AuthContext);
    const config = useContext(ConfigContext);

    const acceptHandler = async () => {
        await postFriend(config.BACKEND_URL, auth.token!, {
            requestor_id: auth.user_id,
            requestee_id: user.user_id,
        } as PostFriendRequest)
    };

    const rejectHandler = async () => {
        await removeFriend(config.BACKEND_URL, auth.token!, {
            requestor_id: auth.user_id,
            requestee_id: auth.user_id,
        } as PostFriendRequest)
    }

    return (
        <div>
            <p>{user.username}</p>
            <p>{user.online}</p>
            <div>
                <button onClick={acceptHandler}>Accept</button>
                <button onClick={rejectHandler}>Reject</button>
            </div>

        </div>
    )
}

export default IncomingFriendRequest;