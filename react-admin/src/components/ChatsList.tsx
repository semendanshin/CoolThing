import ChatsListItem, { ChatItem } from "./ChatsListItem";
import "./ChatsList.css";

interface Props {
    chats: ChatItem[];
    onChatClick: (chat: ChatItem) => void;
}

function ChatsList(
    {chats, onChatClick}: Props
) {
    return (
        <div className="chats-list">
            {chats.map(chat => (
                <ChatsListItem key={chat.id} chatItem={chat} onChatClick={onChatClick}/>
            ))}
        </div>
    )
}

export default ChatsList;