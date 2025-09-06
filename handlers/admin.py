from aiogram import Router, F
from aiogram.types import CallbackQuery
from middlewares.redis_registrations import FSMStateInspector
from keyboards.inline_kb import admin_kb
from db_handler.postgres import get_pool
import redis.asyncio
from decouple import config

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
                a.telegram_id AS agent_id,
                a.telegram_username AS agent_username,
                a.full_name AS agent_full_name
            FROM customers c
            JOIN agents a ON c.agent_id = a.telegram_id
            ORDER BY a.telegram_id, c.created DESC
        """)

    if not rows:
        await callback.message.answer("Нет зарегистрированных пациентов.", reply_markup=admin_kb(callback.from_user.id))
        await callback.answer()
        return

    # Группируем по врачу
    grouped = {}
    for row in rows:
        agent_id = row['agent_id']
        if agent_id not in grouped:
            grouped[agent_id] = {
                "full_name": row['agent_full_name'] or 'Не указано',
                "username": row['agent_username'] or 'Не указан',
                "patients": []
            }
        grouped[agent_id]["patients"].append(row)

    # Формируем сообщения
    for agent_info in grouped.values():
        lines = [f"Врач: {agent_info['full_name']} (@{agent_info['username']})"]
        for p in agent_info["patients"]:
            created = p['patient_created'].strftime('%Y-%m-%d %H:%M:%S') if p['patient_created'] else 'Не указано'
            lines.append(f"{created}; {p['patient_name']}; {p['patient_phone']}")
        message_text = "\n".join(lines)
        await callback.message.answer(message_text)
    await callback.message.answer('Это список всех пациентов', reply_markup=admin_kb(callback.from_user.id))
    await callback.answer()

@admin_router.callback_query(F.data == "admin_incomplete_agents")
async def show_incomplete_agents(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    inspector = FSMStateInspector(redis.Redis.from_url(config("REDIS_LINK"), decode_responses=True))
    registration_states = inspector.get_states_by_pattern("Registration")
    if not registration_states:
        await callback.message.answer(
            "Нет пользователей с незавершённой регистрацией.",
            reply_markup=admin_kb(callback.from_user.id),
        )
        await callback.answer()
        return
    lines = []
    total = len(registration_states)
    await callback.message.answer("Пользователей с незавершённой регистрацией: "+ str(total))
    for key, state_value in registration_states.items():
        user_data = inspector.get_user_data(key)
        if user_data.get("started"):
            lines.append(f"Регистрация начата: {user_data['started']}")
        if user_data.get("telegram_username"):
            lines.append(f"TG_Username: @{user_data['telegram_username']}")
        if user_data.get("phone"):
            lines.append(f"Телефон: {user_data['phone']}")
        if user_data.get("full_name"):
            lines.append(f"ФИО: {user_data['full_name']}")
        if user_data.get("city"):
            lines.append(f"Город: {user_data['city']}")
        if user_data.get("clinic"):
            lines.append(f"Учреждение: {user_data['clinic']}")
        if user_data.get("position"):
            lines.append(f"Должность: {user_data['position']}")
        lines.append(f"{'-'*50}")
    # режем длинные ответы по 3500 символов
    batch = ""
    for line in lines:
        if len(batch) + len(line) > 3500:
            await callback.message.answer(batch)
            batch = ""
        batch += line + "\n"
    if batch:
        await callback.message.answer(batch, reply_markup=admin_kb(callback.from_user.id))
    await callback.answer()