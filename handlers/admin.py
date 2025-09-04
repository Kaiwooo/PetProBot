from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline_kb import admin_kb
from db_handler.db import get_pool

admin_router = Router()

@admin_router.callback_query(F.data == 'admin_panel')
async def admin_panel(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Выберите нужный пункт:', reply_markup=admin_kb(callback.from_user.id))
    await callback.answer()

@admin_router.callback_query(F.data == 'admin_agents')
async def admin_agents(callback: CallbackQuery):
    await callback.message.edit_reply_markup()  # убираем кнопки

    # Получаем всех агентов
    async with get_pool().acquire() as conn:
        rows = await conn.fetch("""
            SELECT *
            FROM agents
            ORDER BY created DESC
        """)

    if not rows:
        await callback.message.answer("Нет зарегистрированных агентов.", reply_markup=admin_kb(callback.from_user.id))
        await callback.answer()
        return

    # Отправляем сообщение с количеством
    total_agents = len(rows)
    await callback.message.answer(f"Всего зарегистрировано {total_agents} агентов")

    # Формируем детальный список
    lines = []
    for row in rows:
        created = row['created'].strftime('%Y-%m-%d %H:%M:%S') if row['created'] else 'Не указано'
        full_name = row['full_name'] or 'Не указано'
        phone = row['phone_number'] or 'Не указано'
        username = f"@{row['telegram_username']}" if row['telegram_username'] else 'Не указан'
        city = row['city'] or 'Не указано'
        organization = row['organization'] or 'Не указано'
        position = row['position'] or 'Не указано'

        lines.append(f"{created}; {full_name}; {phone}; {username}; {city}; {organization}; {position}")

    # Отправляем одним сообщением (если много агентов, можно разбить на блоки)
    full_message = "\n".join(lines)
    await callback.message.answer(full_message, reply_markup=admin_kb(callback.from_user.id))
    await callback.answer()  # убираем "часики" на кнопке

@admin_router.callback_query(F.data == 'admin_customers')
async def admin_customers(callback: CallbackQuery):
    await callback.message.edit_reply_markup()  # убираем кнопки

    # Получаем всех пациентов вместе с информацией о врачах
    async with get_pool().acquire() as conn:
        rows = await conn.fetch("""
            SELECT 
                c.full_name AS patient_name,
                c.phone_number AS patient_phone,
                c.created AS patient_created,
                a.telegram_username AS agent_username,
                a.full_name AS agent_full_name
            FROM customers c
            JOIN agents a ON c.agent_id = a.telegram_id
            ORDER BY a.telegram_username, c.created DESC
        """)

    if not rows:
        await callback.message.answer("Нет зарегистрированных пациентов.", reply_markup=admin_kb(callback.from_user.id))
        await callback.answer()
        return

    # Группируем по врачу
    grouped = {}
    for row in rows:
        agent = row['agent_username'] or 'Не указан'
        if agent not in grouped:
            grouped[agent] = []
        grouped[agent].append(row)

    # Формируем сообщения
    for agent, patients in grouped.items():
        lines = [f"Врач: @{agent}"]
        for p in patients:
            created = p['patient_created'].strftime('%Y-%m-%d %H:%M:%S') if p['patient_created'] else 'Не указано'
            lines.append(f"{created}; {p['patient_name']}; {p['patient_phone']}")
        message_text = "\n".join(lines)
        await callback.message.answer(message_text)

    await callback.message.answer('Это список всех пациентов', reply_markup=admin_kb(callback.from_user.id))
    await callback.answer()
