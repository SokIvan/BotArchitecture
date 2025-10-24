import json
from Commands.TextCommand import TextCommand
from database.database import clearUserOrder,updateUserState
from Requests.requests import sendMessage
from Commands.StartCommand import StartCommand

class clearOrderAndStart(TextCommand):

    def is_command(self,update,state) -> bool:
        return (update["message"]["text"] == "/clearAndStart")

    

    def command(self,update,state) -> None:
            cOmmand = StartCommand()
            cOmmand.command(update,state)