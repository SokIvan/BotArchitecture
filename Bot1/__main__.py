import time
import Bot1.requests.requests as telegramRequests
import Bot1.database.database as telegramDatabase

RECREATE_BOOL = False

def main() -> None:
    
    if RECREATE_BOOL:
        telegramDatabase.recreate_db()
    
    try:
        next_update_offset = 0
        while True:
            updates = telegramRequests.getUpdates(offset = next_update_offset)
            telegramDatabase.persist_updates(updates)
            for update in updates:
                if "message" in update and "text" in update["message"]:
                    telegramRequests.sendMessage(
                        chat_id = update["message"]["chat"]["id"],
                        text = update["message"]["text"]
                    )
                    next_update_offset = max(next_update_offset,update["update_id"]+1)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBye!")

if __name__ == "__main__":
    main()