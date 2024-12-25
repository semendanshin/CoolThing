import { useGPTSettingRepository } from "../context/GPTSettingRepositoryContext.tsx";

export const useGPTSetting = () => {
    const repository = useGPTSettingRepository();

    const fetchGPTSetting = async () => {
        return await repository.getAllGPTSettings();
    };
    return { fetchGPTSetting };
};
