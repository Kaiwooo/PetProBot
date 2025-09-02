from aiogram import Router, F
from aiogram.types import CallbackQuery
from db_handler.user_storage import users_data
from keyboards.inline_kb import reg_user_kb, contract_templates_kb, docs_kb

account_router = Router()

@account_router.callback_query(F.data == 'my_profile')
async def account_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    user_data = users_data.get(callback.from_user.id)
    await callback.message.answer(
        f"Информация о вашем профиле:\n\n"
        f"ФИО: {user_data['full_name']}\n",
        reply_markup=reg_user_kb(callback.from_user.id)
    )

@account_router.callback_query(F.data == 'docs_templates')
async def account_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Выберите тип договора',
        reply_markup=contract_templates_kb(callback.from_user.id)
    )

@account_router.callback_query(F.data == 'download_info')
async def account_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup()
    await callback.message.answer('Выберите необходимую информацию для ознакомления',
                                  reply_markup=docs_kb(callback.from_user.id)
    )