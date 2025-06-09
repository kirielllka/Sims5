from BotMethods import Bot
from Keyboards import start_keyboard
from GameMethods import show_people,child,run_simulation
update_id = None


while True:
    updates = Bot.get_updates(offset=(update_id + 1) if update_id is not None else None)

    if updates['result']:
        for update in updates['result']:
            update_id = update['update_id']
            try:
                if update['callback_query']['data']:
                    show_people(chat_id=update['callback_query']['message']['chat']['id'],page=int(update['callback_query']['data'][-1]),edit=True,message_id=int(update['callback_query']['message']['message_id']))

            except Exception:
                message_text = update['message']['text']
                chat_id = update['message']['chat']['id']

                print(message_text)

                if message_text == '/start':
                    Bot.send_message(
                        chat_id=chat_id,
                        text='Привет это симс5, сейчас вы можете создать человека, заставить их всех повзрослеть и скрестить их',
                        keyboard=start_keyboard
                    )
                if message_text == 'Показать всех людей':
                    show_people(chat_id=chat_id)
                if message_text == 'Скрестить случайную пару':
                    child()
                if message_text == 'Симулировать 1 год':run_simulation(1*12);Bot.send_message(chat_id=chat_id,text='Симуляция завершена')
                if message_text == 'Симулировать 5 лет':run_simulation(5*12);Bot.send_message(chat_id=chat_id,text='Симуляция завершена')
                if message_text == 'Симулировать 1 месяц':run_simulation(1);Bot.send_message(chat_id=chat_id,text='Симуляция завершена')
    else:
        import time
        time.sleep(1)