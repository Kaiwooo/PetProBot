from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from keyboards.inline_kb import start_kb, medspec_kb, about_kb, petnetrubot_kb, reg_user_kb
from db_handler.db import get_pool
from create_bot import admins

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id in admins: #если админ
        await message.answer(
            'Пожалуйста выберите нужный пункт в меню',
            reply_markup=start_kb(message.from_user.id, extra = True)
        )
    else:
        async with get_pool().acquire() as conn:
            agent = await conn.fetchrow(
                "SELECT full_name FROM agents WHERE telegram_id=$1", message.from_user.id
            )
        if agent:  # зарегистрированный пользователь
            full_name = agent['full_name']
            await message.answer(f"Рады вас видеть, {full_name}! 👋",
                                 reply_markup=reg_user_kb(message.from_user.id, full_name)
            )
        else: # если новый пользователь
            await message.answer("Вас приветствует бот профессионального сообщества врачей PET.PRO",
                                 reply_markup=start_kb(message.from_user.id)
            )

@start_router.callback_query(F.data == 'main_menu')
async def cmd_main_menu(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.answer()
    if callback.from_user.id in admins: #если админ
        await callback.message.answer(
            'Пожалуйста выберите нужный пункт в меню',
            reply_markup=start_kb(callback.from_user.id, extra = True)
        )
    else:
        async with get_pool().acquire() as conn:
            agent = await conn.fetchrow(
                "SELECT full_name FROM agents WHERE telegram_id=$1", callback.from_user.id
            )
        if agent:  # зарегистрированный пользователь
            await callback.message.edit_reply_markup(
                reply_markup=reg_user_kb(callback.from_user.id, agent['full_name'])
            )
        else: # если новый пользователь
            await callback.message.answer(
                "Вас приветствует бот профессионального сообщества врачей PET.PRO",
                reply_markup=start_kb(callback.from_user.id)
            )

@start_router.callback_query(F.data == 'about')
async def cmd_about(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.answer()
    await callback.message.answer('Бот помогает получить доступ в профессиональное сообщество врачей PET.PRO, посвященное методу диагностики ПЭТ/КТ от сети центров ядерной медицины ПЭТ Технолоджи.',
                                  reply_markup = about_kb(callback.from_user.id))

@start_router.callback_query(F.data.in_(['is_doctor_no', 'is_doctor_yes']))
async def cmd_about(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.answer()
    if callback.data == 'is_doctor_no':
        await callback.message.answer('Если вы пациент и ищете как обратиться в федеральную сеть клиник ПЭТ-Технолоджи, пожалуйста, напишите ваше обращение 👉 @petnetru_bot',
                                      reply_markup = petnetrubot_kb(callback.from_user.id))
    else: #callback.data == 'is_doctor_yes':
        await callback.message.answer('Бот предназначен для медицинских специалистов. Вы хотите зарегистрироваться?',
                                      reply_markup=medspec_kb(callback.from_user.id))