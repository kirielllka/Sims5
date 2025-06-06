import os
from dotenv import load_dotenv
import requests
load_dotenv()
#https://api.telegram.org/bot7866649635:AAHnE1DsrSn6yy9XlbQgtG-NfYYvEZ_a1Zk/getUpdates

class Bot:
    url = f'https://api.telegram.org/bot{os.getenv('BOT_TOKEN')}/'

    @classmethod
    def send_message(cls, text:str, chat_id:int):
        request = requests.get(url=cls.url+'sendMessage', params={'chat_id':chat_id,'text':text})
        if request.status_code == 200:
            json_result = request.json()
            return {'status':200,'data':json_result}
        else:
            return f'Ошибка:{request.status_code}'

    @classmethod
    def get_updates(cls,offset=None):
        if offset:
            request = requests.get(url=cls.url+'getUpdates',params={'offset':offset})
        else:
            request = requests.get(url=cls.url+'getUpdates')
        if request.status_code == 200:
            return request.json()
        else:
            return f'Ошибка:{request.status_code}'
