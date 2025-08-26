from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import admins

def main_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text="📖 О нас"), KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="📝 Заполнить анкету"), KeyboardButton(text="📚 Каталог")]
    ]
    if user_telegram_id in admins:
        kb_list.append([KeyboardButton(text="⚙️ Админ панель")])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Надо чтото выбрать:")
    return keyboard

def main_kb2(user_telegram_id: int):
    kb_list = [
        [
            InlineKeyboardButton(text="📖 О нас", callback_data="about"),
            InlineKeyboardButton(text="👤 Профиль", callback_data="profile")
        ],
        [
            InlineKeyboardButton(text="📝 Заполнить анкету", callback_data="fill_form"),
            InlineKeyboardButton(text="📚 Каталог", callback_data="catalog")
        ]
    ]
    if user_telegram_id in admins:
        kb_list.append([
            InlineKeyboardButton(text="⚙️ Админ панель", callback_data="admin_panel")
        ])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard