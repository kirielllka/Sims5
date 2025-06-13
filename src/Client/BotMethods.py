import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()


class Bot:
    base_url = f"https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/"
    session = None

    @classmethod
    async def get_session(cls):
        if cls.session is None or cls.session.closed:
            cls.session = aiohttp.ClientSession()
        return cls.session

    @classmethod
    async def close_session(cls):
        if cls.session and not cls.session.closed:
            await cls.session.close()

    @classmethod
    async def make_request(cls, method: str, **params):
        session = await cls.get_session()
        try:
            async with session.post(cls.base_url + method, json=params) as response:
                if response.status == 200:
                    return await response.json()
                return f"Ошибка: {response.status}"
        except aiohttp.ClientError as e:
            return f"Ошибка соединения: {str(e)}"

    @classmethod
    async def send_message(cls, text: str, chat_id: int, keyboard: dict = None):
        params = {"chat_id": chat_id, "text": text}
        if keyboard:
            params["reply_markup"] = keyboard
        return await cls.make_request("sendMessage", **params)

    @classmethod
    async def edit_message(
            cls, text: str, chat_id: int, message_id: int, keyboard: dict = None
    ):
        params = {
            "chat_id": chat_id,
            "text": text,
            "message_id": message_id,
        }
        if keyboard:
            params["reply_markup"] = keyboard
        return await cls.make_request("editMessageText", **params)

    @classmethod
    async def get_updates(cls, offset=None):
        session = await cls.get_session()
        params = {"offset": offset} if offset else {}
        try:
            async with session.get(cls.base_url + "getUpdates", params=params) as response:
                if response.status == 200:
                    return await response.json()
                return f"Ошибка: {response.status}"
        except aiohttp.ClientError as e:
            return f"Ошибка соединения: {str(e)}"

    @classmethod
    async def send_photo(cls, chat_id: int, file_path: str):
        session = await cls.get_session()
        try:
            with open(file_path, 'rb') as file:
                form_data = aiohttp.FormData()
                form_data.add_field('photo', file, filename=os.path.basename(file_path))

                async with session.post(
                        cls.base_url + "sendPhoto",
                        data=form_data,
                        params={"chat_id": chat_id}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return f"Ошибка: {response.status}"
        except (IOError, aiohttp.ClientError) as e:
            return f"Ошибка: {str(e)}"

    @classmethod
    async def send_document(cls, chat_id: int, file_path: str):
        session = await cls.get_session()
        try:
            with open(file_path, 'rb') as file:
                form_data = aiohttp.FormData()
                form_data.add_field('document', file, filename=os.path.basename(file_path))

                async with session.post(
                        cls.base_url + "sendDocument",
                        data=form_data,
                        params={"chat_id": chat_id}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
        except Exception:
            return None