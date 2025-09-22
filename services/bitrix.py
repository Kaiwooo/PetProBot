import aiohttp
import logging
from decouple import config
from utils.split_full_name import split_full_name

logger = logging.getLogger(__name__)

async def _post_json(path: str, payload: dict):
    url = f"{config("BITRIX_WEBHOOK_URL")}/{path}.json"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            data = await resp.json()
            if resp.status != 200 or 'error' in data:
                logger.error("Bitrix API error: %s %s", resp.status, data)
                raise RuntimeError(f"Bitrix error: {data}")
            return data.get('result')

async def create_contact(full_name: str, phone: str | None, city: str | None, telegram_username: str | None = None) -> int | None:
    last_name, first_name, second_name = split_full_name(full_name)
    fields = {
        "NAME": first_name,
        "LAST_NAME": last_name,
        "SECOND_NAME": second_name,
        "TYPE_ID": "PARTNER",
        "SOURCE_ID": "1|TELEGRAM",
        "PHONE": [{"VALUE": phone, "VALUE_TYPE": "MOBILE"}],
        "ADDRESS_CITY": city,
        "IM": [{"VALUE": telegram_username, "VALUE_TYPE": "TELEGRAM"}] if telegram_username else []
    }
    payload = {"fields": fields}
    result = await _post_json("crm.contact.add", payload)
    try:
        return int(result)
    except (TypeError, ValueError):
        return None

async def create_deal(full_name: str, contact_id: int) -> int | None:
    payload = {
        "fields": {
            "TITLE": f"Регистрация через Pet Pro Bot {full_name}",
            "STAGE_ID": "NEW",
            "CATEGORY_ID": 0,
            "CONTACT_ID": contact_id,
        }
    }
    result = await _post_json("crm.deal.add", payload)
    try:
        return int(result)
    except (TypeError, ValueError):
        return None

async def create_contact_and_deal(full_name: str, phone: str | None, city: str | None, telegram_username: str | None = None):
    contact_id = await create_contact(full_name, phone, city, telegram_username)
    deal_id = None
    if contact_id:
        deal_id = await create_deal(full_name, contact_id)
    return contact_id, deal_id

# Найти контакт по телефону
async def find_contact_by_phone(phone: str):
    result = await _post_json("crm.contact.list", {
        "filter": {"PHONE": phone},
        "select": ["ID"]
    })
    if result:
        return int(result[0]["ID"])
    return None

# Найти сделку по CONTACT_ID
async def find_deal_by_contact(contact_id: int):
    result = await _post_json("crm.deal.list", {
        "filter": {"CONTACT_ID": contact_id},
        "select": ["ID", "STAGE_ID"]
    })
    if result:
        return int(result[0]["ID"])
    return None

# Обновить контакт
async def update_contact(contact_id: int, fields: dict):
    return await _post_json("crm.contact.update", {"id": contact_id, "fields": fields})

# Перевести сделку на следующую стадию
async def advance_deal_stage(deal_id: int, next_stage: str):
    return await _post_json("crm.deal.update", {"id": deal_id, "fields": {"STAGE_ID": next_stage}})

# Создать компанию в битрикс
async def create_company(title: str, telegram_id: int | None = None, city: str | None = None):
    fields = {"TITLE": title}
    payload = {"fields": fields}
    result = await _post_json("crm.company.add", payload)
    try:
        return int(result)
    except Exception:
        return None