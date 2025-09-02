from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from keyboards.inline_kb import main_kb, medspec_kb, about_kb, petnetrubot_kb, reg_user_kb
from handlers.registration import users_data

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message, command: Command):
    tg_user_id = message.from_user.id
    command_args: str = command.args  # получаем payload после /start

    if command_args:
        if command_args.lower() == "yana":
            await message.answer("Вас пригласила Яна.")

    if tg_user_id in users_data:
        # зарегистрированный пользователь
        full_name = users_data[tg_user_id].get("full_name", "Участник")
        await message.answer(
            f"Рады вас видеть, {full_name}! 👋",
            reply_markup=reg_user_kb(tg_user_id)
        )
    else:
        # новый пользователь
        await message.answer(
            "Вас приветствует бот профессионального сообщества врачей PET.PRO",
            reply_markup=main_kb(tg_user_id)
        )

@start_router.callback_query(F.data == 'main_menu')
async def cmd_main_menu(callback: CallbackQuery):
    await callback.message.answer('Вас приветствует бот профессионального сообщества врачей PET.PRO',
                         reply_markup=main_kb(callback.from_user.id))
    await callback.answer()  # чтобы убрать "часики" на кнопке

@start_router.callback_query(F.data == 'registration')
async def cmd_registration(callback: CallbackQuery):
    await callback.message.answer('Бот предназначен для медицинских специалистов. Вы медицинский специалист?',
                         reply_markup=medspec_kb(callback.from_user.id))
    await callback.answer()  # чтобы убрать "часики" на кнопке

@start_router.callback_query(F.data == 'about')
async def cmd_about(callback: CallbackQuery):
    await callback.message.answer('Бот помогает получить доступ в профессиональное сообщество врачей PET.PRO, посвященное методу диагностики ПЭТ/КТ от сети центров ядерной медицины ПЭТ Технолоджи.',
                                  reply_markup = about_kb(callback.from_user.id))
    await callback.answer()  # чтобы убрать "часики" на кнопке

@start_router.callback_query(F.data == 'is_doctor_no')
async def cmd_about(callback: CallbackQuery):
    await callback.message.answer('Если вы пациент и ищете как обратиться в федеральную сеть клиник ПЭТ-Технолоджи, пожалуйста, напишите ваше обращение 👉 @petnetru_bot',
                                  reply_markup = petnetrubot_kb(callback.from_user.id))
    await callback.answer()  # чтобы убрать "часики" на кнопке