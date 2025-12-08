import { useContext, useEffect, useState } from 'react';
import { type GetMessageResponse } from '../../dto';
import {Message} from '../../components/message';
import { AuthContext, ConfigContext } from '../../context';
import { getMessages } from '../../api';
import { useSearchParams } from 'react-router-dom';

function Messages() {
    const auth = useContext(AuthContext);
    const config = useContext(ConfigContext);

    const [searchParams, setSearchParams] = useSearchParams();
    const outbound_user_id: string | null = searchParams.get("user");

    if (!outbound_user_id) return (
        <div>
            <h1>Must include ?user=""</h1>
        </div>
    )

    const [messages, setMessages] = useState<GetMessageResponse | null>(null);

    const compGetMessages = async () => {
         setMessages(await getMessages(config.BACKEND_URL, auth.token!, outbound_user_id));
    }

    useEffect(() => {
        const inner = async () => {
            await compGetMessages();
        }
        inner();
    }, [])

    return (
        <div>
            <ul>
                {messages?.messages.map((value) => 
                    <Message key={value.message_id}/>
                )}
            </ul>
        </div>
    )
}

export default Messages;