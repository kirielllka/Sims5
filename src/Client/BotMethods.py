import os

import requests
from dotenv import load_dotenv

load_dotenv()


class Bot:
    url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/"

    @classmethod
    def send_message(cls, text: str, chat_id: int, keyboard: dict = None):
        if keyboard:
            json = {"chat_id": chat_id, "text": text, "reply_markup": keyboard}
        else:
            json = {"chat_id": chat_id, "text": text}

        request = requests.post(url=cls.url + "sendMessage", json=json)

        if request.status_code == 200:
            json_result = request.json()
            return {"status": 200, "data": json_result}
        else:
            return f"Ошибка:{request.status_code}"

    @classmethod
    def edit_message(
        cls, text: str, chat_id: int, message_id: int, keyboard: dict = None
    ):
        request = requests.post(
            url=cls.url + "editMessageText",
            json={
                "chat_id": chat_id,
                "text": text,
                "reply_markup": keyboard,
                "message_id": message_id,
            },
        )
        if request.status_code == 200:
            json_result = request.json()
            return {"status": 200, "data": json_result}
        else:
            return f"Ошибка:{request.status_code}"

    @classmethod
    def get_updates(cls, offset=None):
        if offset:
            request = requests.get(
                url=cls.url + "getUpdates", params={"offset": offset}
            )
        else:
            request = requests.get(url=cls.url + "getUpdates")

        if request.status_code == 200:
            return request.json()
        else:
            return f"Ошибка:{request.status_code}"

    @classmethod
    def send_photo(cls, chat_id, media):
        request = requests.post(
            url=cls.url + f"sendPhoto?chat_id={chat_id}",
            files={"photo": open(media, "rb")},
        )

        if request.status_code == 200:
            return request.json()
        else:
            return f"Ошибка:{request.status_code}"

    @classmethod
    def send_document(cls, chat_id, doc):
        request = requests.post(
            url=cls.url + f"sendDocument?chat_id={chat_id}",
            files={"document": open(doc, "rb")},
        )
        if request.status_code == 200:
            return request.json()
        else:
            return f"Ошибка:{request.status_code}"
