from typing import Any, Dict
from app.logging import get_logger
from app.settings import VariablesMCPPython
import httpx
import json


class SearchWeb:
    """
    Busca informações na web.
    """
    
    def __init__(self):
        self.logger = get_logger("search_web")
        self.name = "search_web"
        self.description = "Busca informações na web"

    async def search_web(self, query: str) -> dict | None:
        payload = json.dumps({"q": query, "num": 2})

        headers = {
            "X-API-KEY": VariablesMCPPython.serper_api_key,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    VariablesMCPPython.serper_url, headers=headers, data=payload, timeout=30.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.TimeoutException:
                return {"organic": []}

    async def execute(self, arguments: Dict[str, Any]) -> str:
        return await self.search_web(arguments["query"])