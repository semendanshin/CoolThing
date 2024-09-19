SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

INSERT INTO public.campaigns (welcome_message, name, chats, plus_keywords, minus_keywords, gpt_settings_id, id, created_at, updated_at, scope, new_lead_wait_interval_seconds, chat_answer_wait_interval_seconds, deleted_at) VALUES ('Hello', 'demo', '["https://t.me/+sCmhD0JS95BlZDMy"]', '["[]"]', '["[]"]', '75bc2e54-0bd5-4c3c-84be-786b464d3adf', '2ce565b5-1693-4a0b-8fcf-e86ef27dbac2', '2024-09-03 16:01:29.292475', '2024-09-03 16:01:29.292475', 'test', '180-300', '15-30', NULL);
