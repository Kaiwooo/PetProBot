import logging
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.inline_kb import start_kb

logger = logging.getLogger(__name__)
special_start_router = Router()

SPECIAL_USER_ID = {
    6705162267: {
        "name": "Арина",
        "animation": "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",
        "caption": "Уважаемая Ариночка Вадимовна! Вас приветствует бот PET.PRO"
    },
    910252: {
        "name": "Петр",
        "animation": "https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif",
        "caption": "Уважаемый Петруша Валерьевич! Вас приветствует бот PET.PRO"
    },
    504217195: {
        "name": "Яна",
        "animation": "https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif",
        "caption": "Уважаемая Яна Владимировна! Вас приветствует PET.PRO бот =)"
    }
}

@special_start_router.message(CommandStart())
async def special_start(message: Message):
    user_id = message.from_user.id
    vip_data = SPECIAL_USER_ID.get(user_id)

    if vip_data:
        try:
            await message.answer_animation(
                animation=vip_data["animation"],
                caption=vip_data["caption"],
                reply_markup=start_kb(message.from_user.id)
            )
        except:
            await message.answer_photo(
                photo="https://placekitten.com/800/600",
                caption=vip_data["caption"]
            )
        return