import json
from Handlers.Handlers import Handler
from database.database import getUser
class Dispatcher:
    def __init__(self):
        self._handlers: list[Handler] = []
        
    def add_handlers(self,*handlers: Handler):
        for handler in handlers:
            self._handlers.append(handler)


    def _get_telegram_id_from_update(self, update: dict) -> int:
        if "message" in update:
            return update["message"]["from"]["id"]
        elif "callback_query" in update:
            return update["callback_query"]["from"]["id"]
        return None

    def dispatch(self,update):
        
        telegram_id = self._get_telegram_id_from_update(update)
        user = getUser(telegram_id)
        user_state = None
        user_order = None
        
        if user:
            user_state = user["state"]
            if (user["_order"]):
                user_order = json.loads(user["_order"])

        for handler in self._handlers:
            if handler.can_handle(update,user_state,user_order):
                signal = handler.handle(update,user_state,user_order)
                if not signal:
                    break