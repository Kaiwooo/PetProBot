import logging
import time
from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Any, Awaitable, Callable, Dict

logger = logging.getLogger("aiogram.event")


class UserLoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        start_time = time.monotonic()

        user_id = None
        event_type = None

        if event.message:
            user_id = event.message.from_user.id
            event_type = "message"
        elif event.callback_query:
            user_id = event.callback_query.from_user.id
            event_type = "callback_query"
        elif event.inline_query:
            user_id = event.inline_query.from_user.id
            event_type = "inline_query"
        elif event.my_chat_member:
            user_id = event.my_chat_member.from_user.id
            event_type = "my_chat_member"
        else:
            event_type = "unknown"

        update_id = event.update_id
        bot_id = data["bot"].id

        result = await handler(event, data)

        duration = (time.monotonic() - start_time) * 1000  # ms
        logger.info(
            f"Update id={update_id} [{event_type}] from user {user_id} is handled. "
            f"Duration {duration:.0f} ms by bot id={bot_id}"
        )

        return result