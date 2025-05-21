import random
import pathlib
import logging
_red = "\x1b[31m"

logger = logging.getLogger(__name__)


class ProxyProvider:
    def __init__(self, filepath: str = "assets/proxy.txt"):
        self.filepath = pathlib.Path(filepath)
        self._load()
        if not self.proxies:
            logger.warning(f"{_red}No proxies found in {filepath}. Defaulting to no proxy for requests.{_red}")

    def _load(self):
        with self.filepath.open("r", encoding="utf-8") as f:
            self.proxies = [f"{line.strip()}" for line in f if line.strip() if not line.startswith("#")]

    def get_random(self) -> str | None:
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def reload(self):
        self._load()

    def all(self):
        return list(self.proxies)
