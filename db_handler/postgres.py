import asyncpg
from asyncpg.pool import Pool
from decouple import config
from typing import Optional


class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Optional[Pool] = None

    async def connect(self, min_size=1, max_size=10):
        """Инициализация пула соединений"""
        self.pool = await asyncpg.create_pool(
            dsn=self.dsn,
            min_size=min_size,
            max_size=max_size
        )

    async def close(self):
        """Закрыть пул соединений"""
        if self.pool:
            await self.pool.close()

    async def fetchrow(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetch(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

# Инициализируем глобальный объект базы
db = Database(config("PG_LINK"))

# ------------------ AGENTS ------------------
async def is_user_registered(telegram_id: int) -> bool:
    """Проверка, есть ли пользователь в таблице agents"""
    row = await db.fetchrow(
        "SELECT telegram_id FROM agents WHERE telegram_id=$1",
        telegram_id
    )
    return row is not None

async def add_agent(telegram_id: int, username: str | None, full_name: str,
                    phone_number: str, city: str | None, organization: str | None,
                    position: str | None, privacy: bool, marketing: bool):
    """Добавить или обновить агента"""
    await db.execute("""
        INSERT INTO agents (
            telegram_id, telegram_username, full_name,
            phone_number, city, organization, position,
            created, privacy, marketing
        )
        VALUES ($1,$2,$3,$4,$5,$6,$7,NOW(),$8,$9)
        ON CONFLICT (telegram_id) DO UPDATE SET
            telegram_username = EXCLUDED.telegram_username,
            full_name = EXCLUDED.full_name,
            phone_number = EXCLUDED.phone_number,
            city = EXCLUDED.city,
            organization = EXCLUDED.organization,
            position = EXCLUDED.position,
            privacy = EXCLUDED.privacy,
            marketing = EXCLUDED.marketing
    """, telegram_id, username, full_name, phone_number,
         city, organization, position, privacy, marketing)

async def get_agents():
    """Получить всех агентов"""
    return await db.fetch("SELECT * FROM agents ORDER BY created DESC")

# ------------------ CUSTOMERS ------------------
async def add_customer(agent_id: int, full_name: str, phone_number: str, center: str | None):
    """Добавить пациента (customer)"""
    await db.execute("""
        INSERT INTO customers (
            agent_id, full_name, phone_number, center, created
        )
        VALUES ($1,$2,$3,$4,NOW())
    """, agent_id, full_name, phone_number, center)

async def get_customers():
    """Получить всех пациентов"""
    return await db.fetch("SELECT * FROM customers ORDER BY created DESC")