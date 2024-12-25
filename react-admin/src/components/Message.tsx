import "./Message.css"

export interface IMessage {
    text: string;
    isOutgoing: boolean;
}

interface Props {
    message: IMessage;
}

function Message(
    {
        message
    }: Props
) {
    return (
        <div className={`message ${message.isOutgoing ? 'outgoing' : 'incoming'}`}>
            {message.text}
        </div>
    );
}

export default Message;