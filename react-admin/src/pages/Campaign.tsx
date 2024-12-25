import React, { useEffect, useState } from "react";
import UpdateForm from "../components/UpdateForm";
import TextInputField from "../components/TextInputField";
import TextAreaField from "../components/TextAreaField";
import SelectField from "../components/SelectField";
import NumberRangeField from "../components/NumberRangeField";
import {useParams, useNavigate} from "react-router-dom";
import {useCampaigns} from "../hooks/useCampaignRepository.ts";
import {Campaign} from "../types/Campaign.ts";
import {useGPTSetting} from "../hooks/useGPTSettingRepository.ts";

interface GPTSetting {
    id: string;
}

interface Props {
    campaign: Campaign;
    gptSettings: GPTSetting[];
}

interface FormData {
    id: string;
    scope: string;
    welcome_message: string;
    chats: string
    plus_keywords: string
    minus_keywords: string
    chat_answer_wait_interval_seconds_start: string;
    chat_answer_wait_interval_seconds_end: string;
    new_lead_wait_interval_seconds_start: string;
    new_lead_wait_interval_seconds_end: string;
    gpt_settings_id: string;
}


const CampaignForm: React.FC<Props> = ({ campaign, gptSettings }) => {
    const [formData, setFormData] = useState<FormData>({
        id: campaign.id,
        scope: campaign.scope,
        welcome_message: campaign.welcome_message,
        chats: campaign.chats.join(", "),
        plus_keywords: campaign.plus_keywords.join(", "),
        minus_keywords: campaign.minus_keywords.join(", "),
        chat_answer_wait_interval_seconds_start: campaign.chat_answer_wait_interval_seconds.split("-")[0],
        chat_answer_wait_interval_seconds_end: campaign.chat_answer_wait_interval_seconds.split("-")[1],
        new_lead_wait_interval_seconds_start: campaign.new_lead_wait_interval_seconds.split("-")[0],
        new_lead_wait_interval_seconds_end: campaign.new_lead_wait_interval_seconds.split("-")[1],
        gpt_settings_id: campaign.gpt_settings_id,
    });

    const repository = useCampaigns();
    const navigate = useNavigate();

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = event.target;
        console.log(name, value);
        setFormData(prevState => ({
            ...prevState,
            [name]: value,
        }));
    };

    const handleSaveChanges = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        console.log("Saving changes with data:", formData);
        if (formData.gpt_settings_id === "") {
            alert("Please enter a valid gpt_settings id");
            return;
        }
        repository.updateCampaign(formData.id, {
            scope: formData.scope,
            welcome_message: formData.welcome_message,
            chats: formData.chats.split(",").map(keyword => keyword.trim()),
            plus_keywords: formData.plus_keywords.split(",").map(keyword => keyword.trim()),
            minus_keywords: formData.minus_keywords.split(",").map(keyword => keyword.trim()),
            gpt_settings_id: formData.gpt_settings_id,
            chat_answer_wait_interval_seconds: formData.chat_answer_wait_interval_seconds_start + '-' + formData.chat_answer_wait_interval_seconds_end,
            new_lead_wait_interval_seconds: formData.new_lead_wait_interval_seconds_start + '-' + formData.new_lead_wait_interval_seconds_end,
        }).catch((err) => {
            console.log(err);
        })
    };

    const deleteEntity = (id: string) => {
        repository.deleteCampaign(id).catch((err) => {
            console.log(err);
        })
        navigate("/campaigns")
    };

    return (
        <UpdateForm
            header="Campaign Details"
            entity="campaign"
            deleteEntity={() => deleteEntity(campaign.id)}
        >
            <form onSubmit={handleSaveChanges}>
                <TextInputField label="Scope" name="scope" value={formData.scope} onChange={handleInputChange} required />
                <TextAreaField label="Welcome Message" name="welcome_message" value={formData.welcome_message} onChange={handleInputChange} />
                <TextAreaField label="Chats" name="chats" value={formData.chats} onChange={handleInputChange} />
                <TextAreaField label="Plus Keywords" name="plus_keywords" value={formData.plus_keywords} onChange={handleInputChange} />
                <TextAreaField label="Minus Keywords" name="minus_keywords" value={formData.minus_keywords} onChange={handleInputChange} />

                <NumberRangeField
                    id="chat_answer_wait_interval_seconds"
                    label="In-chat answer delay interval (seconds)"
                    labelStart="From"
                    labelEnd="To"
                    startValue={formData.chat_answer_wait_interval_seconds_start}
                    endValue={formData.chat_answer_wait_interval_seconds_end}
                    onChangeStart={handleInputChange}
                    onChangeEnd={handleInputChange}
                />

                <NumberRangeField
                    id="new_lead_wait_interval_seconds"
                    label="Welcome message delay interval (seconds)"
                    labelStart="From"
                    labelEnd="To"
                    startValue={formData.new_lead_wait_interval_seconds_start}
                    endValue={formData.new_lead_wait_interval_seconds_end}
                    onChangeStart={handleInputChange}
                    onChangeEnd={handleInputChange}
                />

                <SelectField
                    label="GPT Settings"
                    name="gpt_settings_id"
                    value={formData.gpt_settings_id}
                    options={gptSettings.map(setting => ({ value: setting.id, label: setting.id }))}
                    onChange={handleInputChange}
                />
                <div className="row">
                    <input type="submit" value="Save Changes" className="submit-button" />
                </div>
            </form>
        </UpdateForm>
    );
};

const UpdateCampaignPage: React.FC = () => {
    const { id } = useParams();
    const [campaign, setCampaign] = useState<Campaign | null>(null);
    const [gptSettings, setGptSettings] = useState<GPTSetting[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const campaignsRepository = useCampaigns();
    const gptsRepository = useGPTSetting()

    useEffect(() => {
        if (id) {
            const fetchCampaigns = async () => {
                try {
                    const data = await campaignsRepository.fetchCampaignById(id);
                    setCampaign(data);
                } catch (err) {
                    console.log(err);
                    setError("Failed to fetch campaigns");
                } finally {
                    setLoading(false);
                }
            }
            fetchCampaigns().finally();

            const fetchGPTSettings = async () => {
                try {
                    const data = await gptsRepository.fetchGPTSetting();
                    setGptSettings(data);
                } catch (err) {
                    console.log(err);
                    setError("Failed to fetch campaigns");
                } finally {
                    setLoading(false);
                }
            }
            fetchGPTSettings().finally();
        }
    }, [id]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <CampaignForm
            campaign={campaign!}
            gptSettings={gptSettings}
        />
    );
};

export default UpdateCampaignPage;
