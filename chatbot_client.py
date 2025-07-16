import asyncio
import os
import time
import websockets
from dotenv import load_dotenv
from utils.logger_util import LoggerUtil
from utils.chatbot_client_utils import initiate_chat, receive_full_response


load_dotenv("dev.env")
CHATBOT_SERVER_URL = os.getenv("CHATBOT_SERVER_URL", "ws://localhost:8765")


async def chat():
    # Get user inputs
    client_logger = LoggerUtil.get_logger("chatbot_client", for_client=True)
    user_name, start_new = initiate_chat(client_logger)

    async with websockets.connect(
        CHATBOT_SERVER_URL,
        additional_headers={"X-User-Name": user_name, "X-Start-New": start_new},
    ) as websocket:
        client_logger.info(f"Connected to chatbot as {user_name}. Type 'exit' to quit.\n")
        while True:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            user_input = input(f"{current_time} - [{user_name}]: ")
            if user_input.strip().lower() in ("exit", "quit"):
                break
            await websocket.send(user_input)
            bot_response = await receive_full_response(websocket)
            client_logger.info(f"[Bot]: {bot_response}")


if __name__ == "__main__":
    asyncio.run(chat())
