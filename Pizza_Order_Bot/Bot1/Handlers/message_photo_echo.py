from Handlers.Handlers import Handler,HandlerStatus
from Requests.requests import sendPhoto


class message_photo_echo(Handler):

    def can_handle(self,update,state:str,order:dict) ->bool:
        return "message" in update and "photo" in update["message"]

    def handle(self,update,state:str,order:dict) -> HandlerStatus:
        
        if "caption" in update["message"]:
            caption = update["message"]["caption"]
            sendPhoto(
            chat_id = update["message"]["chat"]["id"],
            photo = update["message"]["photo"][-1]["file_id"],#вроде как
            caption = caption
        )
        else:
            sendPhoto(
                chat_id = update["message"]["chat"]["id"],
                photo = update["message"]["photo"][-1]["file_id"],#вроде как
            )
        return HandlerStatus.STOP