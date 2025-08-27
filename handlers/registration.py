from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.regular_kb import phone_kb
from keyboards.inline_kb import main_kb
from create_bot import bot
from aiogram.types import BotCommand, BotCommandScopeChat

registration_router = Router()

# ------------------- FSM -------------------
class Registration(StatesGroup):
    phone = State()
    full_name = State()
    email = State()
    city = State()
    clinic = State()
    position = State()

# ------------------- Временное хранение зарегистрированных -------------------
registered_users = {}  # key: telegram_id, value: True

# --- Старт регистрации через callback ---
@registration_router.callback_query(F.data == "is_doctor_yes")
async def start_registration_callback(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if registered_users.get(user_id):
        await callback.message.answer(
            "Вы уже зарегистрированы!",
            reply_markup=main_kb(user_id)
        )
        await callback.answer()
        return

    await callback.message.answer(
        "Пожалуйста, поделитесь вашим номером телефона:",
        reply_markup=phone_kb()
    )
    await state.set_state(Registration.phone)
    await callback.answer()

# --- FSM шаги ---
@registration_router.message(F.contact)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer("Введите ваше ФИО:")
    await state.set_state(Registration.full_name)

@registration_router.message(Registration.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Введите ваш Email:")
    await state.set_state(Registration.email)

@registration_router.message(Registration.email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите город:")
    await state.set_state(Registration.city)

@registration_router.message(Registration.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Введите медицинское учреждение:")
    await state.set_state(Registration.clinic)

@registration_router.message(Registration.clinic)
async def process_clinic(message: Message, state: FSMContext):
    await state.update_data(clinic=message.text)
    await message.answer("Введите должность / специализацию:")
    await state.set_state(Registration.position)

@registration_router.message(Registration.position)
async def process_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    data = await state.get_data()
    user_id = message.from_user.id

    # помечаем пользователя как зарегистрированного
    registered_users[user_id] = True

    # обновляем команды для зарегистрированного пользователя
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Главное меню"),
            BotCommand(command="make_request", description="Сделать заявку")
        ],
        scope=BotCommandScopeChat(chat_id=user_id)
    )

    await message.answer(
        f"Регистрация завершена!\n\n"
        f"Телефон: {data.get('phone', '-')}\n"
        f"ФИО: {data.get('full_name', '-')}\n"
        f"Email: {data.get('email', '-')}\n"
        f"Город: {data.get('city', '-')}\n"
        f"Медицинское учреждение: {data.get('clinic', '-')}\n"
        f"Должность: {data.get('position', '-')}",
        reply_markup=main_kb(user_id)
    )
    await state.clear()
