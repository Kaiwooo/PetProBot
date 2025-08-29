from create_bot import admins
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_kb(user_telegram_id: int):
    if user_telegram_id in admins:
        kb_list = [[InlineKeyboardButton(text="⚙️ Админ панель", callback_data="admin_panel")]]
    else:
        kb_list = [
            [InlineKeyboardButton(text="📖 О нас", callback_data="about"),
            InlineKeyboardButton(text="👤 Зарегистрироваться", callback_data="registration")]
    ]
        #kb_list.append([InlineKeyboardButton(text="⚙️ Админ панель", callback_data="admin_panel")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def medspec_kb(user_telegram_id: int):
    kb_list = [
        [InlineKeyboardButton(text="✅ Да", callback_data="is_doctor_yes"),
        InlineKeyboardButton(text="❌ Нет", callback_data="is_doctor_no")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def about_kb(user_telegram_id: int):
    kb_list = [
        [InlineKeyboardButton(text="👤 Зарегистрироваться", callback_data="registration"),
        InlineKeyboardButton(text="🤒 Я пациент", callback_data="is_doctor_no")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def petnetrubot_kb(user_telegram_id: int):
    kb_list = [
        [InlineKeyboardButton(text="Служба заботы ПЭТ-Технолоджи", url='tg://resolve?domain=petnetru_bot')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def reg_user_kb(user_telegram_id: int):
    kb_list = [
        [InlineKeyboardButton(text="📄 Скачать информацию", callback_data="download_info")],
        [InlineKeyboardButton(text="👨‍⚕️ Направить пациента", callback_data="make_request")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard
