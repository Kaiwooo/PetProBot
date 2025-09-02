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

@registration_router.callback_query(F.data == "is_doctor_yes")
async def start_registration_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Нам потребуется ваше согласие на обработку ПД",
        reply_markup=privacy_kb(callback.from_user.id)
    )
    await state.set_state(Registration.privacy)
    await callback.answer()  # чтобы убрать "часики" на кнопке

# ------------------- Получение согласия ПД -------------------
@registration_router.callback_query(F.data.in_(["privacy_agreement_yes", "privacy_agreement_no"]))
async def process_privacy(callback: CallbackQuery, state: FSMContext):
    if callback.data == "privacy_agreement_yes":
        await state.update_data(privacy=True)
        await callback.answer("✅ Согласие на ПД получено")  # маленькое уведомление
        await callback.message.answer(
            "Для продолжения нам потребуется Ваше '''Согласие на коммуникацию''', в том числе маркетингового характера, через указанные вами способы связи.\n Обещаем, много писать не будеv",
            reply_markup=marketing_kb(callback.from_user.id)
        )
        await state.set_state(Registration.marketing)
        await callback.answer()
    else:
        await state.update_data(privacy=False)
        await callback.answer("Без '''Согласие на обработку Персональных Данных''' регистрация невозможна", show_alert=True)
        await state.clear()

# ------------------- Получение согласия Маркетинг-------------------
@registration_router.callback_query(F.data.in_(["marketing_agreement_yes", "marketing_agreement_no"]))
async def process_marketing(callback: CallbackQuery, state: FSMContext):
    if callback.data == "marketing_agreement_yes":
        await state.update_data(marketing=True)
        await callback.answer("✅ Согласие на маркетинг получено")  # toast
        await callback.message.answer(
            "Пожалуйста поделитесь своим телефоном",
            reply_markup=phone_kb()
    )
        await state.set_state(Registration.phone)
        await callback.answer()
    else:
        await state.update_data(privacy=False)
        await callback.answer("К сожалению, мы не Регистрируем без возможности коммуницировать с вами", show_alert=True)
        await state.clear()

@registration_router.message(F.contact, Registration.phone)
async def process_phone(message: Message, state: FSMContext):
    if message.contact.user_id != message.from_user.id:
        await message.answer("Пожалуйста, поделитесь вашим собственным контактом!")
        return
    await state.update_data(phone=message.contact.phone_number)
    await message.answer("Спасибо! А теперь введи ваше ФИО:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registration.full_name)


@registration_router.message(Registration.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("Укажите Ваш Email:")
    await state.set_state(Registration.email)


# ------------------- Email + валидация -------------------
def is_valid_email(email: str) -> bool:
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(pattern, email) is not None

@registration_router.message(Registration.email)
async def process_email(message: Message, state: FSMContext):
    if not is_valid_email(message.text):
        await message.answer("❌ Некорректный email!\nПример: example@mail.com")
        return
    await state.update_data(email=message.text)

    data = await state.get_data()
    if data.get('edit_field') == 'email':
        await state.update_data(edit_field=None)
        #await show_confirmation(message, state)  # тут важно, чтобы функция была определена
        return
    await message.answer("Укажите Ваш город:")
    await state.set_state(Registration.city)

#------------------------------------------------------------

@registration_router.message(Registration.city)
async def process_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Укажите Ваше медицинское учреждение:")
    await state.set_state(Registration.clinic)


@registration_router.message(Registration.clinic)
async def process_clinic(message: Message, state: FSMContext):
    await state.update_data(clinic=message.text)
    await message.answer("Введите должность / специализацию:")
    await state.set_state(Registration.position)


@registration_router.message(Registration.position)
async def process_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)

    data = await state.get_data()
    tg_user_id = message.from_user.id
    tg_user_name = message.from_user.username

    # сохраняем в память
    users_data[tg_user_id] = data
    users_data[tg_user_name] = data

    await message.answer(
        f"Регистрация завершена!"
        f"Телефон: {data['phone']}\n"
        f"ФИО: {data['full_name']}\n"
        f"Email: {data['email']}\n"
        f"Город: {data['city']}\n"
        f"Медицинское учреждение: {data['clinic']}\n"
        f"Должность: {data['position']}",
        reply_markup=confirm_reg_kb(message.from_user.id)
    )

    await state.clear()  # очищаем FSM