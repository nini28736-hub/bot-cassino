from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from typing import Callable, Dict, Any

class LicenseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user: User = data.get("event_from_user")
        db = data.get("db")

        if not user:
            return await handler(event, data)

        text = getattr(event, "text", "") or ""
        if text.startswith("/start"):
            return await handler(event, data)

        user_data = await db.get_user(user.id)
        if not user_data or not user_data.get("is_active"):
            if hasattr(event, "answer"):
                await event.answer("❌ Acesso negado. Licenca invalida.")
            return

        return await handler(event, data)
