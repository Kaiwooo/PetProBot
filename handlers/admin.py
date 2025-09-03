from aiogram import Router, F
from aiogram.types import CallbackQuery
from db_handler.user_storage import users_data, patient_data
from keyboards.inline_kb import admin_kb

admin_router = Router()

@admin_router.callback_query(F.data == 'admin_panel')
async def admin_panel(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Выберите нужный пункт:', reply_markup=admin_kb(callback.from_user.id))
    await callback.answer()

@admin_router.callback_query(F.data == 'admin_agents')
async def admin_agents(callback: CallbackQuery):
    await callback.message.edit_reply_markup()  # убираем кнопки

    if not users_data:
        await callback.message.answer("Нет зарегистрированных пользователей.", reply_markup=admin_kb(callback.from_user.id))
        await callback.answer()
        return

    for user_id, data in users_data.items():
        # Преобразуем словарь в строку "ключ: значение;"
        info = "; ".join(f"{key}: {value}" for key, value in data.items())
        await callback.message.answer(f"ID {user_id} — {info}", reply_markup=admin_kb(callback.from_user.id))

    await callback.answer()  # убираем "часики" на кнопке

@admin_router.callback_query(F.data == 'admin_customers')
async def admin_customers(callback: CallbackQuery):
    await callback.message.edit_reply_markup()  # убираем кнопки

    if not patient_data:
        await callback.message.answer("Нет заявок пациентов.", reply_markup=admin_kb(callback.from_user.id))
        await callback.answer()
        return

    for user_id, data in patient_data.items():
        info = "; ".join(f"{key}: {value}" for key, value in data.items())
        await callback.message.answer(f"ID {user_id} — {info}", reply_markup=admin_kb(callback.from_user.id))

    await callback.answer()
