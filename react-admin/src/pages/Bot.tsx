import React, {useEffect, useState} from "react";
import UpdateForm from "../components/UpdateForm";
import StatusField from "../components/StatusField";
import TextInputField from "../components/TextInputField.tsx";
import TextAreaField from "../components/TextAreaField";
import SelectField from "../components/SelectField";
import {useParams} from "react-router-dom";

interface Bot {
    id: string;
    status: string;
    username: string;
    bio: string | null;
    app_id: string;
    app_hash: string;
    session_string: string;
    proxy: string | null;
    campaign_id: string | null;
    role: string;
}

interface Campaign {
    id: string;
    scope: string;
}

interface Props {
    bot: Bot;
    campaigns: Campaign[];
    deleteEntity: (id: string) => void;
}

const Bot: React.FC<Props> = ({ bot, campaigns, deleteEntity }) => {
    const [formData, setFormData] = useState(bot);

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = event.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value,
        }));
    };

    const handleStatusChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setFormData(prevState => ({
            ...prevState,
            status: event.target.checked ? "active" : "inactive",
        }));
    };

    const handleSaveChanges = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        console.log("Saving changes with data:", formData);
    };

    return (
        <UpdateForm
            header="Bot Details"
            entity="bot"
            deleteEntity={() => deleteEntity(bot.id)}
        >
            <form onSubmit={handleSaveChanges}>
                <StatusField status={formData.status} onChange={handleStatusChange} />
                <TextInputField label="Username" name="username" value={formData.username} onChange={handleInputChange} required />
                <TextAreaField label="Bio" name="bio" value={formData.bio} onChange={handleInputChange} />
                <TextInputField label="App ID" name="app_id" value={formData.app_id} onChange={handleInputChange} />
                <TextInputField label="App Hash" name="app_hash" value={formData.app_hash} onChange={handleInputChange} />
                <TextInputField label="Session String" name="session_string" value={formData.session_string} onChange={handleInputChange} />
                <TextInputField label="Proxy" name="proxy" value={formData.proxy || ""} onChange={handleInputChange} placeholder="http://user:pass@host:port" />
                <SelectField
                    label="Campaign"
                    name="campaign_id"
                    value={formData.campaign_id}
                    options={campaigns.map(campaign => ({ value: campaign.id, label: campaign.scope }))}
                    onChange={handleInputChange}
                />
                <SelectField
                    label="Role"
                    name="role"
                    value={formData.role}
                    options={[
                        { value: "manager", label: "Manager" },
                        { value: "parser", label: "Parser" },
                    ]}
                    onChange={handleInputChange}
                />
                <div className="row">
                    <input type="submit" value="Save Changes" className="submit-button" />
                </div>
            </form>
        </UpdateForm>
    );
};

const UpdateBotPage: React.FC = () => {
    const { id } = useParams(); // Get bot id from URL
    const [bot, setBot] = useState<Bot | null>(null);
    const [campaigns, setCampaigns] = useState<Campaign[]>([]);

    // Fetch bot data when component mounts
    useEffect(() => {
        if (id) {
            // // Fetch bot details by id (replace with your actual API call)
            // fetch(`/api/bots/${id}`)
            //     .then(response => response.json())
            //     .then(data => setBot(data))
            //     .catch(error => console.error("Error fetching bot data:", error));
            //
            // // Fetch campaign data (replace with your actual API call)
            // fetch('/api/campaigns')
            //     .then(response => response.json())
            //     .then(data => setCampaigns(data))
            //     .catch(error => console.error("Error fetching campaigns:", error));

            // Setting fake bot data based on the UUID id
            const fakeBot: Bot = {
                id: id,
                status: 'active',
                username: 'bot_' + id,
                bio: 'This is a fake bot with UUID ' + id,
                app_id: 'app-id-' + id,
                app_hash: 'app-hash-' + id,
                session_string: 'session-' + id,
                proxy: 'http://proxy.fake/' + id,
                campaign_id: 'campaign-id-' + id,
                role: 'manager',
            };
            setBot(fakeBot);

            // Setting fake campaigns data
            const fakeCampaigns: Campaign[] = [
                { id: 'campaign-id-1', scope: 'Campaign 1' },
                { id: 'campaign-id-2', scope: 'Campaign 2' },
                { id: 'campaign-id-3', scope: 'Campaign 3' },
            ];
            setCampaigns(fakeCampaigns);
        }
    }, [id]);

    if (!bot || !campaigns.length) {
        return <div>Loading...</div>; // Loading state
    }

    const deleteEntity = (id: string) => {
        console.log(`Deleting bot with id: ${id}`);
    };

    return (
        <Bot
            bot={bot}
            campaigns={campaigns}
            deleteEntity={deleteEntity}
        />
    );
};

export default UpdateBotPage;
