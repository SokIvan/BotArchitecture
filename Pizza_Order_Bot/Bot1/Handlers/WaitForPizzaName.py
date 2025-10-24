import json

from Handlers.Handlers import Handler,HandlerStatus
from database.database import updateUserOrder,updateUserState
from Requests.requests import answerCallbackQuery,deleteMessage,sendMessage

def answerAnotherOrder(update):
    
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
    elif "callback_query" in update:
        chat_id = update["callback_query"]["message"]["chat"]["id"]
    if False: #работает, но не совсем правильно
        sendMessage(
            chat_id=chat_id,
                text="You have another order!",
        )

class WaitForPizzaName(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_PIZZA_NAME":
            if state == "WAIT_FOR_PIZZA_SIZE" or state == "WAIT_FOR_DRINKS" or state == "WAIT_FOR_ACCEPT" or state == "rebuild":
                answerAnotherOrder(update)
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("pizza_")

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        pizza_name = callback_data.replace("pizza_", "").replace("_", " ").title()
        updateUserOrder(telegram_id, {"pizza_name": pizza_name})
        updateUserState(telegram_id, "WAIT_FOR_PIZZA_SIZE")
        answerCallbackQuery(update["callback_query"]["id"])
        deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )
        sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="Please select pizza size",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Small (25cm)", "callback_data": "size_small"},
                            {"text": "Medium (30cm)", "callback_data": "size_medium"},
                        ],
                        [
                            {"text": "Large (35cm)", "callback_data": "size_large"},
                            {"text": "Extra Large (40cm)", "callback_data": "size_xl"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP