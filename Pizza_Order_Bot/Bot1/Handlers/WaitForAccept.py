import json

from Handlers.Handlers import Handler,HandlerStatus
from database.database import updateUserOrder,updateUserState,getUser,clearUserOrder,updateUserStatus
from Requests.requests import answerCallbackQuery,deleteMessage,sendMessage

from Handlers.WaitForDrinks import count_money
from Commands import StartCommand
from Handlers.WaitForPizzaName import answerAnotherOrder




class WaitForAccept(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_ACCEPT":
            if state == "WAIT_FOR_PIZZA_NAME" or state == "WAIT_FOR_PIZZA_SIZE" or state == "WAIT_FOR_DRINKS" or state == "rebuild":
                answerAnotherOrder(update)
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data == "accept" or callback_data == "rebuild"

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]
        
        if callback_data == "accept":
            user = getUser(telegram_id)
            cost = count_money(user)
            
            updateUserStatus(telegram_id,cost)
            #clearUserOrder(telegram_id) #заказ должен быть оставлен в базе данных для дальнейшего применения
            updateUserState(telegram_id,"NULL")
            sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text = "Thanks for order!"
        )
        answerCallbackQuery(update["callback_query"]["id"])
        deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )        
        
        if callback_data == "rebuild":
            cOmmand = StartCommand.StartCommand()
            cOmmand.command(update,state) #😎 no copypasta
        
        
        
        return HandlerStatus.STOP