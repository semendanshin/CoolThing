import random
import re

from abstractions.usecases.TemplateEngineInterface import TemplateEngineInterface


class TemplateEngine(TemplateEngineInterface):
    async def process_template(self, template: str) -> str:
        pattern = r"\{([^{}]+)\}"

        def replace(match):
            options = match.group(1).split('|')
            return random.choice(options)

        return re.sub(pattern, replace, template)
