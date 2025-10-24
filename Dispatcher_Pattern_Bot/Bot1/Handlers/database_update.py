from Handlers.handlers import Handler
from database.database import persist_updates

class DatabaseUpdate(Handler):

    def can_handle(self,update:list) ->bool:
        assert update!=None and len(update)!=0

    def handle(self,update) -> bool:
        persist_updates(update)
        return True