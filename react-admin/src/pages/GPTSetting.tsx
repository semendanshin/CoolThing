import React, { useEffect, useState } from "react";
import UpdateForm from "../components/UpdateForm";
import TextInputField from "../components/TextInputField";
import TextAreaField from "../components/TextAreaField";
import { useParams } from "react-router-dom";

interface GPTSetting {
    id: string;
    model: string;
    token: string;
    assistant: string;
    service_prompt: string;
    proxy: string;
}

interface Props {
    gptSetting: GPTSetting;
    deleteEntity: (id: string) => void;
}

const GPTSettingForm: React.FC<Props> = ({ gptSetting, deleteEntity }) => {
    const [formData, setFormData] = useState(gptSetting);

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        const { name, value } = event.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value,
        }));
    };

    const handleSaveChanges = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        console.log("Saving changes with data:", formData);
    };

    return (
        <UpdateForm
            header="GPT Setting Details"
            entity="gpt_setting"
            deleteEntity={() => deleteEntity(gptSetting.id)}
        >
            <form onSubmit={handleSaveChanges}>
                <TextInputField label="Model" name="model" value={formData.model} onChange={handleInputChange} />
                <TextInputField label="Token" name="token" value={formData.token} onChange={handleInputChange} />
                <TextInputField label="Assistant ID" name="assistant" value={formData.assistant} onChange={handleInputChange} />
                <TextAreaField label="Service Prompt" name="service_prompt" value={formData.service_prompt} onChange={handleInputChange} />
                <TextInputField label="Proxy" name="proxy" value={formData.proxy} onChange={handleInputChange} placeholder="socks5://username:password@host:port" />
                <div className="row">
                    <input type="submit" value="Save Changes" className="submit-button" />
                </div>
            </form>
        </UpdateForm>
    );
};

const UpdateGPTSettingPage: React.FC = () => {
    const { id } = useParams();
    const [gptSetting, setGptSetting] = useState<GPTSetting | null>(null);

    useEffect(() => {
        if (id) {
            const fakeGPTSetting: GPTSetting = {
                id,
                model: "GPT-3",
                token: "fake-token",
                assistant: "asst_0A9p3q4r5s6t3dH2Gd",
                service_prompt: "Sample service prompt.",
                proxy: "socks5://user:pass@host:port",
            };
            setGptSetting(fakeGPTSetting);
        }
    }, [id]);

    if (!gptSetting) {
        return <div>Loading...</div>;
    }

    const deleteEntity = (id: string) => {
        console.log(`Deleting GPT setting with id: ${id}`);
    };

    return (
        <GPTSettingForm
            gptSetting={gptSetting}
            deleteEntity={deleteEntity}
        />
    );
};

export default UpdateGPTSettingPage;
