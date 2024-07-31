from fastapi import Form

from domain.dto.gpt import GPTUpdateDTO


def update_gpt_setting_form(
    model: str = Form(default=""),
    assistant: str = Form(default=""),
    token: str = Form(default=""),
    service_prompt: str = Form(default=""),
) -> GPTUpdateDTO:
    return GPTUpdateDTO(
        model=model,
        assistant=assistant,
        token=token,
        service_prompt=service_prompt,
    )
