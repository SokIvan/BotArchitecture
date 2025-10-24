import json
from Commands.TextCommand import TextCommand
from Requests.requests import sendMessage
from database.database import getUser

class StatusCommand(TextCommand):

    def is_command(self,update,state) -> bool:
        return update["message"]["text"] == "/status"
    

    def command(self,update,state) -> None:
        """Отправляет статистику пользователя"""
        user = getUser(update["message"]["from"]["id"])
        
        if not user:
            # Если пользователь не найден в базе
            sendMessage(
                chat_id=update["message"]["chat"]["id"],
                text="❌ Вы еще не начинали заказы. Используйте /start чтобы начать!"
            )
            return
        
        # Форматируем дату регистрации
        created_date = user['created_at'].split()[0] if user['created_at'] else "неизвестно"
        
        # Получаем статистику (если None, то 0)
        count = user['count'] or 0
        money_waste = user['money_waste'] or 0.0
        
        status_text = f"""
    📊 *Ваша статистика*

    🍕 Заказано пицц: *{count}*
    💰 Потрачено денег: *${money_waste:.2f}*
    📅 С нами с: *{created_date}*

    Спасибо, что выбираете нас! ❤️
    """
        
        sendMessage(
            chat_id=update["message"]["chat"]["id"],
            text=status_text,
            parse_mode="Markdown"
        )