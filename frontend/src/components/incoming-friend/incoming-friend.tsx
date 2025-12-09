import { useContext } from "react";
import type { PostFriendRequest, User } from "../../dto/friend";
import { ConfigContext } from "../../context";
import { postFriend } from "../../api";
import { removeFriend } from "../../api/api";
import globalStyles from "../../global.module.css";
import { useCookies } from "react-cookie";


interface RequestProps {
    user: User;
    state_update: () => void;
}

function IncomingFriendRequest({user, state_update}: RequestProps) {

    const config = useContext(ConfigContext);
    const [cookies, setCookies, removeCookies] = useCookies(['jwt', 'id']);

    const acceptHandler = async () => {
        await postFriend(config.BACKEND_URL, cookies.jwt, {
            requestor_id: cookies.id,
            requestee_id: user.user_id,
        } as PostFriendRequest)
        state_update();
    };

    const rejectHandler = async () => {
        await removeFriend(config.BACKEND_URL, cookies.jwt, {
            requestor_id: cookies.id,
            requestee_id: user.user_id,
        } as PostFriendRequest)
        state_update();
    }

    return (
        <div className={`${globalStyles.row} ${globalStyles.spaceBetween} ${globalStyles.margin}`}>
            <p>{user.username}</p>
            <p>{user.online}</p>
            <div className={`${globalStyles.row}`}>
                <button onClick={acceptHandler}>Accept</button>
                <button onClick={rejectHandler}>Reject</button>
            </div>
        </div>
    )
}

export default IncomingFriendRequest;