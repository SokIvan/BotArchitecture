import json
from Commands.TextCommand import TextCommand
from database.database import clearUserOrder,updateUserState
from Requests.requests import sendMessage
from Handlers.WaitForPizzaName import answerAnotherOrder

class StartCommand(TextCommand):

    def is_command(self,update,state) -> bool:
        if (update["message"]["text"] == "/start" and (state == "NULL" or state == None or state == "rebuild")):
            return True
        else:
            if state == "WAIT_FOR_PIZZA_NAME" or state == "WAIT_FOR_PIZZA_SIZE" or state == "WAIT_FOR_ACCEPT" or state == "WAIT_FOR_DRINKS":
                answerAnotherOrder(update)
            return False

    

    def command(self,update,state) -> None:
        if "message" in update:
            telegram_id = update["message"]["from"]["id"]
            chat_id = update["message"]["chat"]["id"]
        elif "callback_query" in update:
            telegram_id = update["callback_query"]["from"]["id"]
            chat_id = update["callback_query"]["message"]["chat"]["id"]
        clearUserOrder(telegram_id)
        updateUserState(telegram_id, "WAIT_FOR_PIZZA_NAME")

        sendMessage(
            chat_id=chat_id,
            text="🍕 Welcome to Pizza shop!",
            reply_markup=json.dumps({"remove_keyboard": True}),
        )

        sendMessage(
            chat_id=chat_id,
            text="Please choose pizza type",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Margherita", "callback_data": "pizza_margherita"},
                            {"text": "Pepperoni", "callback_data": "pizza_pepperoni"},
                        ],
                        [
                            {
                                "text": "Quattro Stagioni",
                                "callback_data": "pizza_quattro_stagioni",
                            },
                            {
                                "text": "Capricciosa",
                                "callback_data": "pizza_capricciosa",
                            },
                        ],
                        [
                            {"text": "Diavola", "callback_data": "pizza_diavola"},
                            {"text": "Prosciutto", "callback_data": "pizza_prosciutto"},
                        ],
                    ],
                },
            ),
        )