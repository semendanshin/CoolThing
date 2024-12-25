import MessagesContainer from "./MessagesContainer.tsx";
import ChatFooter from "./ChatFooter.tsx";
import ChatHeader from "./ChatHeader.tsx";
import {IMessage} from "./Message.tsx";
import "./ChatViewPort.css";


export interface IChat {
    id: string;
    userUsername: string;
    botUsername: string;
    messages: IMessage[];
    autoReply: boolean;
}


interface Props {
    chat: IChat | null;
    onSwitchAutoReply?: (autoReply: boolean) => void;
}


function ChatViewPort(
    {
        chat,
        onSwitchAutoReply
    }: Props
) {
    return (
        <div className="chat-viewport">
            {chat && onSwitchAutoReply ? <>
                <ChatHeader userUsername={chat.userUsername} botUsername={chat.botUsername} autoReply={chat.autoReply}
                            onSwitchAutoReply={onSwitchAutoReply}/>
                <MessagesContainer messages={chat.messages}/>
                <ChatFooter autoReply={chat.autoReply} />
            </> : <div className="no-chat-selected">No chat selected</div>}
        </div>
    )
}

export default ChatViewPort;
