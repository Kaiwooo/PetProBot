from create_bot import admins
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_kb(user_id: int):
    if user_id in admins:
        kb_list = [[InlineKeyboardButton(text='⚙️ Админ панель', callback_data='admin_panel')]]
    else:
        kb_list = [
            [InlineKeyboardButton(text='📖 О нас', callback_data='about')],
            [InlineKeyboardButton(text='👤 Зарегистрироваться', callback_data='registration')]
    ]
        #kb_list.append([InlineKeyboardButton(text='⚙️ Админ панель', callback_data='admin_panel')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def medspec_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='✅ Да', callback_data='is_doctor_yes')],
        [InlineKeyboardButton(text='❌ Нет', callback_data='is_doctor_no')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def about_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='👤 Зарегистрироваться', callback_data='registration')],
        [InlineKeyboardButton(text='🤒 Я пациент', callback_data='is_doctor_no')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def petnetrubot_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='Служба заботы ПЭТ-Технолоджи', url='tg://resolve?domain=petnetru_bot')],
        [InlineKeyboardButton(text='Вернуться в клавное меню', callback_data='main_menu')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def reg_user_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='📄 Скачать информацию', callback_data='download_info')],
        [InlineKeyboardButton(text='👨‍⚕️ Направить пациента', callback_data='make_request')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def privacy_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='✅ Принимаю', callback_data='privacy_agreement_yes'),
        InlineKeyboardButton(text='❌ Отказываюсь', callback_data='privacy_agreement_no')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def marketing_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='✅ Принимаю', callback_data='marketing_agreement_yes'),
        InlineKeyboardButton(text='❌ Отказываюсь', callback_data='marketing_agreement_no')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def confirm_reg_kb(user_id: int):
    kb_list = [ [InlineKeyboardButton(text="Исправить ФИО", callback_data="edit_full_name")],
                [InlineKeyboardButton(text="Исправить Email", callback_data="edit_email"),
                InlineKeyboardButton(text="Исправить город", callback_data="edit_city")],
                [InlineKeyboardButton(text="Исправить медицинское учреждение", callback_data="edit_clinic"),
                InlineKeyboardButton(text="Исправить должность", callback_data="edit_position")],
                [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_registration")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard