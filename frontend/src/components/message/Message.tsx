import { useContext } from "react";
import type { Message } from "../../dto/message";
import { AuthContext } from "../../context";
import messageStyles from './messages.module.css';


function MessageComp({sender_id, message, time_stamp}: Message) {
    const auth = useContext(AuthContext);

    return (
        <div className={auth.user_id == sender_id ? messageStyles.sentMesage : messageStyles.receivedMessage}>
            <p>{message}</p>
            <p>{time_stamp.toString()}</p>
        </div>
    )
}

export default MessageComp;