import "./ChatFooter.css"

interface Props {
    autoReply: boolean;
}

function ChatFooter(
    {autoReply}: Props
) {
    return (
        <form action="/chats/{{ chat.info.id }}/send" method="post" className="input-area">
            <label>
                <input type="text" name="message" placeholder="Напишите сообщение..." id="messageInput"/>
            </label>
            <button disabled={autoReply}>Отправить</button>
        </form>
    )
}

export default ChatFooter;