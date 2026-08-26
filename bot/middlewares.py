from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any

class LicenseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Any],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        db = data.get("db")
        
        if event.text and event.text.startswith("/start"):
            return await handler(event, data)

        user = await db.get_user(user_id)
        if not user or not user.get("is_active"):
            await event.answer("❌ Acesso negado. Licenca invalida.")
            return

        return await handler(event, data)