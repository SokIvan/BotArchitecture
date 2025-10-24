from Handlers.Handlers import Handler,HandlerStatus
from Requests.requests import sendMessage
class MessageEcho(Handler):

    def can_handle(self,update,state:str,order:dict) ->bool:
        return "message" in update and "text" in update["message"]

    def handle(self,update,state:str,order:dict) -> HandlerStatus:
        sendMessage(
            chat_id = update["message"]["chat"]["id"],
            text = update["message"]["text"]
        )
        return HandlerStatus.STOP