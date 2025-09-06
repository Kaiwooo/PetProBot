import json

class FSMStateInspector:
    def __init__(self, redis_client):
        self.r = redis_client

    def get_states_by_pattern(self, pattern: str):
        # Получить состояния по шаблону
        result = {}
        for key in self.r.scan_iter("fsm:*:state"):
            value = self.r.get(key)
            if value and pattern in value:
                result[key] = value
        return result

    def get_user_data(self, key: str):
        # Получить данные пользователя по ключу состояния
        parts = key.split(":")
        if len(parts) >= 4:
            chat_id = parts[1]
            user_id = parts[2]
            data_key = f"fsm:{chat_id}:{user_id}:data"
            data = self.r.get(data_key)
            if data:
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    return {"raw_data": data}
        return {}