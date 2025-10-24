import os
import time

from dispatcher.dispatcher import Dispatcher

import database.database as telegramDatabase
from long_polling import start_long_polling
from Handlers import DatabaseUpdate, MessageEcho,message_photo_echo, Command,RegisterUser, WaitForPizzaSize,WaitForPizzaName,WaitForDrinks,WaitForAccept
from Commands import StartCommand,HelpCommand, StatusCommand, clearOrderAndStart



RECREATE_BOOL = False

def main() -> None:
    table_names = ["telegram_updates","users"]

    if not telegramDatabase.all_tables_exists(table_names):
        telegramDatabase.recreate_db()
        print("✅Нужные таблицы добавлены.")
            
    commands = [
        StartCommand.StartCommand(),
        HelpCommand.HelpCommand(),
        StatusCommand.StatusCommand(),
        clearOrderAndStart.clearOrderAndStart(),
        ]
    print("✅Нужные команды зарегистрированы.")
    
    dispatcher = Dispatcher()
    
    dispatcher.add_handlers(
        DatabaseUpdate.DatabaseUpdate(),
        RegisterUser.RegisterUser(),
        Command.Command(commands),
        
        WaitForAccept.WaitForAccept(),
        WaitForDrinks.WaitForDrinks(),
        WaitForPizzaSize.WaitForPizzaSize(),
        WaitForPizzaName.WaitForPizzaName(),
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #MessageEcho.MessageEcho(),
        #message_photo_echo.message_photo_echo()
        )
    print("✅Нужные хендлеры добавлены в диспетчер.")
    print("Запуск бота.")
    start_long_polling(dispatcher)

if __name__ == "__main__":
    main()