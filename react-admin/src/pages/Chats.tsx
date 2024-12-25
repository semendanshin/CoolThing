import {useEffect, useState} from "react";
import {ChatItem} from "../components/ChatsListItem.tsx";
import ChatsList from "../components/ChatsList.tsx";
import ChatViewPort, {IChat} from "../components/ChatViewPort.tsx";
import "./Chats.css";

const chats: IChat[] = [
    {
        id: "2f5b4b9e-4b7b-4b7b-8b7b-4b7b4b7b4b7b",
        userUsername: 'User',
        botUsername: 'Bot',
        messages: [
            {
                text: 'Hello!',
                isOutgoing: false
            },
            {
                text: 'Hi!',
                isOutgoing: true
            }
        ],
        autoReply: true
    },
    {
        id: "ag3b4b9e-4b7b-4b7b-8b7b-4b7b4b7b4b7b",
        userUsername: 'User2',
        botUsername: 'Bot2',
        messages: [
            {
                text: 'Hello!',
                isOutgoing: false
            },
            {
                text: 'Hi!',
                isOutgoing: true
            },
            {
                text: 'How are you?',
                isOutgoing: true
            }
        ],
        autoReply: false
    },
    {
        id: "90430185-f6da-48e0-ad00-8a3b79676245",
        "userUsername": 'semendanshin',
        "botUsername": 'Руслан',
        messages: [
            {
                "text": "Вложения в недвижимость могут быть одним из способов увеличить свое богатство. Однако важно также обратить внимание на другие аспекты финансового планирования, такие как инвестиции, сбережения и разнообразные источники дохода. Поговорить с финансовым консультантом может быть хорошей идеей для создания стратегии достижения финансовых целей. Если возникнут еще вопросы, с удовольствием помогу разобраться!",
                "isOutgoing": false
            },
            {
                "text": "Хочу виллу, как разбогатеть",
                "isOutgoing": true
            },
            {
                "text": "Прогнозировать будущее в политике сложно, так как много факторов влияет на исход выборов. Следи за новостями и аналитикой, чтобы быть в курсе событий! Если нужна помощь с другими вопросами, обращайся.",
                "isOutgoing": false
            },
            {
                "text": "Следующий вопрос: кто станет президентом сша на выборах в 2024 году",
                "isOutgoing": true
            },
            {
                "text": "Пожалуйста! Если у тебя возникнут еще вопросы, обращайся. Хорошего дня!",
                "isOutgoing": false
            },
            {
                "text": "Спс",
                "isOutgoing": true
            },
            {
                "text": "Не уверен насчет ос, но если рассматривать пчелу, то ее полетная дальность может достигать до 5-10 километров без посадок. Надеюсь, это информация окажется полезной!",
                "isOutgoing": false
            },
            {
                "text": "Есть вопрос сколько может пролететь оса беспосадочно",
                "isOutgoing": true
            },
            {
                "text": "Извини, но я не имею контактов агента по недвижимости. Надеюсь, ты найдешь подходящее агентство для своих потребностей. Если возникнут другие вопросы, с удовольствием помогу!",
                "isOutgoing": false
            },
            {
                "text": "Ага давай",
                "isOutgoing": true
            },
            {
                "text": "Привет! Видел ты ищешь агента по недвиге, У меня есть контакты, могу отправить.",
                "isOutgoing": false
            },
            {
                "text": "Хочу виллу, как разбогатеть",
                "isOutgoing": true
            },
            {
                "text": "Прогнозировать будущее в политике сложно, так как много факторов влияет на исход выборов. Следи за новостями и аналитикой, чтобы быть в курсе событий! Если нужна помощь с другими вопросами, обращайся.",
                "isOutgoing": false
            },
            {
                "text": "Следующий вопрос: кто станет президентом сша на выборах в 2024 году",
                "isOutgoing": true
            },
            {
                "text": "Пожалуйста! Если у тебя возникнут еще вопросы, обращайся. Хорошего дня!",
                "isOutgoing": false
            },
            {
                "text": "Спс",
                "isOutgoing": true
            },
            {
                "text": "Не уверен насчет ос, но если рассматривать пчелу, то ее полетная дальность может достигать до 5-10 километров без посадок. Надеюсь, это информация окажется полезной!",
                "isOutgoing": false
            },
            {
                "text": "Есть вопрос сколько может пролететь оса беспосадочно",
                "isOutgoing": true
            },
            {
                "text": "Извини, но я не имею контактов агента по недвижимости. Надеюсь, ты найдешь подходящее агентство для своих потребностей. Если возникнут другие вопросы, с удовольствием помогу!",
                "isOutgoing": false
            },
            {
                "text": "Ага давай",
                "isOutgoing": true
            },
            {
                "text": "Привет! Видел ты ищешь агента по недвиге, У меня есть контакты, могу отправить.",
                "isOutgoing": false
            },
            {
                "text": "Хочу виллу, как разбогатеть",
                "isOutgoing": true
            },
            {
                "text": "Прогнозировать будущее в политике сложно, так как много факторов влияет на исход выборов. Следи за новостями и аналитикой, чтобы быть в курсе событий! Если нужна помощь с другими вопросами, обращайся.",
                "isOutgoing": false
            },
            {
                "text": "Следующий вопрос: кто станет президентом сша на выборах в 2024 году",
                "isOutgoing": true
            },
            {
                "text": "Пожалуйста! Если у тебя возникнут еще вопросы, обращайся. Хорошего дня!",
                "isOutgoing": false
            },
            {
                "text": "Спс",
                "isOutgoing": true
            },
            {
                "text": "Не уверен насчет ос, но если рассматривать пчелу, то ее полетная дальность может достигать до 5-10 километров без посадок. Надеюсь, это информация окажется полезной!",
                "isOutgoing": false
            },
            {
                "text": "Есть вопрос сколько может пролететь оса беспосадочно",
                "isOutgoing": true
            },
            {
                "text": "Извини, но я не имею контактов агента по недвижимости. Надеюсь, ты найдешь подходящее агентство для своих потребностей. Если возникнут другие вопросы, с удовольствием помогу!",
                "isOutgoing": false
            },
            {
                "text": "Ага давай",
                "isOutgoing": true
            },
            {
                "text": "Привет! Видел ты ищешь агента по недвиге, У меня есть контакты, могу отправить.",
                "isOutgoing": false
            }
        ],
        autoReply: false
    },
];

function Chats() {
    const [activeChat, setActiveChat] = useState<IChat | null>(null);
    const [chatItems, setChatItems] = useState<ChatItem[]>([]);

    useEffect(() => {
        const handleEsc = (event: KeyboardEvent) => {
            if (event.key === "Escape") {
                setActiveChat(null);
            }
        };
        window.addEventListener("keydown", handleEsc);
        return () => {
            window.removeEventListener("keydown", handleEsc);
        };
    }, []);

    function getChat(id: string): IChat {
        return chats.find(chat => chat.id === id)!;
    }

    function onChatClick(chat: ChatItem) {
        setActiveChat(getChat(chat.id));
    }

    useEffect(() => {
        setChatItems(chats.map(chat => {
            return {
                id: chat.id,
                userUsername: chat.userUsername,
                botUsername: chat.botUsername,
                lastMessage: chat.messages[chat.messages.length - 1].text,
                autoReply: chat.autoReply
            }
        }));
    }, []);

    return (
        <div className={"container chats-page"}>
            <ChatsList chats={chatItems} onChatClick={onChatClick}/>
            <ChatViewPort chat={activeChat} onSwitchAutoReply={(autoReply) => {
                if (activeChat) {
                    activeChat.autoReply = autoReply;
                    setActiveChat({...activeChat});
                }
            }
            }/>
        </div>
    )
}

export default Chats;