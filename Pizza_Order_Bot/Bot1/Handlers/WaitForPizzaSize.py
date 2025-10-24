import json

from Handlers.Handlers import Handler,HandlerStatus
from database.database import updateUserOrder, updateUserState
from Requests.requests import sendMessage, answerCallbackQuery, deleteMessage
from Handlers.WaitForPizzaName import answerAnotherOrder

class WaitForPizzaSize(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_PIZZA_SIZE":
            if state == "WAIT_FOR_PIZZA_NAME" or state == "WAIT_FOR_DRINKS" or state == "WAIT_FOR_ACCEPT" or state == "rebuild":
                answerAnotherOrder(update)
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("size_")

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        size_mapping = {
            "size_small": "Small (25cm)",
            "size_medium": "Medium (30cm)",
            "size_large": "Large (35cm)",
            "size_xl": "Extra Large (40cm)",
        }

        pizza_size = size_mapping.get(callback_data)
        data["pizza_size"] = pizza_size
        updateUserOrder(telegram_id, data)
        updateUserState(telegram_id, "WAIT_FOR_DRINKS")

        answerCallbackQuery(update["callback_query"]["id"])

        deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="Please choose some drinks",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Coca-Cola", "callback_data": "drink_coca_cola"},
                            {"text": "Pepsi", "callback_data": "drink_pepsi"},
                        ],
                        [
                            {
                                "text": "Orange Juice",
                                "callback_data": "drink_orange_juice",
                            },
                            {
                                "text": "Apple Juice",
                                "callback_data": "drink_apple_juice",
                            },
                        ],
                        [
                            {"text": "Water", "callback_data": "drink_water"},
                            {"text": "Iced Tea", "callback_data": "drink_iced_tea"},
                        ],
                        [
                            {"text": "No drinks", "callback_data": "drink_none"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP