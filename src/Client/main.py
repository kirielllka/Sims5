from BotMethods import Bot

update_id = None

while True:
    updates = Bot.get_updates(offset=(update_id + 1) if update_id is not None else None)

    if updates['result']:
        for update in updates['result']:
            update_id = update['update_id']

            message_text = update['message']['text']
            chat_id = update['message']['chat']['id']

            print(message_text)

            if message_text == '/start':
                Bot.send_message(
                    chat_id=chat_id,
                    text='Привет это симс5, сейчас вы можете создать человека, заставить их всех повзрослеть и скрестить их'
                )
    else:
        import time
        time.sleep(1)