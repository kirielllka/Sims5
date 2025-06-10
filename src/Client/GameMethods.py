import math
from functools import partial

from src.Client.BotMethods import Bot
from src.HumanDAO.HumanDAO import HumanDAO
from concurrent.futures import ThreadPoolExecutor, as_completed

import random

male_names = [
    "Александр",
    "Дмитрий",
    "Максим",
    "Игорь",
    "Павел",
    "Владимир",
    "Роман",
    "Станислав",
    "Константин",
    "Виктор",
    "Андрей",
    "Михаил",
    "Вячеслав",
    "Кирилл",
    "Юрий",
    "Олег",
    "Борис",
    "Алексей",
    "Григорий",
    "Никита",
    "Денис",
    "Артур",
    "Лев",
    "Тимофей",
    "Степан",
    "Даниил",
    "Василий",
    "Захар",
    "Геннадий",
]

female_names = [
    "Мария",
    "Ольга",
    "Татьяна",
    "Ирина",
    "Наталья",
    "Елена",
    "София",
    "Виктория",
    "Ксения",
    "Юлия",
    "Анастасия",
    "Вероника",
    "Людмила",
    "Карина",
    "Дарья",
    "Валерия",
    "Ксения",
    "Марина",
    "Екатерина",
    "Полина",
    "Вера",
    "Светлана",
    "Олеся",
    "Алина",
    "Мила",
    "Василиса",
    "Анна",
    "Кристина",
    "Галина",
    "Нина",
]


def process_mother(mother, males):
    if mother.pregnancy:
        return None

    suitable_males = []
    male_weights = []

    for father in males:
        children = HumanDAO.child_by_parents(father.id, mother.id)
        weight = 3 if children else 1
        suitable_males.append(father)
        male_weights.append(weight)

    if suitable_males:
        chosen_father = random.choices(suitable_males, weights=male_weights, k=1)[0]
        return chosen_father, mother
    return None


def child():
    adults = HumanDAO.get_adults()
    males = [p for p in adults if p.sex == "M"]
    females = [p for p in adults if p.sex == "F"]
    pairs = []
    weights = []
    with ThreadPoolExecutor() as executor:
        process_func = partial(process_mother, males=males)
        future_to_mother = {
            executor.submit(process_func, mother): mother for mother in females
        }
        for future in as_completed(future_to_mother):
            result = future.result()
            if result:
                pairs.append(result)
                weights.append(2)
    if pairs:
        father, mother = random.choices(pairs, weights=weights, k=1)[0]
        updates = [
            {"human_id": mother.id, "updated_data": {"pregnancy": 9}},
            {"human_id": father.id, "updated_data": {"last_partner": mother.id}},
            {"human_id": mother.id, "updated_data": {"last_partner": father.id}},
        ]
        with ThreadPoolExecutor() as executor:
            list(executor.map(lambda x: HumanDAO.update(**x), updates))

    return None


def process_person(people):
    death_prob = 1 - math.exp(-((people.age / (350 * 12)) ** 3))
    if random.random() < death_prob:
        HumanDAO.update(human_id=people.id, updated_data={"death_or_alive": False})
        return

    if people.pregnancy:
        if people.pregnancy == 1:
            birth(people)
        else:
            HumanDAO.update(
                human_id=people.id,
                updated_data={
                    "age": people.age + 1,
                    "pregnancy": people.pregnancy - 1,
                },
            )
    else:
        HumanDAO.update(human_id=people.id, updated_data={"age": people.age + 1})


def oldering_on_month():
    peoples = HumanDAO.get_alive()
    child()

    with ThreadPoolExecutor() as executor:
        executor.map(process_person, peoples)


def birth(mother):
    sex = random.choice(["M", "F"])
    name = random.choice(male_names if sex == "M" else female_names)

    updates = [
        {"human_id": mother.id, "updated_data": {"pregnancy": None}},
        {
            "data": {
                "name": name,
                "age": 0,
                "mother_id": mother.id,
                "father_id": mother.last_partner,
                "sex": sex,
                "death_or_alive": True,
            }
        },
    ]

    with ThreadPoolExecutor() as executor:
        executor.submit(HumanDAO.update, **updates[0])
        executor.submit(HumanDAO.create, **updates[1])


def run_simulation(months=1):
    for i in range(months):
        oldering_on_month()
        if i % 12 == 0:
            print(i)


def show_people(
    chat_id, page=0, page_size=10, edit: bool = False, message_id: int = None
):
    people = HumanDAO.get_all()
    total_pages = (len(people) + page_size - 1) // page_size

    message = "Список людей:\n"
    for person in people[page * page_size : (page + 1) * page_size]:
        message += (
            f"{person.name}-{int(person.age / 12)} лет "
            f"{'Жив' if person.death_or_alive else 'Мертв'}"
            f" {f'{10 - person.pregnancy} месяц беременности'
                        if person.pregnancy else ''}\n"
        )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "⬅️ Назад", "callback_data": f"people_page_{page - 1}"},
                {
                    "text": f"{page + 1}/{total_pages}",
                    "callback_data": "current_page",
                },
                {"text": "Вперёд ➡️", "callback_data": f"people_page_{page + 1}"},
            ]
        ]
    }
    if edit:
        Bot.edit_message(
            chat_id=chat_id, text=message, keyboard=keyboard, message_id=message_id
        )
    else:
        Bot.send_message(chat_id=chat_id, text=message, keyboard=keyboard)


def reset():
    for p in HumanDAO.get_all():
        HumanDAO.delete(p.id)
    for p in start_characters:
        HumanDAO.create(p)


start_characters = [
    {
        "name": "Алиса",
        "age": 30 * 12,
        "mother_id": None,
        "pregnancy": None,
        "father_id": None,
        "sex": "F",
        "death_or_alive": True,
    },
    {
        "name": "Миша",
        "age": 35 * 12,
        "mother_id": None,
        "pregnancy": None,
        "father_id": None,
        "sex": "M",
        "death_or_alive": True,
    },
    {
        "name": "Анна",
        "age": 5,
        "mother_id": None,
        "pregnancy": None,
        "father_id": None,
        "sex": "M",
        "death_or_alive": True,
    },
    {
        "name": "Диана",
        "age": 28 * 12,
        "mother_id": None,
        "pregnancy": None,
        "father_id": None,
        "sex": "F",
        "death_or_alive": True,
    },
    {
        "name": "Рома",
        "age": 10 * 12,
        "mother_id": None,
        "pregnancy": None,
        "father_id": None,
        "sex": "M",
        "death_or_alive": True,
    },
    {
        "name": "Николай",
        "age": 23 * 12,
        "mother_id": None,
        "pregnancy": None,
        "father_id": None,
        "sex": "M",
        "death_or_alive": True,
    },
    {
        "name": "Алина",
        "age": 20 * 12,
        "mother_id": None,
        "pregnancy": None,
        "father_id": None,
        "sex": "F",
        "death_or_alive": True,
    },
]
