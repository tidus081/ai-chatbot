
import asyncio
import os
import textwrap
import websockets
from urllib.parse import urlparse
from typing import Any, Optional
from dotenv import load_dotenv

from chai_model_api.client import ChaiModelApiClient
from utils.logger_util import LoggerUtil
from utils.user_rate_limiter_util import UserRateLimiter
from utils.chatbot_server_utils import parse_headers, handle_chat_history


load_dotenv("dev.env")
BOT_NAME = os.getenv("BOT_NAME", "Bot")
CHATBOT_SERVER_URL = os.getenv("CHATBOT_SERVER_URL", "ws://localhost:8765")
PING_INTERVAL = int(os.getenv("PING_INTERVAL", "60"))
PING_TIMEOUT = int(os.getenv("PING_TIMEOUT", "60"))
RATE_LIMIT_MAX_CALLS = int(os.getenv("RATE_LIMIT_MAX_CALLS", 10))  # e.g. 10
RATE_LIMIT_PERIOD = int(
    os.getenv("RATE_LIMIT_PERIOD", 3600)
)  # e.g. 3600 seconds (1 hour)
 # TODO : should be stored in a more robust cache
CHAT_HISTORY = {}  # key: user_name, value: chat history

LOGGER = LoggerUtil.get_logger("chatbot_server")

async def handle_connection(websocket) -> None:
    try:
        # Fetch user_name and start_new_chat from headers
        user_name, start_new_chat = parse_headers(websocket.request.headers, logger)

        # Handle chat history based on header
        handle_chat_history(user_name, start_new_chat, CHAT_HISTORY, logger)

        chai_client = ChaiModelApiClient()
        user_rate_limiter = UserRateLimiter(RATE_LIMIT_MAX_CALLS, RATE_LIMIT_PERIOD)

    except ValueError as e:
        LOGGER.error(f"Error parsing headers: {e}")
        await websocket.close(code=4000, reason=str(e))
        return
    
    try:
        while True:
            user_input = await websocket.recv()
            # Rate limit check
            if not user_rate_limiter.is_allowed(user_name):
                LOGGER.warning(f"Rate limit exceeded for user: {user_name}")
                await websocket.send(
                    f"[Error: Rate limit exceeded. "
                    f"You can send up to {RATE_LIMIT_MAX_CALLS} messages every "
                    f"{RATE_LIMIT_PERIOD // 60} minutes. Please try again later.]"
                )
                await websocket.send("[[END]]")
                continue
            LOGGER.info(f"User input from {user_name}: {user_input}")
            CHAT_HISTORY[user_name].append({"sender": user_name, "message": user_input})
            response = chai_client.send_chat(
                chat_history=CHAT_HISTORY[user_name],
            )

            if response.status_code == 200:
                bot_message = response.model_output
                LOGGER.info(f"Bot response to {user_name}: {bot_message}")
                CHAT_HISTORY[user_name].append(
                    {"sender": BOT_NAME, "message": bot_message}
                )
                for chunk in textwrap.wrap(bot_message, 50):
                    await websocket.send(chunk)
            else:
                await websocket.send("[Error: No response from Chai API]")

            await websocket.send("[[END]]")
    except websockets.exceptions.ConnectionClosed:
        LOGGER.info(f"Client disconnected: {user_name}")

def process_request(path: str, request: Any) -> Optional[tuple[int, list[tuple[str, str]], bytes]]:
    # Header validation: require X-User-Name header
    if "X-User-Name" not in request.headers:
        return (
            400,
            [("Content-Type", "text/plain")],
            b"Missing or empty X-User-Name header.",
        )
    return None

async def main() -> None:
    parsed_url = urlparse(CHATBOT_SERVER_URL)
    async with websockets.serve(
        handle_connection,
        parsed_url.hostname,
        parsed_url.port,
        ping_interval=PING_INTERVAL,
        ping_timeout=PING_TIMEOUT,
        process_request=process_request,
    ):
        LOGGER.info(f"WebSocket server running on {CHATBOT_SERVER_URL}")
        await asyncio.Future()  # Keep server alive


if __name__ == "__main__":
    asyncio.run(main())
