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

INSERT INTO public.gpt_settings (model, name, assistant, token, id, created_at, updated_at, service_prompt, proxy, deleted_at) VALUES ('123', 'demo', 'fef2', '1234', '75bc2e54-0bd5-4c3c-84be-786b464d3adf', '2024-09-03 16:00:24.411757', '2024-09-03 16:00:24.411757', '', '', NULL);
