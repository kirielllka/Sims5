import asyncio
import os

from BotMethods import Bot
from Keyboards import start_keyboard
from GameMethods import show_people, run_simulation, reset, choose_pair
from src.StatPlots import StatPlot


async def main():
    update_id = None
    while True:
        updates = await Bot.get_updates(
            offset=(update_id + 1) if update_id is not None else None
        )

        if updates["result"]:
            for update in updates["result"]:
                update_id = update["update_id"]
                try:
                    if update["callback_query"]["data"]:
                        await show_people(
                            chat_id=update["callback_query"]["message"]["chat"]["id"],
                            page=int(update["callback_query"]["data"][-1]),
                            edit=True,
                            message_id=int(
                                update["callback_query"]["message"]["message_id"]
                            ),
                        )

                except Exception:
                    message_text = update["message"]["text"]
                    chat_id = update["message"]["chat"]["id"]

                    print(message_text)

                    if message_text == "/start":
                        await Bot.send_message(
                            chat_id=chat_id,
                            text="Привет это симс5, сейчас вы можете создать человека,"
                            " заставить их всех повзрослеть и скрестить их",
                            keyboard=start_keyboard,
                        )
                    if message_text == "Показать всех людей":
                        await show_people(chat_id=chat_id)

                    if message_text == "Скрестить случайную пару":
                        choose_pair()

                    if message_text == "Симулировать 1 год":
                        run_simulation(1)
                        await Bot.send_message(chat_id=chat_id, text="Симуляция завершена")

                    if message_text == "Симулировать 5 лет":
                        run_simulation(5)
                        await Bot.send_message(chat_id=chat_id, text="Симуляция завершена")

                    if message_text == "Симулировать 500 лет":
                        await Bot.send_message(chat_id=chat_id, text="Вам придется подождать(")
                        run_simulation(500)
                        await Bot.send_message(chat_id=chat_id, text="Симуляция завершена")

                    if message_text == "Сбросить":
                        reset()
                        await Bot.send_message(chat_id=chat_id, text="Сброшено")

                    if message_text == "Получить статистику":
                        urls = StatPlot.get_all()
                        for ph in urls[:-1]:
                            await Bot.send_photo(chat_id, ph)
                        await Bot.send_document(chat_id, urls[-1])
                        for url in urls:
                            os.remove(url)
        else:
            import time

            time.sleep(1)

asyncio.run(main())