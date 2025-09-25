from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State

send_message_router = Router()

class MessageToUser(StatesGroup):
    id = State()
    message = State()

# 1. Админ нажимает кнопку
@send_message_router.callback_query(F.data == "admin_send_message")
async def get_id(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer("Введите ID пользователя, которому хотите отправить сообщение:")
    await state.set_state(MessageToUser.id)
    await callback.answer()

# 2. Админ вводит ID
@send_message_router.message(MessageToUser.id)
async def save_id(message: Message, state: FSMContext):
    await state.update_data(user_id=message.text)
    await message.answer("Теперь напишите текст сообщения:")
    await state.set_state(MessageToUser.message)

# 3. Админ вводит сообщение, и оно отправляется
@send_message_router.message(MessageToUser.message)
async def send_message(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id = int(data["user_id"])  # ID, введённый админом
    text = message.text

    try:
        await bot.send_message(chat_id=user_id, text=text)
        await message.answer(f"✅ Сообщение отправлено пользователю {user_id}")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка при отправке: {e}")

    await state.clear()