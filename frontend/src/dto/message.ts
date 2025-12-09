export interface Message {
    message_id: string;
    sender_id: string;
    recipient_id: string;
    time_stamp: Date;
    message: string;
}

export interface GetMessageResponse {
    messages: Array<Message>;
}

export interface PostMessageRequest {
    recipient_id: string;
    message: string;
}

export interface PostMessageResponse {
    success: boolean;
}