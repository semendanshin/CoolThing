import {Campaign} from "../types/Campaign.ts";

export interface CreateCampaignDTO {
    scope: string;
    welcome_message: string;
    chats: string;
    plus_keywords: string;
    minus_keywords: string;
    gpt_settings_id: string;
}

export interface UpdateCampaignDTO {
    scope: string;
    welcome_message: string;
    chats: string[];
    plus_keywords: string[];
    minus_keywords: string[];
    gpt_settings_id: string;
    chat_answer_wait_interval_seconds: string;
    new_lead_wait_interval_seconds: string;
}

export interface CampaignRepository {
    getAllCampaigns(): Promise<Campaign[]>;
    getCampaignById(id: string): Promise<Campaign | null>;
    createCampaign(campaign: CreateCampaignDTO): Promise<Campaign>;
    updateCampaign(id: string, campaign: UpdateCampaignDTO): Promise<void>;
    deleteCampaign(id: string): Promise<void>;
}
