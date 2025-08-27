from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from keyboards.inline_kb import main_kb, medspec_kb, about_kb, petnetrubot_kb

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Вас приветствует бот профессионального сообщества врачей PET.PRO',
                         reply_markup=main_kb(message.from_user.id))

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


#@start_router.message(Command('docs'))
#async def cmd_start_2(message: Message):
#    await message.answer('Запуск сообщения по команде /start_2 используя фильтр Command()',
#                         reply_markup=main_kb2(message.from_user.id))

#@start_router.message(F.text == '/register')
#async def cmd_start_3(message: Message):
#    await message.answer('Бот предназначен для медицинских специалистов. Вы медицинский специалист?',
#                         reply_markup=medspec_kb(message.from_user.id))

