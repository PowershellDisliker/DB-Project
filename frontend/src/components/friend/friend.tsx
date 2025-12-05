import type { GetPublicUserResponse } from '../../dto';

function Friend({username, online}: GetPublicUserResponse) {

    return (
        <div>
            <p>{username}</p>
            <p>{online ? "online" : "offline"}</p>
        </div>
    )
}

export default Friend;