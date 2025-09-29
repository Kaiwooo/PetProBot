#!/usr/bin/env

import asyncio
from create_bot import bot, scheduler, dp
from handlers.account import account_router
from handlers.admin import admin_router
from handlers.registration import registration_router
from handlers.request_contract import request_contract_router
from handlers.send_message import send_message_router
from handlers.start import start_router
from db_handler.postgres import db
# from work_time.time_func import send_time_msg

async def main():
    await db.connect()
    # регистрация роутеров
    dp.include_router(send_message_router)
    dp.include_router(account_router)
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(registration_router)
    dp.include_router(request_contract_router)
    # запуск бота в режиме long polling при запуске бот очищает все обновления, которые были за его моменты бездействия
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        await db.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass