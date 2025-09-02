
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='⚙️ Админ панель', callback_data='admin_panel')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def start_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='📖 О нас', callback_data='about')],
        [InlineKeyboardButton(text='🤒 Я пациент', callback_data='is_doctor_no'),
        InlineKeyboardButton(text='👨‍⚕️ Я врач', callback_data='is_doctor_yes')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def medspec_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='Вернуться в клавное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='👤 Зарегистрироваться', callback_data='registration')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def about_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='🤒 Я пациент', callback_data='is_doctor_no'),
         InlineKeyboardButton(text='👨‍⚕️ Я врач', callback_data='is_doctor_yes')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def petnetrubot_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='Вернуться в клавное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='Служба заботы ПЭТ-Технолоджи', url='tg://resolve?domain=petnetru_bot')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def reg_user_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='👨‍⚕️ Мой профиль', callback_data='my_profile')],
        [InlineKeyboardButton(text='Шаблоны договоров', callback_data='docs_templates')],
        [InlineKeyboardButton(text='Скачать информацию', callback_data='download_info')],
        [InlineKeyboardButton(text='Главный Радиолог Слушает', url='https://api.whatsapp.com/send?phone=74950330001')],
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

def verified_user_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='👨‍⚕️ Мой профиль', callback_data='my_profile')],
        [InlineKeyboardButton(text='Шаблоны договоров', callback_data='docs_templates')],
        [InlineKeyboardButton(text='Скачать информацию', callback_data='download_info')],
        [InlineKeyboardButton(text='Направить пациента', callback_data='make_request')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def contract_templates_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='Вернуться в клавное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='Агентский договор с физ. лицом', url='https://docs.google.com/document/d/1VQ2xMdnXdZGpRJWHajM6cZv5pif-o0qZ/edit?usp=sharing&ouid=115324883075267776916&rtpof=true&sd=true')],
        [InlineKeyboardButton(text='Агентский договор с юр. лицом', url='https://docs.google.com/document/d/1clnpvUzvyLBCYAuDi7k843w2i-ToyOyn/edit?usp=sharing&ouid=115324883075267776916&rtpof=true&sd=true')],
        [InlineKeyboardButton(text='Агентский договор с юр. лицом по гарантийным письмам', url='https://docs.google.com/document/d/13BLPArOc5yli6sqCGM0P51IMQ9ahOunJ/edit?usp=sharing&ouid=115324883075267776916&rtpof=true&sd=true')]
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def docs_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='Вернуться в клавное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='Сайт для партнеров',
                              url='https://www.pet-net.ru/page/partnership')],
        [InlineKeyboardButton(text='Карта с разбивкой по трейсерам',
                              url='https://www.pet-net.ru/page/komu-pokazano#imageSlider')],
        [InlineKeyboardButton(text='Как записаться пациенту в ПЭТ технолоджи',
                              url='https://drive.google.com/file/d/1IsOaaJCs9BNxDVM-XN4QcbaYy4A94yvQ/view?usp=sharing')],
        [InlineKeyboardButton(text='Как записать пациента на ПЭТ-КТ с глюкозой ПСМА или тирозином',
                              url='https://drive.google.com/file/d/1zdRg07uyQPlSm7N2kb43gilprazi2pXn/view?usp=sharing')],
        [InlineKeyboardButton(text='Московский кластер «ПЭТ-Технолоджи»',
                              url='https://drive.google.com/file/d/1nRBL5Zhx6SQmeI_y8CGDoAHXX8E-q-3F/view?usp=sharing')],
        [InlineKeyboardButton(text='Карта центров «ПЭТ-Технолоджи»',
                              url='https://drive.google.com/file/d/1dpRP3dEClATW0ENY5Dq8Hy1MT5bAYIR8/view?usp=sharing')],
        [InlineKeyboardButton(text='Карта «ПЭТ-Технолоджи» с трейсерами',
                              url='https://drive.google.com/file/d/1uvZbWGCV2bhed-7KmJKOp5DOayOGvEJN/view?usp=sharing')],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard