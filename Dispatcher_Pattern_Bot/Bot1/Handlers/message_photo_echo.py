from Handlers.handlers import Handler
from Requests.requests import sendPhoto


class message_photo_echo(Handler):

    def can_handle(self,update) ->bool:
        return "message" in update and "photo" in update["message"]

    def handle(self,update) -> bool:
        
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
        return False