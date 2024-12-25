import Card from "../components/Card.tsx";
import {useEffect, useState} from "react";
import CardsContainer from "../components/CardsContainer.tsx";
import FloatingAddButton from "../components/FloatingAddButton.tsx";

interface GPTSetting {
    id: string;
    model: string;
    assistant?: string;
    service_prompt?: string;
    proxy?: string;
}

function GPTSettings() {
    const [gptSettings, setGPTSettings] = useState<GPTSetting[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        function fetchGPTSettings() {
            const testGPTSettings: GPTSetting[] = [
                {
                    id: "45022c80-50b5-4074-ba4f-44bb63e4a3bc",
                    model: "GPT-3",
                    assistant: "asst_0A9poRF87AS32IbJIJ4jJNr7",
                },
                {
                    id: "f8fc8028-6227-41f4-8b18-e11a97b71273",
                    model: "GPT-4",
                    service_prompt: "Hello, how can I help you?",
                    proxy: "user123163:ml27en@177.241.234.222:19104",
                },
            ];

            return testGPTSettings;
        }

        const gptSettings = fetchGPTSettings();
        setLoading(false);

        return setGPTSettings(gptSettings);
    }, []);

    if (loading) return <div>Loading...</div>;

    const gptSettingToCard = (gptSetting: GPTSetting) => {
        const attributes = [
            {name: "Model", value: gptSetting.model},
        ]
        if (gptSetting.assistant) {
            attributes.push({name: "Assistant", value: gptSetting.assistant});
        }
        if (gptSetting.service_prompt) {
            attributes.push({name: "Service Prompt", value: gptSetting.service_prompt});
        }
        attributes.push({name: "Proxy", value: gptSetting.proxy || "No proxy"});
        return (
            <Card href={`/gpts/${gptSetting.id}`} title={gptSetting.id} attributes={attributes} key={gptSetting.id}/>
        );
    }

    return (
        <>
            <CardsContainer>
                    {gptSettings.map(gptSettingToCard)}
            </CardsContainer>
            <FloatingAddButton href={"/gpts/new"}/>
        </>
    );
}

export default GPTSettings;
