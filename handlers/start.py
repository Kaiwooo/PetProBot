from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.inline_kb import main_kb, medspec_kb, about_kb, petnetrubot_kb
from create_bot import bot
from handlers.registration import registered_users
from aiogram.types import BotCommand, BotCommandScopeChat

start_router = Router()

# --- Команда /start ---
@start_router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id

    if registered_users.get(user_id):
        # пользователь уже зарегистрирован
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Главное меню"),
                BotCommand(command="make_request", description="Сделать заявку")
            ],
            scope=BotCommandScopeChat(chat_id=user_id)
        )
        await message.answer(
            "Добро пожаловать обратно!",
            reply_markup=main_kb(user_id)
        )
    else:
        # новый пользователь
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Запуск бота"),
                BotCommand(command="registration", description="Зарегистрироваться")
            ],
            scope=BotCommandScopeChat(chat_id=user_id)
        )
        await message.answer(
            "Вас приветствует бот профессионального сообщества врачей PET.PRO\n"
            "Вы медицинский специалист?",
            reply_markup=medspec_kb(user_id)  # inline-кнопки "Да/Нет"
        )

# --- Кнопка регистрации ---
@start_router.callback_query(F.data == 'registration')
async def cmd_registration(callback: CallbackQuery):
    await callback.message.answer(
        'Бот предназначен для медицинских специалистов. Вы медицинский специалист?',
        reply_markup=medspec_kb(callback.from_user.id)
    )
    await callback.answer()

# --- Кнопка о боте ---
@start_router.callback_query(F.data == 'about')
async def cmd_about(callback: CallbackQuery):
    await callback.message.answer(
        'Бот помогает получить доступ в профессиональное сообщество врачей PET.PRO, '
        'посвященное методу диагностики ПЭТ/КТ от сети центров ядерной медицины ПЭТ Технолоджи.',
        reply_markup=about_kb(callback.from_user.id)
    )
    await callback.answer()

# --- Кнопка если не доктор ---
@start_router.callback_query(F.data == 'is_doctor_no')
async def cmd_not_doctor(callback: CallbackQuery):
    await callback.message.answer(
        'Если вы пациент и ищете как обратиться в федеральную сеть клиник ПЭТ-Технолоджи, '
        'пожалуйста, напишите ваше обращение 👉 @petnetru_bot',
        reply_markup=petnetrubot_kb(callback.from_user.id)
    )
    await callback.answer()
