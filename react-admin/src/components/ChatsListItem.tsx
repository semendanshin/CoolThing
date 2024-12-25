import "./ChatsListItem.css";
export interface ChatItem {
    id: string;
    userUsername: string;
    botUsername: string;
    lastMessage: string;
    unreadCount?: number;
}

interface Props {
    chatItem: ChatItem;
    onChatClick: (chat: ChatItem) => void;
}

function ChatsListItem(
    {chatItem, onChatClick}: Props
) {
    return (
        <a href="#" onClick={() => onChatClick(chatItem)}>
            <div className="chat-item">
                <div className="chat-item-content">
                    <div className="chat-item-info">
                        <span className="bot-name"><b>{chatItem.botUsername}</b></span>
                        <span className="user-name"><b>{chatItem.userUsername}</b></span>
                    </div>
                    <div className="chat-item-message">
                        <span className="last-message">{chatItem.lastMessage}</span>
                    </div>
                </div>
            </div>
        </a>
    )
}

export default ChatsListItem;
