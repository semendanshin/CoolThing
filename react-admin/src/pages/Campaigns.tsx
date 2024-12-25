import {useEffect, useState} from "react";
import Card from "../components/Card.tsx";
import CardsContainer from "../components/CardsContainer.tsx";
import FloatingAddButton from "../components/FloatingAddButton.tsx";
import {Campaign} from "../types/Campaign.ts";
import {useCampaigns} from "../hooks/useCampaignRepository.ts";

function Campaigns() {
    const [campaigns, setCampaigns] = useState<Campaign[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const repository = useCampaigns();

    useEffect(() => {
        const fetchCampaigns = async () => {
            try {
                const data = await repository.fetchCampaigns();
                setCampaigns(data);
            } catch (err) {
                console.log(err);
                setError("Failed to fetch campaigns");
            } finally {
                setLoading(false);
            }
        };

        fetchCampaigns().finally();
    }, [""]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    const campaignToCard = (campaign: Campaign) => {
        return (
            <Card
                href={`/campaigns/${campaign.id}`}
                title={campaign.id}
                attributes={[
                    { name: "Scope", value: campaign.scope },
                    { name: "Welcome Message", value: campaign.welcome_message },
                    { name: "Chats", value: campaign.chats.join(", ") },
                    { name: "Plus Keywords", value: campaign.plus_keywords.join(", ") },
                    { name: "Minus Keywords", value: campaign.minus_keywords.join(", ") },
                    { name: "GPT Settings ID", value: campaign.gpt_settings_id },
                ]}
                key={campaign.id}
            />
        );
    };

    return (
        <>
            <CardsContainer>
                {campaigns.map(campaignToCard)}
            </CardsContainer>
            <FloatingAddButton href={"/campaigns/new"} />
        </>
    );
}

export default Campaigns;