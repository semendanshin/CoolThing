import { useCampaignRepository } from "../context/CampaignRepositoryContext.tsx";
import {UpdateCampaignDTO} from "../repositories/CampaignRepository.ts";

export const useCampaigns = () => {
    const repository = useCampaignRepository();

    const fetchCampaigns = async () => {
        return await repository.getAllCampaigns();
    };

    const fetchCampaignById = async (id: string) => {
        return await repository.getCampaignById(id);
    };

    const deleteCampaign = async (id: string) => {
        return await repository.deleteCampaign(id);
    }

    const updateCampaign = async (id: string, dto: UpdateCampaignDTO) => {
        return await repository.updateCampaign(id, dto);
    }

    return { fetchCampaigns, fetchCampaignById, deleteCampaign, updateCampaign };
};
