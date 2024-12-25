import React, { createContext, useContext } from "react";
import { CampaignRepository } from "../repositories/CampaignRepository";
import { CampaignApiRepository } from "../repositories/CampaignApiRepository.ts";

const CampaignRepositoryContext = createContext<CampaignRepository | null>(null);

export const CampaignRepositoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const repository = new CampaignApiRepository(); // Switch to MockRepo for testing
    return (
        <CampaignRepositoryContext.Provider value={repository}>
            {children}
        </CampaignRepositoryContext.Provider>
    );
};

export const useCampaignRepository = (): CampaignRepository => {
    const context = useContext(CampaignRepositoryContext);
    if (!context) {
        throw new Error("useCampaignRepository must be used within a CampaignRepositoryProvider");
    }
    return context;
};
