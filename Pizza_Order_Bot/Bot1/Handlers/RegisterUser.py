from Handlers.Handlers import Handler,HandlerStatus
from database.database import ensure_user_exists


class RegisterUser(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        return "message" in update and "from" in update["message"]

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]
        ensure_user_exists(telegram_id)
        return HandlerStatus.CONTINUE