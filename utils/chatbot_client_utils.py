from typing import Any
import logging


def initiate_chat(logger: logging.Logger) -> tuple[str, str]:
    user_name = input("Enter your name: ").strip() or "User"
    start_new = input("Start a new chat? (y/n): ").strip().lower()

    if start_new == "y":
        logger.info(f"Starting a new chat for {user_name}.")
    elif start_new == "n":
        logger.info(f"Loading existing chat for {user_name}.")
    else:
        logger.warning(
            f"Invalid input '{start_new}'. Defaulting to loading existing chat for {user_name}."
        )
        start_new = "n"

    return user_name, start_new

async def receive_full_response(websocket: Any, end_marker: str = "[[END]]") -> str:
    response = ""
    while True:
        message = await websocket.recv()
        if message == end_marker:
            break
        response += message
    return response