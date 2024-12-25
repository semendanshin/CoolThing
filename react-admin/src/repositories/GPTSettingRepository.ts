import {GPTSettings} from "../types/GPTSettings.ts";

export interface GPTSettingRepository {
    getAllGPTSettings(): Promise<GPTSettings[]>;
}
