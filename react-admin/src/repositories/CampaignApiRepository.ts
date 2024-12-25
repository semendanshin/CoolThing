import { CampaignRepository, CreateCampaignDTO, UpdateCampaignDTO } from "./CampaignRepository";
import { Campaign } from "../types/Campaign";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

export class CampaignApiRepository implements CampaignRepository {
    private readonly base_url: string = BASE_URL;

    async getAllCampaigns(): Promise<Campaign[]> {
        const response = await fetch(`${this.base_url}/campaigns`);
        return response.json();
    }

    async getCampaignById(id: string): Promise<Campaign | null> {
        const response = await fetch(`${this.base_url}/campaigns/${id}`);
        return response.ok ? response.json() : null;
    }

    async createCampaign(campaign: CreateCampaignDTO): Promise<Campaign> {
        const response = await fetch(`${this.base_url}/campaigns`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(campaign),
        });
        return response.json();
    }

    async updateCampaign(id: string, campaign: UpdateCampaignDTO): Promise<void> {
        await fetch(`${this.base_url}/campaigns/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(campaign),
        });
    }

    async deleteCampaign(id: string): Promise<void> {
        await fetch(`${this.base_url}/campaigns/${id}`, { method: 'DELETE' });
    }
}
