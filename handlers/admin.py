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

    total_agents = len(users_data)
    await callback.message.answer(f"Всего зарегистрировано {total_agents} агентов:\n\n")

    message_lines = []
    for user_id, data in users_data.items():
        reg_date = data.get('reg_date', 'Неизвестно')
        full_name = data.get('full_name', 'Не указано')
        phone = data.get('phone', 'Не указано')
        username = f"@{data['username']}" if data.get('username') else 'Не указан'
        city = data.get('city', 'Не указано')
        clinic = data.get('clinic', 'Не указано')
        position = data.get('position', 'Не указано')

        message_lines.append(
            f"{reg_date}; {full_name}; {phone}; {username}; {city}; {clinic}; {position}"
        )

    full_message = "\n".join(message_lines)
    await callback.message.answer(full_message, reply_markup=admin_kb(callback.from_user.id))
    await callback.answer()  # убираем "часики" на кнопке

@admin_router.callback_query(F.data == 'admin_customers')
async def admin_customers(callback: CallbackQuery):
    await callback.message.edit_reply_markup()  # убираем кнопки

    if not patient_data:
        await callback.message.answer("Нет заявок пациентов.", reply_markup=admin_kb(callback.from_user.id))
        await callback.answer()
        return

    for doctor_id, patients in patient_data.items():
        doctor_user = users_data.get(doctor_id)
        doctor_name = doctor_user.get("full_name", "Неизвестно")
        doctor_username = doctor_user.get("username", "Нет username")
        header = f"От врача: {doctor_name} (@{doctor_username})"
        patient_lines = []
        for patient in patients:
            line = f"Дата: {patient['created_at']}; ФИО: {patient['full_name']}; Телефон: {patient['phone_number']}"
            patient_lines.append(line)
        message_text = header + "\n" + "\n".join(patient_lines)
        await callback.message.answer(message_text)

    await callback.message.answer('Это список всех пациентов', reply_markup=admin_kb(callback.from_user.id))
    await callback.answer()
