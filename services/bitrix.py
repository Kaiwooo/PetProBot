import aiohttp
from decouple import config
from utils.split_full_name import split_full_name

CATEGORY_ID_AGENTS = config("CATEGORY_ID_AGENTS", cast=int)
CATEGORY_ID_PATIENTS = config("CATEGORY_ID_PATIENTS", cast=int)

class BitrixClient:
    def __init__(self, base_url: str | None = None, timeout: int = 15):
        self.base_url = base_url or config("BITRIX_WEBHOOK_URL")
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def post(self, path: str, payload: dict):
        url = f"{self.base_url}/{path}.json"
        async with self.session.post(url, json=payload) as resp:
            data = await resp.json()
            if resp.status != 200 or "error" in data:
                raise RuntimeError(f"Bitrix API error {resp.status}: {data.get('error_description', data)}")
            return data.get("result")

async def create_contact(full_name: str, phone: str, city: str, telegram_username: str | None = None):
    last_name, first_name, second_name = split_full_name(full_name)
    payload = {
        "fields": {
            "NAME": first_name,
            "LAST_NAME": last_name,
            "SECOND_NAME": second_name,
            "TYPE_ID": "PARTNER",
            "SOURCE_ID": 1,
            "PHONE": [{"VALUE": phone, "VALUE_TYPE": "MOBILE"}] if phone else [],
            "ADDRESS_CITY": city,
            "IM": [{"VALUE": telegram_username, "VALUE_TYPE": "TELEGRAM"}] if telegram_username else [],
        }
    }
    async with BitrixClient() as bitrix:
        return await bitrix.post("crm.contact.add", payload)

async def update_contact(contact_id: int, email: str, position: str, company_id: int):
    payload = {
        "ID": contact_id,
        "fields": {
            "EMAIL": [{"VALUE": email, "VALUE_TYPE": "WORK"}],
            "COMPANY_ID": company_id,
            "POST": position
        }
    }
    async with BitrixClient() as bitrix:
        return await bitrix.post("crm.contact.update", payload)

async def create_company(title: str):
    payload = {"fields":
                   {"TITLE": title}
               }
    async with BitrixClient() as bitrix:
        return await bitrix.post("crm.company.add", payload)

async def create_deal_agents(full_name: str, contact_id: int) -> int | None:
    payload = {
        "fields": {
            "CATEGORY_ID": CATEGORY_ID_AGENTS,
            "TITLE": f"Регистрация {full_name}",
            "STAGE_ID": "NEW",
            "CONTACT_ID": contact_id,
            "SOURCE_ID": 1
        }
    }
    async with BitrixClient() as bitrix:
        return await bitrix.post("crm.deal.add", payload)

async def create_deal_patient(full_name: str, phone_number: str, contact_id: int) -> int:
    payload = {
        "fields": {
            "CATEGORY_ID": CATEGORY_ID_PATIENTS,
            "TITLE": f"{full_name} {phone_number}",
            "CONTACT_ID": contact_id,
            "SOURCE_ID": 1
        }
    }
    async with BitrixClient() as bitrix:
        return await bitrix.post("crm.deal.add", payload)

async def change_deal_stage(deal_id: int, next_stage: str):
    if not deal_id or not next_stage:
        return None
    payload = {"id": deal_id, "fields": {"STAGE_ID": next_stage}}
    async with BitrixClient() as bitrix:
        return await bitrix.post("crm.deal.update", payload)