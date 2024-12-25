import Message, {IMessage} from "./Message";
import "./MessagesContainer.css"

interface Props {
    messages: IMessage[];
}


function MessagesContainer(
    {
        messages
    }: Props
) {
    return (
        <div className={"messages"}>
            {messages.map((message, index) => {
                return (
                    <Message key={index} message={message}/>
                )
            })}
            <br></br>
        </div>
    );
}

export default MessagesContainer