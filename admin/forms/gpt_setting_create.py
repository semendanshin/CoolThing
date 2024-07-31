from fastapi import Form

from domain.dto.gpt import GPTCreateDTO


def create_gpt_setting_form(
    model: str = Form(...),
    token: str = Form(...),
    assistant: str = Form(default=""),
    service_prompt: str = Form(default=""),
) -> GPTCreateDTO:
    return GPTCreateDTO(
        model=model,
        assistant=assistant,
        token=token,
        service_prompt=service_prompt,
    )
