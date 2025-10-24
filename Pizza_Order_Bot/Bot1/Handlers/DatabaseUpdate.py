from Handlers.Handlers import Handler,HandlerStatus
from database.database import persist_updates

class DatabaseUpdate(Handler):

    def can_handle(self,update:list,state:str,order:dict) ->bool:
        return update!=None and len(update)!=0

    def handle(self,update,state:str,order:dict) -> HandlerStatus:
        persist_updates(update)
        return HandlerStatus.CONTINUE