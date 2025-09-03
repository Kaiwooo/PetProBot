from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from db_handler.user_storage import patient_data
from keyboards.inline_kb import reg_user_kb, cooperation_kb, confirm_patient_kb

account_router = Router()

class PatientFromAgent(StatesGroup):
    full_name = State()
    phone_number = State()
    confirmation = State()

# @account_router.callback_query(F.data == 'my_profile')
# async def account_callback(callback: CallbackQuery):
#     await callback.message.edit_reply_markup()
#     user_data = users_data.get(callback.from_user.id)
#     await callback.message.answer(
#         f"Информация о вашем профиле:\n\n"
#         f"Ваше ФИО: {user_data['full_name']}\n",
#         reply_markup=reg_user_kb(callback.from_user.id)
#     )

@account_router.callback_query(F.data == 'cooperation')
async def account_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Вы можете направлять платных пациентов за вознаграждение в размере 10% от стоимости ПЭТ/КТ (или других услуг).\n\n'
                                  'Как происходит сотрудничество?\n'
                                  '* Заполните договор о сотрудничестве\n'
                                  '* Выдайте пациенту рекомендацию для проведения ПЭТ/КТ и памятку по подготовке\n'
                                  '* Запишите пациента на услугу\n'
                                  '* После того, как пациент пройдет ПЭТ/КТ на платной основе, выплата придет Вам в ближайший четверг после дня исследования',
                                  reply_markup=cooperation_kb(callback.from_user.id)
                                  )

# @account_router.callback_query(F.data == 'docs_templates')
# async def account_callback(callback: CallbackQuery):
#     await callback.message.edit_reply_markup()
#     await callback.message.answer('Выберите тип договора',
#         reply_markup=cooperation_kb(callback.from_user.id)
#     )

# @account_router.callback_query(F.data == 'download_info')
# async def account_callback(callback: CallbackQuery):
#     await callback.message.edit_reply_markup()
#     await callback.message.answer('Выберите необходимую информацию для ознакомления',
#                                   reply_markup=docs_kb(callback.from_user.id)
#     )

@account_router.callback_query(F.data == 'make_request')
async def account_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Нам потребуется ФИО вашего пациента.')
    await state.set_state(PatientFromAgent.full_name)
    await callback.answer()

@account_router.message(PatientFromAgent.full_name)
async def patient_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    if data.get('edit_field') == 'full_name':
        await state.update_data(edit_field=None)
        await confirmation(message, state)
        return
    await message.answer('Укажите контактный номер пациента:')
    await state.set_state(PatientFromAgent.phone_number)

@account_router.message(PatientFromAgent.phone_number)
async def patient_full_name(message: Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    data = await state.get_data()
    if data.get('edit_field') == 'phone_number':
        await state.update_data(edit_field=None)
        await confirmation(message, state)
        return
    await confirmation(message, state)

#----------------------- Показываем подтверждение ------------------------

async def confirmation(obj: Message | CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(PatientFromAgent.confirmation)
    summary = (
        f"Проверьте введённые данные:\n\n"
        f"ФИО: {data['full_name']}\n"
        f"Телефон: {data['phone_number']}\n"
    )
    keyboard = confirm_patient_kb(obj.from_user.id)
    if isinstance(obj, CallbackQuery):
        await obj.message.edit_text(summary, reply_markup=keyboard)
        await obj.answer()
    else:
        await obj.answer(summary, reply_markup=keyboard)

#----------------------- Обработчики правок ------------------------

@account_router.callback_query(F.data == 'edit_patient_full_name', PatientFromAgent.confirmation)
async def edit_full_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='full_name')
    try:    # попробуем отредактировать предыдущее (подтверждающее) сообщение бота
        await callback.message.edit_text("Введите корректное ФИО:", reply_markup=None)
    except Exception:   # если редактирование не удалось (например, сообщение нельзя редактировать), упадём обратно к отправке нового сообщения, но это редкий случай
        await callback.message.answer("Введите корректное ФИО:")
    await state.set_state(PatientFromAgent.full_name)
    await callback.answer()

@account_router.callback_query(F.data == 'edit_patient_phone_number', PatientFromAgent.confirmation)
async def edit_full_name(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='phone_number')
    try:    # попробуем отредактировать предыдущее (подтверждающее) сообщение бота
        await callback.message.edit_text("Введите корректный номер телефона:", reply_markup=None)
    except Exception:   # если редактирование не удалось (например, сообщение нельзя редактировать), упадём обратно к отправке нового сообщения, но это редкий случай
        await callback.message.answer("Введите корректный номер телефона:")
    await state.set_state(PatientFromAgent.phone_number)
    await callback.answer()

#----------------------- Подтверждение записи ------------------------

@account_router.callback_query(F.data == 'confirm_patient')
async def confirm_registration(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    patient_data[callback.from_user.id] = data
    await callback.message.edit_text(
        # f"Уважаемый {data['full_name']}, мы приняли ваш запрос на запись
        f"Мы приняли ваш запрос на запись {data['full_name']} в центр ПЭТ-Технолоджи",
        reply_markup=reg_user_kb(callback.from_user.id)
    )
    await state.clear() # очищаем FSM