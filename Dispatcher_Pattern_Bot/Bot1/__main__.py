import time

from Handlers import database_update, message_echo
from dispatcher.dispatcher import Dispatcher

import database.database as telegramDatabase
from long_polling import start_long_polling
from Handlers import message_photo_echo, command

RECREATE_BOOL = False

def main() -> None:
    dispatcher = Dispatcher()
    
    dispatcher.add_handlers(
        database_update.DatabaseUpdate(),
        command.Command(),
        message_echo.MessageEcho(),#Важный момент эхо вызывается перед фото. Если пользователь отправит фото с текстом, бот вернет только текст
        message_photo_echo.message_photo_echo())
    start_long_polling(dispatcher)

if __name__ == "__main__":
    main()