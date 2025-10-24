import json

from Handlers.Handlers import Handler,HandlerStatus
from database.database import updateUserOrder,updateUserState,getUser
from Requests.requests import answerCallbackQuery,deleteMessage,sendMessage
from Handlers.WaitForPizzaName import answerAnotherOrder

def count_money(user) -> float:
    user_order = json.loads(user["_order"])
    pizza = user_order["pizza_name"]  # "pizza pepperoni" (с пробелом)
    size = user_order["pizza_size"]   # "Large (35cm)" (значение)
    drink = user_order["drink_name"]  # "Coca Cola" (значение)
    
    # Цены на пиццы (используем названия с пробелами)
    pizza_prices = {
        "pizza margherita": 12.0,
        "pizza pepperoni": 15.0,
        "pizza quattro stagioni": 18.0,
        "pizza capricciosa": 16.0,
        "pizza diavola": 17.0,
        "pizza prosciutto": 14.0
    }
    
    # Цены на размеры (по значениям из size_mapping)
    size_prices = {
        "Small (25cm)": 0.7,    # множитель
        "Medium (30cm)": 1.0,   # базовая цена
        "Large (35cm)": 1.3,    # множитель
        "Extra Large (40cm)": 1.6  # множитель
    }
    
    # Цены на напитки (по значениям из drink_mapping)
    drink_prices = {
        "Coca Cola": 3.0,
        "Pepsi": 2.8,
        "Orange Juice": 4.0,
        "Apple Juice": 4.0,
        "Water": 1.5,
        "Iced Tea": 3.5,
        "No Drinks": 0.0
    }
    
    # Расчет стоимости
    base_pizza_price = pizza_prices.get(pizza, 15.0)  # цена по умолчанию
    size_multiplier = size_prices.get(size, 1.0)      # множитель по умолчанию
    drink_price = drink_prices.get(drink, 0.0)        # цена напитка
    
    pizza_price = base_pizza_price * size_multiplier
    total_price = pizza_price + drink_price
    
    return round(total_price, 2)






class WaitForDrinks(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_DRINKS":
            if state == "WAIT_FOR_PIZZA_NAME" or state == "WAIT_FOR_PIZZA_SIZE" or state == "WAIT_FOR_ACCEPT" or state == "rebuild":
                answerAnotherOrder(update)
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]


        drink_mapping = {
            "drink_coca_cola": "Coca Cola",
            "drink_pepsi": "Pepsi",
            "drink_orange_juice": "Orange Juice",
            "drink_apple_juice": "Apple Juice",
            "drink_water": "Water",
            "drink_iced_tea": "Iced Tea",
            "drink_none": "No Drinks",
        }

        data["drink_name"] = drink_mapping.get(callback_data)
        updateUserOrder(telegram_id,data)
        updateUserState(telegram_id, "WAIT_FOR_ACCEPT")
        answerCallbackQuery(update["callback_query"]["id"])
        deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )
        
        user = getUser(telegram_id)
        user_order = json.loads(user["_order"])
        print(user_order)
        pizza = user_order["pizza_name"]
        size = user_order["pizza_size"]
        drink = user_order["drink_name"]
        cost = count_money(user)
        sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text=f"""Your Pizza order:\n
            Pizza: {pizza}\n
            Size: {size}\n
            Drinks: {drink}
            """,
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": f"Accept and Pay {cost}$", "callback_data": "accept"},
                            
                        ],
                        [
                            {"text": "Rebuild", "callback_data": "rebuild"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP