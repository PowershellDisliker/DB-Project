import { useContext } from 'react';
import type { PostFriendRequest } from '../../dto';
import { ConfigContext } from '../../context';
import { removeFriend } from '../../api/api';
import type { User } from '../../dto/friend';
import globalStyles from "../../global.module.css";
import localStyles from "./friend.module.css";
import { useNavigate } from 'react-router-dom';
import unfriendIconURL from '../../../public/unfriend.png';
import messageIconURL from '../../../public/message.png';
import { useCookies } from 'react-cookie';

interface props {
    user: User
    state_update: () => void;
}

function Friend({user, state_update}: props) {
    const [cookies, setCookies, removeCookies] = useCookies(['jwt', 'id'])

    const config = useContext(ConfigContext);

    const navigator = useNavigate();

    const removeFriendHandler = async () => {
        const repsonse = await removeFriend(config.BACKEND_URL, cookies.jwt, {
            requestor_id: cookies.id,
            requestee_id: user.user_id
        } as PostFriendRequest)
        state_update();
    }

    const startMessageHandler = () => {
        navigator(`/messages?user=${user.user_id}`)
    }

    return (
        <div className={`${globalStyles.row} ${globalStyles.center} ${globalStyles.roundedContainer} ${localStyles.gap} ${localStyles.margin}`}>
            <p className={`${localStyles.username}`}>{user.username}</p>

            <button onClick={removeFriendHandler} className={localStyles.button}>
                <img src={unfriendIconURL} className={localStyles.icon} />
            </button>
            <button onClick={startMessageHandler} className={localStyles.button}>
                <img src={messageIconURL} className={localStyles.icon} />
            </button>
        </div>
    )
}

export default Friend;