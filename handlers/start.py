from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from keyboards.inline_kb import start_kb, medspec_kb, about_kb, petnetrubot_kb, reg_user_kb, admin_kb, verified_user_kb
from handlers.registration import users_data
from create_bot import admins

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message, command: Command):
    command_args: str = command.args  # получаем payload после /start
    if command_args:
        if command_args.lower() == "yana":
            await message.answer("Вас пригласила Яна.")

    if message.from_user.id in users_data: #если уже зарегистрированный пользователь
        full_name = users_data[message.from_user.id].get("full_name")
        await message.answer(
            f"Рады вас видеть, {full_name}! 👋",
            reply_markup=reg_user_kb(message.from_user.id)
        )
    elif message.from_user.id in admins: #если админ
        await message.answer(
            'Пожалуйста выберите нужный пункт в меню',
            reply_markup=admin_kb(message.from_user.id)
        )
    # elif message.from_user.id in users_data2: #если админ
    #     await message.answer(
    #         'Пожалуйста выберите нужный пункт в меню',
    #         reply_markup=verified_user_kb(message.from_user.id)
    #     )
    else: # если новый пользователь
        await message.answer(
            "Вас приветствует бот профессионального сообщества врачей PET.PRO",
            reply_markup=start_kb(message.from_user.id)
        )

@start_router.callback_query(F.data == 'main_menu')
async def cmd_main_menu(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    if callback.from_user.id in users_data: #если уже зарегистрированный пользователь
        full_name = users_data[callback.from_user.id].get("full_name")
        await callback.message.answer(
            f"Рады вас видеть, {full_name}! 👋",
            reply_markup=reg_user_kb(callback.from_user.id)
        )
    elif callback.from_user.id in admins: #если админ
        await callback.message.answer(
            'Пожалуйста выберите нужный пункт в меню',
            reply_markup=admin_kb(callback.from_user.id)
        )
    # elif message.from_user.id in users_data2: #если админ
    #     await message.answer(
    #         'Пожалуйста выберите нужный пункт в меню',
    #         reply_markup=verified_user_kb(message.from_user.id)
    #     )
    else: # если новый пользователь
        await callback.message.answer(
            "Вас приветствует бот профессионального сообщества врачей PET.PRO",
            reply_markup=start_kb(callback.from_user.id)
        )
    await callback.answer()  # чтобы убрать "часики" на кнопке

@start_router.callback_query(F.data == 'about')
async def cmd_about(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Бот помогает получить доступ в профессиональное сообщество врачей PET.PRO, посвященное методу диагностики ПЭТ/КТ от сети центров ядерной медицины ПЭТ Технолоджи.',
                                  reply_markup = about_kb(callback.from_user.id))
    await callback.answer()

@start_router.callback_query(F.data.in_(['is_doctor_no', 'is_doctor_yes']))
async def cmd_about(callback: CallbackQuery):
    if callback.data == 'is_doctor_no':
        await callback.message.edit_reply_markup()
        await callback.message.answer('Если вы пациент и ищете как обратиться в федеральную сеть клиник ПЭТ-Технолоджи, пожалуйста, напишите ваше обращение 👉 @petnetru_bot',
                                      reply_markup = petnetrubot_kb(callback.from_user.id))
    elif callback.data == 'is_doctor_yes':
        await callback.message.edit_reply_markup()
        await callback.message.answer('Бот предназначен для медицинских специалистов. Вы хотите зарегистрироваться?',
                                      reply_markup=medspec_kb(callback.from_user.id))
    else:
        return
    await callback.answer()