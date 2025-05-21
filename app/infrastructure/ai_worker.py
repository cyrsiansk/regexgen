import g4f.models
from g4f.client import AsyncClient
import logging
from app.infrastructure.proxy_provider import ProxyProvider

logger = logging.getLogger(__name__)


async def retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
    raise RuntimeError("All attempts to call the LLM failed")


class Character:
    def __init__(self, description: str, name: str, proxy_provider: ProxyProvider):
        self.name = name
        self.history = [{"role": "system", "content": description}]
        self.proxy_provider = proxy_provider

    async def ask(self, prompt: str) -> str:
        async def make_request():
            client = AsyncClient()
            proxy = self.proxy_provider.get_random()
            response = client.chat.completions.create(
                model=g4f.models.gpt_4o_mini,
                messages=self.history + [{"role": "user", "content": prompt}],
                web_search=False,
                proxy=proxy,
                stream=True,
                stop=["</python>"]
            )
            full_response = ""
            async for chunk in response:
                delta = chunk.choices[0].delta.content
                if delta:
                    full_response += delta
            return full_response

        result = await retry(make_request)
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": result})
        return result


class CharacterFactory:
    proxy_provider = None

    @staticmethod
    def set_proxy_provider(proxy_provider: ProxyProvider):
        CharacterFactory.proxy_provider = proxy_provider

    @staticmethod
    def create(name: str) -> Character:
        if not CharacterFactory.proxy_provider:
            CharacterFactory.proxy_provider = ProxyProvider()
        with open("assets/prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()
        return Character(system_prompt, name, CharacterFactory.proxy_provider)
