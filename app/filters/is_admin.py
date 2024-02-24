from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from config import admin_ids


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if isinstance(admin_ids, int):
            return message.from_user.id == admin_ids
        return message.from_user.id in admin_ids


class IsAdminCallback(BaseFilter):
    async def __call__(self, callback_query: CallbackQuery) -> bool:
        if isinstance(admin_ids, int):
            return callback_query.from_user.id == admin_ids
        return callback_query.from_user.id in admin_ids

