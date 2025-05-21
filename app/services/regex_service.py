import re
import sys
import textwrap
import asyncio
import logging

from app.infrastructure.ai_worker import CharacterFactory

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logger = logging.getLogger(__name__)

class RegexService:
    def __init__(self):
        self.character = CharacterFactory.create("regex")

    def extract_tagged(self, text: str, tag: str):
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        if start_tag not in text or end_tag not in text:
            raise ValueError(f"Missing <{tag}> tags")
        return text.split(start_tag)[-1].split(end_tag)[0].strip()

    def _remove_imports(self, code: str) -> str:
        cleaned_lines = []
        for line in code.splitlines():
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                continue
            cleaned_lines.append(line)
        return "\n".join(cleaned_lines)

    async def generate_regex(self, prompt: str) -> str:
        base_prompt = f"""Здравствуйте! Пожалуйста, помогите мне с регулярными выражениями.
Описание проблемы: {prompt}"""

        error = None
        while True:
            try:
                message = base_prompt
                if error:
                    message += f"\n\n{error}"

                result = await self.character.ask(message)
                regex = self.extract_tagged(result, "regex")
                python_test = self.extract_tagged(result, "python")

                re.compile(regex)
                python_test = textwrap.dedent(python_test)
                python_test = self._remove_imports(python_test)
                exec(python_test, {"__builtins__": __builtins__, "re": re})
                return regex
            except Exception as e:
                logger.warning(f"Retrying due to error: {e}")
                error = f"Ошибка при проверке regex: {e}"
