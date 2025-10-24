import time
from dispatcher.dispatcher import Dispatcher

from Requests.requests import getUpdates


def start_long_polling(dispatcher:Dispatcher) -> None:

    next_update_offset = 0
    while True:
        updates = getUpdates(offset = next_update_offset)
        for update in updates:

            next_update_offset = max(next_update_offset,update["update_id"]+1)
            dispatcher.dispatch(update)
        time.sleep(1)
