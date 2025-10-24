from Handlers.handlers import Handler
from Requests.requests import sendMessage
class MessageEcho(Handler):

    def can_handle(self,update) ->bool:
        return "message" in update and "text" in update["message"]

    def handle(self,update) -> bool:
        sendMessage(
            chat_id = update["message"]["chat"]["id"],
            text = update["message"]["text"]
        )
        return False