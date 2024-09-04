from fastapi import Form

from domain.dto.gpt import GPTCreateDTO


def create_gpt_setting_form(
    name: str = Form(...),
    model: str = Form(...),
    token: str = Form(...),
    assistant: str = Form(default=""),
    service_prompt: str = Form(default=""),
    proxy: str = Form(default=""),
) -> GPTCreateDTO:
    return GPTCreateDTO(
        name=name,
        model=model,
        assistant=assistant,
        token=token,
        service_prompt=service_prompt,
        proxy=proxy,
    )
