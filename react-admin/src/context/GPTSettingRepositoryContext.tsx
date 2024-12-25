import React, { createContext, useContext } from "react";
import { GPTSettingRepository } from "../repositories/GPTSettingRepository.ts";
import { GPTSettingApiRepository } from "../repositories/GPTSettingApiRepository.ts";

const GPTSettingRepositoryContext = createContext<GPTSettingRepository | null>(null);

export const GPTSettingRepositoryProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const repository = new GPTSettingApiRepository(); // Switch to MockRepo for testing
    return (
        <GPTSettingRepositoryContext.Provider value={repository}>
            {children}
        </GPTSettingRepositoryContext.Provider>
    );
};

export const useGPTSettingRepository = (): GPTSettingRepository => {
    const context = useContext(GPTSettingRepositoryContext);
    if (!context) {
        throw new Error("useGPTSettingRepository must be used within a GPTSettingRepositoryProvider");
    }
    return context;
};
