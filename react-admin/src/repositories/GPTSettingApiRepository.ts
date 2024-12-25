import {GPTSettingRepository} from "./GPTSettingRepository.ts";
import {GPTSettings} from "../types/GPTSettings.ts";

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

export class GPTSettingApiRepository implements GPTSettingRepository {
    private readonly base_url: string = BASE_URL;


    async getAllGPTSettings(): Promise<GPTSettings[]> {
        const response = await fetch(`${this.base_url}/gpts`);
        return response.json();
    }
}
