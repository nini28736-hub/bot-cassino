import asyncio
from tinydb import TinyDB, Query
from typing import Optional, Dict, Any

class DatabaseManager:
    def __init__(self, db_path: str = "database.json"):
        self.db = TinyDB(db_path)
        self.users = self.db.table("users")
        self.query = Query()
        self._lock = asyncio.Lock()

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        async with self._lock:
            result = self.users.search(self.query.user_id == user_id)
            return result[0] if result else None

    async def upsert_user(self, user_id: int, is_active: bool = True) -> None:
        async with self._lock:
            self.users.upsert(
                {"user_id": user_id, "is_active": is_active},
                self.query.user_id == user_id
            )