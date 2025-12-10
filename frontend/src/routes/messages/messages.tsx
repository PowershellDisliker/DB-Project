import { useContext, useEffect, useRef, useState } from 'react';
import { type GetMessageResponse, type PostMessageRequest } from '../../dto';
import { MessageComp } from '../../components/message';
import { ConfigContext } from '../../context';
import { getMessages } from '../../api';
import { useSearchParams } from 'react-router-dom';
import { postUserMessage } from '../../api';
import { useCookies } from 'react-cookie';
import globalStyles from '../../global.module.css';

function Messages() {
    const config = useContext(ConfigContext);
    const [cookies] = useCookies(['jwt', 'id']);

    const [reload, setReload] = useState<boolean>(false);
    const inputRef = useRef<HTMLInputElement>(null);

    const [searchParams] = useSearchParams();
    const outbound_user_id: string | null = searchParams.get("user");

    if (!outbound_user_id) return (
        <div>
            <h1>Must include ?user=""</h1>
        </div>
    )

    const [messages, setMessages] = useState<GetMessageResponse | null>(null);
    const [messageInput, setMessageInput] = useState<string>("");

    const compGetMessages = async () => {
         setMessages(await getMessages(config.BACKEND_URL, cookies.jwt, outbound_user_id));
    }

    useEffect(() => {
        const inner = async () => {
            await compGetMessages();
        }
        inner();
    }, [reload])

    const sendHandler = async () => {
        await postUserMessage(config.BACKEND_URL, cookies.jwt, {
            recipient_id: outbound_user_id,
            message: messageInput,
        } as PostMessageRequest);
        inputRef.current!.value = "";
        setReload(true);
    }

    return (
        <div className={globalStyles.center}>
            <ul>
                {messages?.messages?.map((value) => 
                    <MessageComp sender_id={value.sender_id} recipient_id={value.recipient_id} time_stamp={value.time_stamp} message={value.message} message_id={value.message_id} key={value.message_id}/>
                )}
            </ul>
            <input type="text" onChange={(event) => setMessageInput(event.target.value)} ref={inputRef}/>
            <button onClick={sendHandler}>Send</button>
        </div>
    )
}

export default Messages;