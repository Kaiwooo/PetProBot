import asyncpg
from asyncpg.pool import Pool
from decouple import config
from typing import Optional
from datetime import datetime

class Database:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: Optional[Pool] = None

    async def connect(self, min_size=1, max_size=10):
        self.pool = await asyncpg.create_pool(
            dsn=self.dsn,
            min_size=min_size,
            max_size=max_size
        )

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def fetchrow(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetch(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchval(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

# Инициализируем глобальный объект базы
db = Database(config("PG_LINK"))

# ------------------ AGENTS ------------------
async def is_user_registered(telegram_id: int) -> bool:
    row = await db.fetchrow(
        "SELECT telegram_id FROM agents WHERE telegram_id=$1",
        telegram_id
    )
    return row is not None

async def add_agent(telegram_id: int, username: str | None, full_name: str,
                    phone_number: str, city: str, privacy: bool, created: datetime,
                    bitrix_contact_id: int | None = None, bitrix_deal_id: int | None = None):
    await db.execute(
        """INSERT INTO agents (
            telegram_id,
            telegram_username,
            full_name,
            phone_number,
            city,
            created,
            privacy,
            bitrix_contact_id,
            bitrix_deal_id
            )
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) ON CONFLICT (telegram_id) DO UPDATE SET
            telegram_username = EXCLUDED.telegram_username,
            full_name = EXCLUDED.full_name,
            phone_number = EXCLUDED.phone_number,
            city = EXCLUDED.city,
            created = EXCLUDED.created,
            privacy = EXCLUDED.privacy,
            bitrix_contact_id = EXCLUDED.bitrix_contact_id,
            bitrix_deal_id = EXCLUDED.bitrix_deal_id
            """,
        telegram_id,
        username,
        full_name,
        phone_number,
        city,
        created,
        privacy,
        bitrix_contact_id,
        bitrix_deal_id
    )

async def update_agent(email: str, organization: str, position: str, telegram_id: int):
    return await db.fetchrow(
        """UPDATE agents SET email=$1, organization=$2, position=$3, requested_contract=TRUE
        WHERE telegram_id=$4
        RETURNING bitrix_contact_id, bitrix_deal_id
        """,
            email, organization, position, telegram_id
    )

async def get_agents():
    return await db.fetch("SELECT * FROM agents ORDER BY created DESC")

# ------------------ CUSTOMERS ------------------
async def add_customer(agent_id: int, full_name: str,
                       phone_number: str, created: datetime, deal_id: int):
    await db.execute(
        """INSERT INTO customers (
        agent_id,
        full_name, 
        phone_number,
        created,
        bitrix_deal_id
        ) VALUES ($1,$2,$3,$4,$5)
        """,
        agent_id,
        full_name,
        phone_number,
        created,
        deal_id
    )

async def get_customers():
    return await db.fetch("SELECT * FROM customers ORDER BY created DESC")