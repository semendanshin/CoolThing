from pydantic import BaseModel


class Prompt(BaseModel):
    aim: str
    prompt: str
