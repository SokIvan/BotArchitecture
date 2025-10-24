from Handlers.handlers import Handler
from Requests.requests import sendMessage

class Command(Handler):
    """Проверяет сообщение на отправку определенного текстового сообщения(пока не реализовано)"""
    def can_handle(self,update) ->bool:
        return False # позже доделаю

    def handle(self,update) -> bool:
        pass