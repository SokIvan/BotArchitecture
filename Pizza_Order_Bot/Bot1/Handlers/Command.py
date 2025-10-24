from typing import List
from Handlers.Handlers import Handler,HandlerStatus
from Requests.requests import sendMessage
from Commands.TextCommand import TextCommand
class Command(Handler):
    """Проверяет сообщение на отправку определенного текстового сообщения"""
    
    def __init__(self,commands:list[TextCommand] = None):
        self.commands = commands
    
    def can_handle(self,update,state:str,order:dict) ->bool:
        return "message" in update and "text" in update["message"] and update["message"]["text"].startswith("/")

    def handle(self,update,state:str,order:dict) -> HandlerStatus:
        for command in self.commands:
            if command.is_command(update,state):
                command.command(update,state)

                return HandlerStatus.STOP
        return HandlerStatus.CONTINUE