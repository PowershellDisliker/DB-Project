import { useContext } from 'react';
import type { PostFriendRequest } from '../../dto';
import { AuthContext, ConfigContext } from '../../context';
import { removeFriend } from '../../api/api';
import type { User } from '../../dto/friend';
import globalStyles from "../../global.module.css";
import localStyles from "./friend.module.css";

interface props {
    user: User
    state_update: () => void;
}

function Friend({user, state_update}: props) {

    const auth = useContext(AuthContext);
    const config = useContext(ConfigContext);

    const removeFriendHandler = async () => {
        const repsonse = await removeFriend(config.BACKEND_URL, auth.token!, {
            requestor_id: auth.user_id,
            requestee_id: user.user_id
        } as PostFriendRequest)
        state_update();
    }

    return (
        <div className={`${globalStyles.row} ${globalStyles.center} ${globalStyles.roundedContainer} ${localStyles.gap} ${localStyles.margin}`}>
            <p className={localStyles.bold}>{user.username}</p>
            <p>{user.online ? "online" : "offline"}</p>

            <button onClick={removeFriendHandler}>Remove Friend</button>
        </div>
    )
}

export default Friend;