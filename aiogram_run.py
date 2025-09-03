import asyncio
from create_bot import bot, dp, scheduler
from handlers.account import account_router
from handlers.admin import admin_router
from handlers.registration import registration_router
from handlers.start import start_router
from db_handler.db import init_db, close_db

# from work_time.time_func import send_time_msg

async def main():
    await init_db()
    # регистрация роутеров
    dp.include_router(start_router)
    dp.include_router(registration_router)
    dp.include_router(account_router)
    dp.include_router(admin_router)
    # запуск бота в режиме long polling при запуске бот очищает все обновления, которые были за его моменты бездействия
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        await close_db()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass