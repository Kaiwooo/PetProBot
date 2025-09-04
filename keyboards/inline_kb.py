from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='Посмотреть агентов', callback_data='admin_agents')],
        [InlineKeyboardButton(text='Посмотреть пациентов', callback_data='admin_customers')],
        [InlineKeyboardButton(text='Отправить сообщение', callback_data='admin_send_message')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def start_kb(user_id: int, extra: bool = False):
    kb_list = [
        [InlineKeyboardButton(text='📖 О нас', callback_data='about')],
        [InlineKeyboardButton(text='🤒 Я пациент', callback_data='is_doctor_no'),
        InlineKeyboardButton(text='👨‍⚕️ Я врач', callback_data='is_doctor_yes')]
    ]
    if extra:
        kb_list.append([InlineKeyboardButton(text='⚙️ Админ панель', callback_data='admin_panel')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def medspec_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')],
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
        [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='Служба заботы ПЭТ-Технолоджи', url='tg://resolve?domain=petnetru_bot')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def reg_user_kb(user_id: int, full_name: str, extra: bool = False):
    kb_list = [
        # [InlineKeyboardButton(text='👨‍⚕️ Мой профиль', callback_data='my_profile')],
        [InlineKeyboardButton(text='Скачать файлы для врачей', url='https://www.pet-net.ru/page/komu-pokazano')],
        [InlineKeyboardButton(text='Связаться с главным радиологом', url=f'https://wa.me/74950330001?text=Здравствуйте,%20меня%20зовут%20{full_name}.%20У%20меня%20вопрос')],
        [InlineKeyboardButton(text='Сотрудничество', callback_data='cooperation')]
    ]
    if extra:
    # if user_id in admins:
         kb_list.append([InlineKeyboardButton(text="⚙️ Админ панель", callback_data="admin_panel")])
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
    kb_list = [ [InlineKeyboardButton(text="Исправить ФИО", callback_data="edit_full_name"),
                # [InlineKeyboardButton(text="Исправить Email", callback_data="edit_email"),
                InlineKeyboardButton(text="Исправить город", callback_data="edit_city")],
                [InlineKeyboardButton(text="Исправить медицинское учреждение", callback_data="edit_clinic"),
                InlineKeyboardButton(text="Исправить должность", callback_data="edit_position")],
                [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_registration")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def confirm_patient_kb(user_id: int):
    kb_list = [ [InlineKeyboardButton(text="Исправить ФИО", callback_data="edit_patient_full_name"),
                InlineKeyboardButton(text="Исправить телефон", callback_data="edit_patient_phone_number")],
                [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_patient")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def verified_user_kb(user_id: int):
    kb_list = [
        #[InlineKeyboardButton(text='👨‍⚕️ Мой профиль', callback_data='my_profile')],
        [InlineKeyboardButton(text='Шаблоны договоров', callback_data='docs_templates')],
        [InlineKeyboardButton(text='Скачать информацию', callback_data='download_info')],
        [InlineKeyboardButton(text='Направить пациента', callback_data='make_request')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def cooperation_kb(user_id: int, full_name: str):
    #full_name = users_data.get(user_id).get("full_name")
    kb_list = [
        [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='Заполнить договор', url='https://docs.google.com/document/d/1VQ2xMdnXdZGpRJWHajM6cZv5pif-o0qZ/edit?usp=sharing&ouid=115324883075267776916&rtpof=true&sd=true')],
        [InlineKeyboardButton(text='Записать пациента', callback_data='make_request')],
        [InlineKeyboardButton(text='Остались вопросы', url=f'https://wa.me/74950330001?text=Здравствуйте,%20меня%20зовут%20{full_name}.%20У%20меня%20вопрос%20по%20сотрудничеству')]
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

# def docs_kb(user_id: int):
#     kb_list = [
#         [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')],
#         [InlineKeyboardButton(text='Сайт для партнеров',
#                               url='https://www.pet-net.ru/page/partnership')],
#         [InlineKeyboardButton(text='Карта с разбивкой по трейсерам',
#                               url='https://www.pet-net.ru/page/komu-pokazano#imageSlider')],
#         [InlineKeyboardButton(text='Как записаться пациенту в ПЭТ технолоджи',
#                               url='https://drive.google.com/file/d/1IsOaaJCs9BNxDVM-XN4QcbaYy4A94yvQ/view?usp=sharing')],
#         [InlineKeyboardButton(text='Как записать пациента на ПЭТ-КТ с глюкозой ПСМА или тирозином',
#                               url='https://drive.google.com/file/d/1zdRg07uyQPlSm7N2kb43gilprazi2pXn/view?usp=sharing')],
#         [InlineKeyboardButton(text='Московский кластер «ПЭТ-Технолоджи»',
#                               url='https://drive.google.com/file/d/1nRBL5Zhx6SQmeI_y8CGDoAHXX8E-q-3F/view?usp=sharing')],
#         [InlineKeyboardButton(text='Карта центров «ПЭТ-Технолоджи»',
#                               url='https://drive.google.com/file/d/1dpRP3dEClATW0ENY5Dq8Hy1MT5bAYIR8/view?usp=sharing')],
#         [InlineKeyboardButton(text='Карта «ПЭТ-Технолоджи» с трейсерами',
#                               url='https://drive.google.com/file/d/1uvZbWGCV2bhed-7KmJKOp5DOayOGvEJN/view?usp=sharing')],
#     ]
#     keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
#     return keyboard