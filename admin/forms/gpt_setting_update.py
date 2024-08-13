from fastapi import Form, Path

from domain.dto.gpt import GPTUpdateDTO


def update_gpt_setting_form(
    id: str = Path(..., alias="gpt_id"),
    model: str = Form(default=""),
    token: str = Form(default=""),
    proxy: str = Form(default=""),
    assistant: str = Form(default=""),
    service_prompt: str = Form(default=""),
) -> GPTUpdateDTO:
    return GPTUpdateDTO(
        id=id,
        model=model,
        assistant=assistant,
        token=token,
        service_prompt=service_prompt,
        proxy=proxy,
    )
