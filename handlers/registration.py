from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.inline_kb import reg_user_kb, confirm_reg_kb, privacy_kb
from keyboards.regular_kb import phone_kb
from datetime import datetime
from db_handler.postgres import get_pool
from middlewares.decorators import skip_if_registered
import re

registration_router = Router()

# ------------------- FSM -------------------
class RegistrationAgent(StatesGroup):
    privacy = State()
    # marketing = State()
    phone = State()
    full_name = State()
    city = State()
    confirmation = State()

@registration_router.callback_query(F.data == 'registration')
async def start_registration_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.answer() # убираем часики на кнопке
    await state.update_data(telegram_username=callback.from_user.username)
    await state.update_data(started=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    await callback.message.answer('Для регистрации, нам потребуются Ваши согласия')
    await callback.message.answer(
        'Я принимаю <a href="https://www.pet-net.ru/page/soglasie-na-obrabotku-agenty">Соглашение об обработке Персональных Данных</a>',
        reply_markup=privacy_kb(callback.from_user.id)
    )
    await state.set_state(RegistrationAgent.privacy)

# ------------------- Получение согласия ПД -------------------
@registration_router.callback_query(F.data.in_(['privacy_agreement_yes', 'privacy_agreement_no']))
async def process_privacy(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'privacy_agreement_yes':
        await state.update_data(privacy=True)
        await callback.message.edit_reply_markup()  # убираем кнопки
        await callback.answer('✅ Согласие на ПД получено')  # маленькое уведомление
        await callback.message.answer(
            'Благодарим вас за принятие соглашения, а теперь укажите Ваш номер телефона, нажав на кнопку "Поделиться контактом"',
            reply_markup=phone_kb()
        )
        await state.set_state(RegistrationAgent.phone)
        await callback.answer()
    else:
        await state.update_data(privacy=False)
        await callback.answer('Без принятия Согласия на обработку Персональных Данных регистрация невозможна', show_alert=True)
        await state.clear()

# # ------------------- Получение согласия Маркетинг-------------------
# @registration_router.callback_query(F.data.in_(['marketing_agreement_yes', 'marketing_agreement_no']))
# async def process_marketing(callback: CallbackQuery, state: FSMContext):
#     if callback.data == 'marketing_agreement_yes':
#         await state.update_data(marketing=True)
#         await callback.message.edit_reply_markup()  # убираем кнопки
#         await callback.answer('✅ Согласие на маркетинг получено')  # toast
#         await callback.message.answer(
#             'Благодарим вас за принятие соглашений, а теперь укажите Ваш номер телефона',
#             reply_markup=phone_kb()
#         )
#         await state.set_state(RegistrationAgent.phone)
#         await callback.answer()
#     else:
#         await state.update_data(privacy=False)
#         await callback.answer('К сожалению, регистрация без возможности отправлять Вам сообщения невозможна', show_alert=True)
#         await state.clear()

@registration_router.message(F.contact, RegistrationAgent.phone)
async def process_phone(message: Message, state: FSMContext):
    if message.contact.user_id != message.from_user.id:
        await message.answer('Пожалуйста, поделитесь вашим собственным контактом!')
        return
    await state.update_data(phone=message.contact.phone_number)
    await message.answer('Спасибо! А теперь введи ваше ФИО:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationAgent.full_name)

@registration_router.message(RegistrationAgent.full_name)
async def process_full_name(message: Message, state: FSMContext):
    text = message.text.strip()

    # Проверка на недопустимые символы (только буквы и дефис)
    if not re.fullmatch(r"[A-Za-zА-Яа-яЁё\- ]+", text):
        await message.answer("ФИО может содержать только буквы и дефис. Пожалуйста, введите корректное ФИО.")
        return

    # Разбиваем ФИО
    fio_parts = text.split()
    last_name = fio_parts[0] if len(fio_parts) > 0 else None
    first_name = fio_parts[1] if len(fio_parts) > 1 else None
    patronymic = fio_parts[2] if len(fio_parts) > 2 else None

    # Проверка, что все части введены
    if not last_name or not first_name or not patronymic:
        await message.answer("Пожалуйста, введите полностью ФИО: фамилия, имя, отчество.")
        return

    # Проверка на использование одного алфавита (кириллица или латиница)
    if any(re.search(r'[А-Яа-яЁё]', part) for part in fio_parts) and any(
            re.search(r'[A-Za-z]', part) for part in fio_parts):
        await message.answer("ФИО должно быть полностью на кириллице или полностью на латинице, без смешения.")
        return

    # Нормализация: первая буква заглавная, остальные строчные
    last_name = last_name.capitalize()
    first_name = first_name.capitalize()
    patronymic = patronymic.capitalize()
    normalized_fio = f"{last_name} {first_name} {patronymic}"

    # Сохраняем
    await state.update_data(full_name=normalized_fio)

    data = await state.get_data()
    if data.get('edit_field') == 'full_name':
        await state.update_data(edit_field=None)
        await show_confirmation(message, state)
        return
    await message.answer('Укажите город, в котором Вы работаете:')
    await state.set_state(RegistrationAgent.city)

@registration_router.message(RegistrationAgent.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()
    if data.get('edit_field') == 'city':
        await state.update_data(edit_field=None)
        await show_confirmation(message, state)
        return
    await show_confirmation(message, state)

# ------------------- Показываем подтверждение -------------------
async def show_confirmation(obj: Message | CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(RegistrationAgent.confirmation)

    # Разбиваем ФИО на фамилию, имя, отчество
    fio_parts = data.get("full_name", "").split()
    last_name = fio_parts[0] if len(fio_parts) > 0 else "не указано"
    first_name = fio_parts[1] if len(fio_parts) > 1 else "не указано"
    patronymic = fio_parts[2] if len(fio_parts) > 2 else "не указано"

    summary_lines = (
        f"Пожалуйста внимательно проверьте введённые данные.\n"
        f"Вы не сможете изменить их самостоятельно без медицинского представителя:\n\n"
        f"Телефон: {data['phone']}\n"
        f"Фамилия: {last_name}",
        f"Имя: {first_name}",
        f"Отчество: {patronymic}",
        f"Город: {data['city']}\n"
    )
    summary = "\n".join(summary_lines)

    keyboard = confirm_reg_kb(obj.from_user.id)
    if isinstance(obj, CallbackQuery):
        await obj.message.edit_text(summary, reply_markup=keyboard)
        await obj.answer()
    else:
        await obj.answer(summary, reply_markup=keyboard)

# ------------------- Обработчики кнопок "Исправить ..." -------------------
@registration_router.callback_query(F.data == 'edit_full_name', RegistrationAgent.confirmation)
@skip_if_registered
async def edit_full_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='full_name')
    try:    # попробуем отредактировать предыдущее (подтверждающее) сообщение бота
        await callback.message.edit_text("Введите корректное ФИО:", reply_markup=None)
    except Exception:   # если редактирование не удалось (например, сообщение нельзя редактировать), упадём обратно к отправке нового сообщения, но это редкий случай
        await callback.message.answer("Введите корректное ФИО:")
    await state.set_state(RegistrationAgent.full_name)
    await callback.answer()

@registration_router.callback_query(F.data == 'edit_city', RegistrationAgent.confirmation)
@skip_if_registered
async def edit_city(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='city')
    try:
        await callback.message.edit_text('Введите корректный город:', reply_markup=None)
    except Exception:
        await callback.message.answer('Введите корректный город:')
    await state.set_state(RegistrationAgent.city)
    await callback.answer()

# ------------------- Подтверждение регистрации -------------------
@registration_router.callback_query(F.data == 'confirm_registration')
@skip_if_registered
async def confirm_registration(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    username = data.get("telegram_username") or None  # Telegram username или None если нет
    reg_date = datetime.now()   # Дата регистрации
    full_name = data.get('full_name', '')
    phone = data.get('phone', None)
    city = data.get('city', None)
    privacy = data.get('privacy', False)
    requested_contract = data.get('requested_contract', False)
    # marketing = data.get('marketing', False)

    # Сохраняем в Postgres
    async with get_pool().acquire() as conn:
        await conn.execute(
            """
            INSERT INTO agents(
                telegram_id,
                telegram_username,
                full_name,
                phone_number,
                city,
                created,
                privacy
            ) VALUES ($1,$2,$3,$4,$5,$6,$7)
            ON CONFLICT (telegram_id) DO UPDATE SET
                telegram_username = EXCLUDED.telegram_username,
                full_name = EXCLUDED.full_name,
                phone_number = EXCLUDED.phone_number,
                city = EXCLUDED.city,
                created = EXCLUDED.created,
                privacy = EXCLUDED.privacy
            """,
            callback.from_user.id,
            username,
            full_name,
            phone,
            city,
            reg_date,
            privacy,
            # marketing
        )

    await callback.message.edit_text(
        f"Уважаемый {data['full_name']}, спасибо за регистрацию!\n",
        reply_markup=reg_user_kb(callback.from_user.id, full_name, requested_contract),
    )
    await state.clear() # очищаем FSM

