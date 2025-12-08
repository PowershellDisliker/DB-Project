import { useContext } from 'react';
import type { PostFriendRequest } from '../../dto';
import { AuthContext, ConfigContext } from '../../context';
import { removeFriend } from '../../api/api';
import type { User } from '../../dto/friend';
import globalStyles from "../../global.module.css";
import localStyles from "./friend.module.css";
import { useNavigate } from 'react-router-dom';

interface props {
    user: User
    state_update: () => void;
}

function Friend({user, state_update}: props) {

    const auth = useContext(AuthContext);
    const config = useContext(ConfigContext);

    const navigator = useNavigate();

    const removeFriendHandler = async () => {
        const repsonse = await removeFriend(config.BACKEND_URL, auth.token!, {
            requestor_id: auth.user_id,
            requestee_id: user.user_id
        } as PostFriendRequest)
        state_update();
    }

    const startMessageHandler = () => {
        navigator(`/messages?user=${user.user_id}`)
    }

    return (
        <div className={`${globalStyles.row} ${globalStyles.center} ${globalStyles.roundedContainer} ${localStyles.gap} ${localStyles.margin}`}>
            <p className={localStyles.bold}>{user.username}</p>
            <p>{user.online ? "online" : "offline"}</p>

            <button onClick={removeFriendHandler}>Remove Friend</button>
            <button onClick={startMessageHandler}>Send Message</button>
        </div>
    )
}

export default Friend;