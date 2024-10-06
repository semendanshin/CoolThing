from abc import ABC, abstractmethod


class TemplateEngineInterface(ABC):
    @abstractmethod
    async def process_template(self, template: str) -> str:
        ...
