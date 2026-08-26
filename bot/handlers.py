from aiogram import Router, Command
from aiogram.types import Message
from database.db import DatabaseManager

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, db: DatabaseManager):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    
    if not user:
        await db.upsert_user(user_id, is_active=True)
        await message.answer("🎉 Bem-vindo! Trial ativado.")
    else:
        await message.answer("🤖 Bot ativado e aguardando novos sinais...")

@router.message(Command("status"))
async def cmd_status(message: Message):
    await message.answer("🟢 Sistema operando normalmente na Square Cloud.")