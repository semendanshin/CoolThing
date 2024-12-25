import {useEffect, useState} from "react";
import Card from "../components/Card.tsx";
import CardsContainer from "../components/CardsContainer.tsx";
import FloatingAddButton from "../components/FloatingAddButton.tsx";
import "./Bots.css";

interface Bot {
    id: string;
    username: string;
    app_id: string;
    campaign: string;
    role: string;
    proxy: string;
    status: string;
}


function Bots() {
    const [bots, setBots] = useState<Bot[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        function fetchBots() {
            const testBots: Bot[] = [
                {
                    id: "45022c80-50b5-4074-ba4f-44bb63e4a3bc",
                    username: "Руслан",
                    app_id: "24513346",
                    campaign: "45022c80-50b5-4074-ba4f-44bb63e4a3bc",
                    role: "Manager",
                    proxy: "No proxy",
                    status: "Stopped",
                },
                {
                    id: "f8fc8028-6227-41f4-8b18-e11a97b71273",
                    username: "Daniel Trust",
                    app_id: "25808176",
                    campaign: "No campaign",
                    role: "Parser",
                    proxy: "user123163:ml27en@178.208.184.83:19104",
                    status: "Stopped",
                },
                {
                    id: "d8fc8028-6227-41f4-8b18-e11a97b71273",
                    username: "Олег",
                    app_id: "27589084",
                    campaign: "45022c80-50b5-4074-ba4f-44bb63e4a3bc",
                    role: "Parser",
                    proxy: "No proxy",
                    status: "Active",
                },
            ];

            return testBots;
        }

        const bots = fetchBots();
        setLoading(false);
        return setBots(bots);
    }, []);

    if (loading) return <div>Loading...</div>;

    const botToCard = (bot: Bot) => {
        return (
            <Card href={`/bots/${bot.id}`} title={bot.username} attributes={[
                {name: "App ID", value: bot.app_id},
                {name: "Campaign", value: bot.campaign},
                {name: "Role", value: bot.role},
                {name: "Proxy", value: bot.proxy},
                {
                    name: "Status",
                    value: <span className={bot.status.toLowerCase() === "active" ? "status-up" : "status-down"}>
                        {bot.status}
                    </span>
                },
            ]} key={bot.id}/>
        );
    }

    return (
        <>
            <CardsContainer>
                {bots.map(botToCard)}
            </CardsContainer>
            <FloatingAddButton href={"/bots/new"}/>
        </>
    );
}

export default Bots