from typing import Dict, Tuple
import logging


def parse_headers(headers: Dict[str, str], logger: logging.Logger) -> Tuple[str, bool]:
    user_name = headers.get("X-User-Name", None)
    if user_name is None:
        raise ValueError("Missing required X-User-Name header.")
    start_new_chat = (
        headers.get("X-Start-New-Chat", "n").lower() == "y"
    )
    logger.info(
        f"Client connected. User name from header: {user_name}. Start new chat: {start_new_chat}"
    )
    return user_name, start_new_chat

def handle_chat_history(
    user_name: str,
    start_new_chat: bool,
    chat_history: Dict[str, list[Dict[str, str]]],
    logger: logging.Logger
) -> None:
    if start_new_chat or user_name not in chat_history:
        chat_history[user_name] = []
        logger.info(f"Starting new chat for user: {user_name}")
    else:
        logger.info(f"Found existing chat history for user: {user_name}")