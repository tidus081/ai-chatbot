import os
import time
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

from chai_model_api.response import ChaiModelResponse
from utils.logger_util import LoggerUtil

load_dotenv("dev.env")
os.getenv("USER_NAME", "User")


class ChaiModelApiClient:
    def __init__(
        self,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
        bot_name: Optional[str] = None,
        user_name: Optional[str] = None,
        prompt: Optional[str] = None,
    ):
        self.api_url = api_url or os.getenv("API_URL")
        self.api_key = api_key or os.getenv("API_KEY")
        self.bot_name = bot_name or os.getenv("BOT_NAME", "Bot")
        self.user_name = user_name or os.getenv("USER_NAME")
        self.prompt = prompt or os.getenv("PROMPT")
        self.logger = LoggerUtil.get_logger("chai_model_api_client")
        self._validate()

    def _validate(self) -> None:
        missing = []
        if not self.api_url:
            missing.append("API_URL")
        if not self.api_key:
            missing.append("API_KEY")
        if not self.user_name:
            missing.append("USER_NAME")
        if not self.prompt:
            missing.append("PROMPT")
        if missing:
            raise Exception(f"Missing required configuration(s): {', '.join(missing)}")

    def _get_headers_and_payload(
        self, chat_history: List[Dict[str, str]], memory: Optional[str] = ""
    ) -> tuple[dict[str, str], dict[str, object]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "prompt": self.prompt,
            "bot_name": self.bot_name,
            "user_name": self.user_name,
            "chat_history": chat_history,
            "memory": memory if memory is not None else "",  # Deprecated field but required key.
        }
        return headers, payload
    
    def send_chat(
        self, chat_history: List[Dict[str, str]], memory: Optional[str] = ""
    ) -> ChaiModelResponse:
        headers, payload = self._get_headers_and_payload(chat_history, memory)
        max_attempts = 3
        attempt = 0
        while attempt <= max_attempts:
            try:
                response = requests.post(self.api_url, json=payload, headers=headers)
                data = response.json()
                model_output = data.get("model_output", None)
                model_name = data.get("model_name", None)
                return ChaiModelResponse(
                    status_code=response.status_code,
                    model_output=model_output,
                    model_name=model_name,
                )
            except requests.RequestException as e:
                if attempt < max_attempts - 1:
                    delay = 2 ** (attempt + 1)
                    self.logger.warning(
                        f"Request failed (attempt {attempt+1}), retrying in {delay}s: {e}"
                    )
                    time.sleep(delay)
                    attempt += 1
                else:
                    self.logger.error(f"Request failed after {attempt+1} attempts: {e}")
                    break
        # If all attempts fail, or response is malformed, return a default ChaiModelResponse
        return ChaiModelResponse(
            status_code=500,
            model_output=None,
            model_name=None,
        )
