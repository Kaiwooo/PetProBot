from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.inline_kb import reg_user_kb, cooperation_kb, confirm_full_info_kb
from db_handler.postgres import db
import re
from services.bitrix import update_contact, change_deal_stage, create_company

request_contract_router=Router()

# ------------------- FSM -------------------
class FullAgentInfo(StatesGroup):
    email = State()
    organization = State()
    position = State()
    confirmation = State()

@request_contract_router.callback_query(F.data == 'cooperation')
async def account_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.answer()
    row = await db.fetchrow(
            "SELECT full_name FROM agents WHERE telegram_id=$1",
            callback.from_user.id
        )
    full_name = row["full_name"]
    await callback.message.answer('Вы можете направлять платных пациентов за вознаграждение в размере 10% от стоимости ПЭТ/КТ (или других услуг).\n\n'
                                  'Как происходит сотрудничество?\n'
                                  '* Заполните договор о сотрудничестве\n'
                                  '* Выдайте пациенту рекомендацию для проведения ПЭТ/КТ и памятку по подготовке\n'
                                  '* Запишите пациента на услугу\n'
                                  '* После того, как пациент пройдет ПЭТ/КТ на платной основе, выплата придет Вам в ближайший четверг после дня исследования',
                                  reply_markup=cooperation_kb(callback.from_user.id, full_name)
                                  )

@request_contract_router.callback_query(F.data == 'request_contract')
async def account_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Для сотрудничества нам потребуется еще немного - укажите ваш email.')
    await state.set_state(FullAgentInfo.email)
    await callback.answer()

# ------------------- Обработчики ввода -------------------

# ------------------- валидация email -------------------
def is_valid_email(email: str) -> bool:
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(pattern, email) is not None

@request_contract_router.message(FullAgentInfo.email)
async def process_email(message: Message, state: FSMContext):
    if not is_valid_email(message.text):
        await message.answer('❌ Некорректный email!\nПример: example@mail.com')
        return
    await state.update_data(email=message.text)
    data = await state.get_data()
    if data.get('edit_field') == 'email':
        await state.update_data(edit_field=None)
        await show_confirmation2(message, state)  # тут важно, чтобы функция была определена
        return
    await message.answer('Введите медицинское учреждение:')
    await state.set_state(FullAgentInfo.organization)

@request_contract_router.message(FullAgentInfo.organization)
async def process_organization(message: Message, state: FSMContext):
    await state.update_data(organization=message.text)
    data = await state.get_data()
    if data.get('edit_field') == 'organization':
        await state.update_data(edit_field=None)
        await show_confirmation2(message, state)
        return
    await message.answer('Введите должность / специализацию:')
    await state.set_state(FullAgentInfo.position)

@request_contract_router.message(FullAgentInfo.position)
async def process_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    data = await state.get_data()
    if data.get('edit_field') == 'position':
        await state.update_data(edit_field=None)
        await show_confirmation2(message, state)
        return
    await show_confirmation2(message, state)

# ------------------- Показываем подтверждение -------------------
async def show_confirmation2(obj: Message | CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(FullAgentInfo.confirmation)
    summary = (
        f"Пожалуйста внимательно проверьте введённые данные.\n\n"
        f"Email: {data['email']}\n"
        f"Медицинское учреждение: {data['organization']}\n"
        f"Должность: {data['position']}"
    )
    keyboard = confirm_full_info_kb(obj.from_user.id)
    if isinstance(obj, CallbackQuery):
        await obj.message.edit_text(summary, reply_markup=keyboard)
        await obj.answer()
    else:
        await obj.answer(summary, reply_markup=keyboard)

# ------------------- Обработчики кнопок "Исправить ..." -------------------
@request_contract_router.callback_query(F.data == 'edit_email', FullAgentInfo.confirmation)
async def edit_email(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='email')
    try:
        await callback.message.edit_text('Введите корректный Email:', reply_markup=None)
    except Exception:
        await callback.message.answer('Введите корректный Email:')
    await state.set_state(FullAgentInfo.email)
    await callback.answer()

@request_contract_router.callback_query(F.data == 'edit_organization', FullAgentInfo.confirmation)
async def edit_organization(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='organization')
    try:
        await callback.message.edit_text('Введите корректное медицинское учреждение:', reply_markup=None)
    except Exception:
        await callback.message.answer('Введите корректное медицинское учреждение:')
    await state.set_state(FullAgentInfo.organization)
    await callback.answer()

@request_contract_router.callback_query(F.data == 'edit_position', FullAgentInfo.confirmation)
async def edit_position(callback: CallbackQuery, state: FSMContext):
    await state.update_data(edit_field='position')
    try:
        await callback.message.edit_text('Введите корректную должность / специализацию:', reply_markup=None)
    except Exception:
        await callback.message.answer('Введите корректную должность / специализацию:')
    await state.set_state(FullAgentInfo.position)
    await callback.answer()

# ------------------- Подтверждение регистрации -------------------
@request_contract_router.callback_query(F.data == 'confirm_full_info')
async def confirm_full_info(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    email = data.get('email')
    organization = data.get('organization')
    position = data.get('position')
    await db.execute(
            "UPDATE agents SET email=$1, organization=$2, position=$3, requested_contract=TRUE WHERE telegram_id=$4",
            email, organization, position, callback.from_user.id
        )
    row = await db.fetchrow(
            "SELECT bitrix_contact_id, bitrix_deal_id FROM agents WHERE telegram_id=$1",
            callback.from_user.id
        )
    contact_id = row["bitrix_contact_id"]
    deal_id = row["bitrix_deal_id"]
    company_id = await create_company(title=organization)
    if contact_id:
        # Обновляем контакт
        await update_contact(contact_id, {
            "EMAIL": [{"VALUE": email, "VALUE_TYPE": "WORK"}],
            "COMPANY_ID": company_id,
            "POST": position
        })
    if deal_id:
        await change_deal_stage(deal_id, "PREPARATION")  # пример стадии

    await state.clear() # очищаем FSM
    await callback.message.edit_text(
        f'Пожалуйста ознакомьтесь с <a href="https://www.pet-net.ru/storage/app/media/sotrudnichestvo/%D0%90%D0%B3%D0%B5%D0%BD%D1%82%D1%81%D0%BA%D0%B8%D0%B9%20%D0%B4%D0%BE%D0%B3%D0%BE%D0%B2%D0%BE%D1%80%20%D1%81%20%D1%84%D0%B8%D0%B7.%D0%BB%D0%B8%D1%86%D0%BE%D0%BC.docx">Договором</a>.\n'
        f'Медицинский представитель свяжется с вами чтобы запросить реквизиты для подписания',
        reply_markup=reg_user_kb(callback.from_user.id, full_name=None, requested_contract=True)
    )
        # reply_markup=reg_user_kb(callback.from_user.id, full_name))  # сообщение после подтверждения
