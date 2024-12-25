import Slider from "./Slider.tsx";
import "./ChatHeader.css";


interface Props {
    userUsername: string;
    botUsername: string;
    autoReply: boolean;
    onSwitchAutoReply: (autoReply: boolean) => void;
}

function ChatHeader(
    {
        userUsername,
        botUsername,
        autoReply,
        onSwitchAutoReply,
    }: Props
) {
    return (
        <div className="chat-header">
            <a href="/chats" className="back-button">
                <i className="fa fa-long-arrow-left" aria-hidden="true"></i>
            </a>
            <span className="header-text header-hide"><b>User: </b>{userUsername}</span>
            <span className="header-text header-hide"><b>Bot: </b>{botUsername}</span>
            <div className={"header-auto-reply-container"}>
                <span className="header-text"><b>Auto reply: </b></span>
                <Slider size="small" isOn={autoReply} onSwitch={onSwitchAutoReply}/>
            </div>
        </div>
    );
}

export default ChatHeader;