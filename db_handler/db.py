import asyncpg
from asyncpg.pool import Pool
from decouple import config

db_pool: asyncpg.Pool | None = None

async def init_db():
    """Инициализация пула соединений с PostgreSQL"""
    global db_pool
    db_pool = await asyncpg.create_pool(
        dsn=config("PG_LINK"),
        min_size=1,
        max_size=10
    )

def get_pool() -> Pool:
    if db_pool is None:
        raise RuntimeError("DB pool is not initialized")
    return db_pool

async def close_db():
    """Закрыть пул соединений"""
    global db_pool
    if db_pool:
        await db_pool.close()

# ------------------ AGENTS ------------------

async def add_agent(telegram_id: int, username: str | None, full_name: str,
                    phone_number: str, city: str | None, organization: str | None,
                    position: str | None, privacy: bool, marketing: bool):
    """Добавить или обновить агента"""
    async with db_pool.acquire() as conn:
        await conn.execute("""
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
        """, telegram_id, username, full_name, phone_number, city, organization, position, privacy, marketing)

async def get_agents():
    """Получить всех агентов"""
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM agents ORDER BY created DESC")
        return rows

# ------------------ CUSTOMERS ------------------

async def add_customer(agent_id: int, full_name: str, phone_number: str, center: str | None):
    """Добавить пациента (customer)"""
    async with db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO customers (
                agent_id, full_name, phone_number, center, created
            )
            VALUES ($1,$2,$3,$4,NOW())
        """, agent_id, full_name, phone_number, center)

async def get_customers():
    """Получить всех пациентов"""
    async with db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM customers ORDER BY created DESC")
        return rows