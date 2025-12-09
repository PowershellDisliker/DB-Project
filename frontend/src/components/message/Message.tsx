import type { Message } from "../../dto/message";
import messageStyles from './messages.module.css';
import { useCookies } from "react-cookie";


function MessageComp({sender_id, message, time_stamp}: Message) {
    const [cookies] = useCookies(['id']);

    return (
        <div className={cookies.id == sender_id ? messageStyles.sentMesage : messageStyles.receivedMessage}>
            <p>{message}</p>
            <p>{time_stamp.toString()}</p>
        </div>
    )
}

export default MessageComp;