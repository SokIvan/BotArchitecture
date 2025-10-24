import json
import os
from urllib import request

from dotenv import load_dotenv

load_dotenv()

def makePostRequest(method:str,**param) -> dict:
    json_data = json.dumps(param).encode("utf-8")
    makerequest = request.Request(
        method="POST",
        url=f"{os.getenv("TELEGRAM_API_URL")}/{method}",
        data=json_data,
        headers={"Content-Type": "application/json"}
    )
    
    with request.urlopen(makerequest) as response:
        response_body = response.read().decode("utf-8")
        response_json = json.loads(response_body)
        assert response_json["ok"] == True
        return response_json["result"]
    
def getUpdates(**param) -> dict:
    return makePostRequest("getUpdates",**param)

def sendMessage(**param) -> dict:
    return makePostRequest("sendMessage",**param)

def getMe(**param) -> dict:
    return makePostRequest("getMe",**param)

def sendPhoto(**param) -> dict:
    return makePostRequest("sendPhoto",**param)

def answerCallbackQuery(callback_query_id: str, **kwargs) -> dict:
    return makePostRequest("answerCallbackQuery", callback_query_id=callback_query_id, **kwargs)

def deleteMessage(chat_id: int, message_id: int) -> dict:
    return makePostRequest("deleteMessage", chat_id=chat_id, message_id=message_id)