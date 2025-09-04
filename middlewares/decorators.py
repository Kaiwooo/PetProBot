from functools import wraps
from aiogram.types import CallbackQuery

def skip_if_registered(handler):
    """Декоратор: если пользователь уже зарегистрирован — гасим кнопки и выходим"""
    @wraps(handler)
    async def wrapper(callback: CallbackQuery, *args, **kwargs):
        from db_handler.db import is_user_registered  # импорт внутри чтобы избежать циклических импортов
        if await is_user_registered(callback.from_user.id):
            # Убираем кнопки и показываем уведомление
            await callback.message.edit_reply_markup(reply_markup=None)
            await callback.answer("Вы уже зарегистрированы ✅", show_alert=True)
            return
        return await handler(callback, *args, **kwargs)
    return wrapper