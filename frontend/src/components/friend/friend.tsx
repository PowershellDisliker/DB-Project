import { useContext } from 'react';
import type { PostFriendRequest } from '../../dto';
import { AuthContext, ConfigContext } from '../../context';
import { removeFriend } from '../../api/api';
import type { User } from '../../dto/friend';

interface props {
    user: User
}

function Friend({user}: props) {

    const auth = useContext(AuthContext);
    const config = useContext(ConfigContext);

    const removeFriendHandler = async () => {
        const repsonse = await removeFriend(config.BACKEND_URL, auth.token!, {
            requestor_id: auth.user_id,
            requestee_id: user.user_id
        } as PostFriendRequest)
    }

    return (
        <div>
            <p>{user.username}</p>
            <p>{user.online ? "online" : "offline"}</p>
            <button onClick={removeFriendHandler}>Remove Friend</button>
        </div>
    )
}

export default Friend;