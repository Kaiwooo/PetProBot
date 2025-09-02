import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db_handler.user_storage import users_data
from keyboards.inline_kb import reg_user_kb, confirm_reg_kb, privacy_kb, marketing_kb
from keyboards.regular_kb import phone_kb

registration_router = Router()

# ------------------- FSM -------------------
class Registration(StatesGroup):
    privacy = State()
    marketing = State()
    phone = State()
    full_name = State()
    email = State()
    city = State()
    clinic = State()
    position = State()
    confirmation = State()

@registration_router.callback_query(F.data == 'is_doctor_yes')
async def start_registration_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        'Нам потребуется ваше согласие на обработку ПД',
        reply_markup=privacy_kb(callback.from_user.id)
    )
    await state.set_state(Registration.privacy)
    await callback.answer()  # чтобы убрать "часики" на кнопке

# ------------------- Получение согласия ПД -------------------
@registration_router.callback_query(F.data.in_(['privacy_agreement_yes', 'privacy_agreement_no']))
async def process_privacy(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'privacy_agreement_yes':
        await state.update_data(privacy=True)
        await callback.message.edit_reply_markup()  # убираем кнопки
        await callback.answer('✅ Согласие на ПД получено')  # маленькое уведомление
        await callback.message.answer(
            'Для продолжения примите "Согласие на коммуникацию" (в том числе маркетингового характера), через указанные вами способы связи.\n Обещаем, много писать не будем',
            reply_markup=marketing_kb(callback.from_user.id)
        )
        await state.set_state(Registration.marketing)
        await callback.answer()
    else:
        await state.update_data(privacy=False)
        await callback.answer('Без принятия "Согласие на обработку Персональных Данных" регистрация невозможна', show_alert=True)
        await state.clear()

# ------------------- Получение согласия Маркетинг-------------------
@registration_router.callback_query(F.data.in_(['marketing_agreement_yes', 'marketing_agreement_no']))
async def process_marketing(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'marketing_agreement_yes':
        await state.update_data(marketing=True)
        await callback.message.edit_reply_markup()  # убираем кнопки
        await callback.answer('✅ Согласие на маркетинг получено')  # toast
        await callback.message.answer(
            'Пожалуйста поделитесь своим телефоном',
            reply_markup=phone_kb()
    )
        await state.set_state(Registration.phone)
        await callback.answer()
    else:
        await state.update_data(privacy=False)
        await callback.answer('К сожалению, регистрация без возможности отправлять Вам сообщения невозможна', show_alert=True)
        await state.clear()

@registration_router.message(F.contact, Registration.phone)
async def process_phone(message: Message, state: FSMContext):
    if message.contact.user_id != message.from_user.id:
        await message.answer('Пожалуйста, поделитесь вашим собственным контактом!')
        return
    await state.update_data(phone=message.contact.phone_number)
    await message.answer('Спасибо! А теперь введи ваше ФИО:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registration.full_name)


@registration_router.message(Registration.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    if data.get('edit_field') == 'full_name':
        await state.update_data(edit_field=None)
        await show_confirmation(message, state)
        return
    await message.answer('Введите ваш Email:')
    await state.set_state(Registration.email)

# ------------------- валидация email-------------------
def is_valid_email(email: str) -> bool:
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(pattern, email) is not None

@registration_router.message(Registration.email)
async def process_email(message: Message, state: FSMContext):
    if not is_valid_email(message.text):
        await message.answer('❌ Некорректный email!\nПример: example@mail.com')
        return
    await state.update_data(email=message.text)
    data = await state.get_data()
    if data.get('edit_field') == 'email':
        await state.update_data(edit_field=None)
        await show_confirmation(message, state)  # тут важно, чтобы функция была определена
        return
    await message.answer('Укажите Ваш город:')
    await state.set_state(Registration.city)

@registration_router.message(Registration.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()

    if data.get('edit_field') == 'city':
        await state.update_data(edit_field=None)
        await show_confirmation(message, state)
        return

    await message.answer('Введите медицинское учреждение:')
    await state.set_state(Registration.clinic)

@registration_router.message(Registration.clinic)
async def process_clinic(message: Message, state: FSMContext):
    await state.update_data(clinic=message.text)
    data = await state.get_data()
    if data.get('edit_field') == 'clinic':
        await state.update_data(edit_field=None)
        await show_confirmation(message, state)
        return
    await message.answer('Введите должность / специализацию:')
    await state.set_state(Registration.position)

@registration_router.message(Registration.position)
async def process_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    data = await state.get_data()
    if data.get('edit_field') == 'position':
        await state.update_data(edit_field=None)
        await show_confirmation(message, state)
        return
    await show_confirmation(message, state)

# ------------------- Показываем подтверждение -------------------
async def show_confirmation(obj: Message | CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(Registration.confirmation)
    summary = (
        f"Проверьте введённые данные:\n\n"
        f"Телефон: {data['phone']}\n"
        f"ФИО: {data['full_name']}\n"
        f"Email: {data['email']}\n"
        f"Город: {data['city']}\n"
        f"Медицинское учреждение: {data['clinic']}\n"
        f"Должность: {data['position']}"
    )

    keyboard = confirm_reg_kb(obj.from_user.id)

    if isinstance(obj, CallbackQuery):
        await obj.message.edit_text(summary, reply_markup=keyboard)
        await obj.answer()
    else:
        await obj.answer(summary, reply_markup=keyboard)

# ------------------- Обработчики кнопок "Исправить ..." -------------------
@registration_router.callback_query(F.data == 'edit_full_name', Registration.confirmation)
async def edit_full_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='full_name')
    await callback.message.answer('Введите корректное ФИО:')
    await state.set_state(Registration.full_name)
    await callback.answer()

@registration_router.callback_query(F.data == 'edit_email', Registration.confirmation)
async def edit_email(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='email')
    await callback.message.answer('Введите корректный Email:')
    await state.set_state(Registration.email)
    await callback.answer()

@registration_router.callback_query(F.data == 'edit_city', Registration.confirmation)
async def edit_city(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='city')
    await callback.message.answer('Введите корректный город:')
    await state.set_state(Registration.city)
    await callback.answer()

@registration_router.callback_query(F.data == 'edit_clinic', Registration.confirmation)
async def edit_clinic(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='clinic')
    await callback.message.answer('Введите корректное медицинское учреждение:')
    await state.set_state(Registration.clinic)
    await callback.answer()

@registration_router.callback_query(F.data == 'edit_position', Registration.confirmation)
async def edit_position(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='position')
    await callback.message.answer('Введите корректную должность / специализацию:')
    await state.set_state(Registration.position)
    await callback.answer()

# ------------------- Подтверждение регистрации -------------------
@registration_router.callback_query(F.data == 'confirm_registration')
async def confirm_registration(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users_data[callback.from_user.id] = data
    await callback.message.edit_text(
        f"Уважаемый {data['full_name']}, спасибо за регистрацию!",
        reply_markup=reg_user_kb(callback.from_user.id),
    )
    await state.clear() # очищаем FSM