from typing import Any, Dict
from app.logging import get_logger
import httpx
from bs4 import BeautifulSoup


class FetchUrl:
    """
    Busca informações em uma URL.
    """
    
    def __init__(self):
        self.logger = get_logger("fetch_url")
        self.name = "fetch_url"
        self.description = "Busca informações em uma URL"

    async def fetch_url(self, url: str) -> str:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=30.0)
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text()
                return text
            except httpx.TimeoutException:
                return "Timeout error"

    async def execute(self, arguments: Dict[str, Any]) -> str:
        return await self.fetch_url(arguments["url"])