from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.inline_kb import reg_user_kb, confirm_patient_kb
from datetime import datetime
from db_handler.postgres import db, add_customer
from services.bitrix import create_deal_patient
from utils.split_full_name import split_full_name
import re

account_router = Router()

class PatientFromAgent(StatesGroup):
    full_name = State()
    phone_number = State()
    confirmation = State()

#--------------------------- Запись пациента -----------------------------
@account_router.callback_query(F.data == 'send_patient')
async def account_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Нам потребуется ФИО вашего пациента.')
    await state.set_state(PatientFromAgent.full_name)
    await callback.answer()

@account_router.message(PatientFromAgent.full_name)
async def patient_full_name(message: Message, state: FSMContext):
    text = message.text.strip()
    last_name, first_name, second_name = split_full_name(text)
    # Проверка: ФИО должно быть либо полностью на кириллице, либо полностью на латинице, только буквы и дефис
    if not (re.fullmatch(r"[А-Яа-яЁё\- ]+", text) or re.fullmatch(r"[A-Za-z\- ]+", text)):
        await message.answer("ФИО может содержать только буквы и дефис, и должно быть полностью на кириллице или полностью на латинице.")
        return
    # Проверка, что все части введены
    if not last_name or not first_name:
        await message.answer("Пожалуйста, введите ФИО: минимум фамилия и имя.")
        return

    normalized_fio = f"{last_name} {first_name} {second_name}".strip()
    await state.update_data(full_name=normalized_fio)

    data = await state.get_data()
    if data.get('edit_field') == 'full_name':
        await state.update_data(edit_field=None)
        await confirmation(message, state)
        return
    await message.answer('Укажите контактный номер пациента:')
    await state.set_state(PatientFromAgent.phone_number)

@account_router.message(PatientFromAgent.phone_number)
async def patient_full_name(message: Message, state: FSMContext):
    phone = message.text.strip()
    # Проверка: + и 10–15 цифр
    phone_pattern = re.compile(r"^\+\d{10,15}$")
    if not phone_pattern.match(phone):
        await message.answer(
            "❌ Неверный формат номера телефона.\n"
            "Введите номер в международном формате (от 10 до 15 цифр), например: +71234567890"
        )
        return
    await state.update_data(phone_number=phone)
    data = await state.get_data()
    if data.get('edit_field') == 'phone_number':
        await state.update_data(edit_field=None)
        await confirmation(message, state)
        return
    await confirmation(message, state)

#----------------------- Показываем подтверждение ------------------------

async def confirmation(obj: Message | CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(PatientFromAgent.confirmation)
    last_name, first_name, second_name = split_full_name(data.get('full_name'))
    summary = "\n".join([
        f"Проверьте введённые данные:\n\n"
        f"Фамилия: {last_name}",
        f"Имя: {first_name}",
        f"Отчество: {second_name}",
        f"Телефон: {data['phone_number']}\n"
    ])
    keyboard = confirm_patient_kb(obj.from_user.id)
    if isinstance(obj, CallbackQuery):
        await obj.message.edit_text(summary, reply_markup=keyboard)
        await obj.answer()
    else:
        await obj.answer(summary, reply_markup=keyboard)

#----------------------- Обработчики правок ------------------------

@account_router.callback_query(F.data == 'edit_patient_full_name', PatientFromAgent.confirmation)
async def edit_full_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='full_name')
    try:    # попробуем отредактировать предыдущее (подтверждающее) сообщение бота
        await callback.message.edit_text("Введите корректное ФИО:", reply_markup=None)
    except Exception:   # если редактирование не удалось (например, сообщение нельзя редактировать), упадём обратно к отправке нового сообщения, но это редкий случай
        await callback.message.answer("Введите корректное ФИО:")
    await state.set_state(PatientFromAgent.full_name)
    await callback.answer()

@account_router.callback_query(F.data == 'edit_patient_phone_number', PatientFromAgent.confirmation)
async def edit_full_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='phone_number')
    try:    # попробуем отредактировать предыдущее (подтверждающее) сообщение бота
        await callback.message.edit_text("Введите корректный номер телефона:", reply_markup=None)
    except Exception:   # если редактирование не удалось (например, сообщение нельзя редактировать), упадём обратно к отправке нового сообщения, но это редкий случай
        await callback.message.answer("Введите корректный номер телефона:")
    await state.set_state(PatientFromAgent.phone_number)
    await callback.answer()

#----------------------- Подтверждение записи ------------------------

@account_router.callback_query(F.data == 'confirm_patient')
async def confirm_request(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    agent_id = callback.from_user.id
    full_name = data.get('full_name')
    phone_number = data.get('phone_number')
    created = datetime.now()
    contact_id = await db.fetchval("SELECT bitrix_contact_id FROM agents WHERE telegram_id = $1", agent_id)
    deal_id = await create_deal_patient(full_name, phone_number, contact_id)

    await add_customer(
        agent_id=agent_id,
        full_name=full_name,
        phone_number=phone_number,
        created=created,
        deal_id=deal_id
    )
    requested_contract = await db.fetchval(
        "SELECT requested_contract FROM agents WHERE telegram_id=$1",
        agent_id
    )
    await callback.message.edit_text(
        f"Мы приняли ваш запрос на запись {full_name}",
        reply_markup=reg_user_kb(agent_id, full_name, requested_contract)
    )
    await state.clear() # очищаем FSM

@account_router.callback_query(F.data == 'main_menu', PatientFromAgent.confirmation)
async def cancel_request(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    # Удаляем сообщение с подтверждением (если оно ещё доступно)
    await callback.message.edit_text(
        f'Отменили запрос на запись',
        reply_markup=reg_user_kb(callback.from_user.id, True, None)  # сюда твое меню
    )
    await callback.answer()