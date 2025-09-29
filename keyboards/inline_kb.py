from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='Посмотреть агентов', callback_data='admin_agents')],
        [InlineKeyboardButton(text='Посмотреть пациентов', callback_data='admin_customers')],
        [InlineKeyboardButton(text='Посмотреть незавершенные регистрации', callback_data='admin_incomplete_agents')],
        [InlineKeyboardButton(text='Отправить сообщение', callback_data='admin_send_message')]
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

def reg_user_kb(user_id: int, requested_contract: bool, full_name: str | None = None):
    kb_list = [
        [InlineKeyboardButton(text='Скачать файлы для врачей', url='https://www.pet-net.ru/page/komu-pokazano')],
        [InlineKeyboardButton(text='Связаться с главным радиологом', url=f'https://wa.me/74950330001?text=Здравствуйте,%20меня%20зовут%20{full_name}.%20У%20меня%20вопрос')],
        [InlineKeyboardButton(
            text='Направить пациента' if requested_contract else 'Сотрудничество',
            callback_data='send_patient' if requested_contract else 'cooperation'
        )]    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def privacy_kb(user_id: int):
    kb_list = [
        [InlineKeyboardButton(text='✅ Принимаю', callback_data='privacy_agreement_yes'),
        InlineKeyboardButton(text='❌ Отказываюсь', callback_data='privacy_agreement_no')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

# def marketing_kb(user_id: int):
#     kb_list = [
#         [InlineKeyboardButton(text='✅ Принимаю', callback_data='marketing_agreement_yes'),
#         InlineKeyboardButton(text='❌ Отказываюсь', callback_data='marketing_agreement_no')]
#     ]
#     keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
#     return keyboard

def confirm_reg_kb(user_id: int):
    kb_list = [ [InlineKeyboardButton(text="Исправить ФИО", callback_data="edit_full_name"),
                InlineKeyboardButton(text="Исправить город", callback_data="edit_city")],
                [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_registration")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def confirm_full_info_kb(user_id: int):
    kb_list = [ [InlineKeyboardButton(text="Исправить Email", callback_data="edit_email")],
                [InlineKeyboardButton(text="Исправить клинику", callback_data="edit_organization")],
                [InlineKeyboardButton(text="Исправить должность", callback_data="edit_position")],
                [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_full_info")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def confirm_patient_kb(user_id: int):
    kb_list = [ [InlineKeyboardButton(text="Исправить ФИО", callback_data="edit_patient_full_name"),
                InlineKeyboardButton(text="Исправить телефон", callback_data="edit_patient_phone_number")],
                [InlineKeyboardButton(text="❌ Отменить", callback_data="main_menu")],
                [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_patient")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard

def cooperation_kb(user_id: int):
    #full_name = users_data.get(user_id).get("full_name")
    kb_list = [
        [InlineKeyboardButton(text='Вернуться в главное меню', callback_data='main_menu')],
        [InlineKeyboardButton(text='Заполнить договор', callback_data='request_contract')],
        [InlineKeyboardButton(text='Остались вопросы', url=f'https://wa.me/74950330001?text=Здравствуйте,%20у%20меня%20вопрос%20по%20сотрудничеству')]
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return keyboard