export interface Campaign {
    id: string;
    scope: string;
    welcome_message: string;
    chats: string[];
    plus_keywords: string[];
    minus_keywords: string[];
    gpt_settings_id: string;
    chat_answer_wait_interval_seconds: string;
    new_lead_wait_interval_seconds: string;
}
