import json
from Commands.TextCommand import TextCommand
from Requests.requests import sendMessage
class HelpCommand(TextCommand):

    def is_command(self,update,state) -> bool:
        return update["message"]["text"] == "/help"
    

    def command(self,update,state) -> None:
        help_text = """
                🍕 *Пицца-бот: Инструкция*

                Доступные команды:

                /start - Начать новый заказ
                _Запускает процесс оформления заказа пиццы_

                /status - Статус и статистика
                _Показывает вашу статистику заказов_

                /help - Помощь
                _Показывает это сообщение_

                /clearAndStart - Начать новый заказ
                _В отличие от /start можно запускать вне зависимости от того есть ли сейчас заказ_
                *Как пользоваться:*
                1. Нажмите /start чтобы начать заказ
                2. Выберите пиццу, размер и напиток
                3. Подтвердите заказ

                Приятного аппетита! 🍕
                """
    
        sendMessage(
            chat_id=update["message"]["chat"]["id"],
            text=help_text,
            parse_mode="Markdown"
        )