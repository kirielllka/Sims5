import csv
import math
import random
from concurrent.futures import ThreadPoolExecutor

from src.Client.BotMethods import Bot
from src.database import session_maker
from src.HumanDAO.HumanDAO import HumanDAO,Human

import random

male_names = [
    "Александр", "Дмитрий", "Максим", "Игорь", "Павел",
    "Владимир", "Роман", "Станислав", "Константин", "Виктор",
    "Андрей", "Михаил", "Вячеслав", "Кирилл", "Юрий",
    "Олег", "Борис", "Алексей", "Григорий", "Никита",
    "Денис", "Артур", "Лев", "Тимофей", "Степан",
    "Даниил", "Василий", "Захар", "Геннадий"
]

female_names = [
    "Мария", "Ольга", "Татьяна", "Ирина", "Наталья",
    "Елена", "София", "Виктория", "Ксения", "Юлия",
    "Анастасия", "Вероника", "Людмила", "Карина", "Дарья",
    "Валерия", "Ксения", "Марина", "Екатерина", "Полина",
    "Вера", "Светлана", "Олеся", "Алина", "Мила",
    "Василиса", "Анна", "Кристина", "Галина", "Нина"
]


def child():
    adults = HumanDAO.get_adults()
    pairs = []
    weights = []
    for i, person1 in enumerate(adults):
        for person2 in adults[i + 1:]:
            print(111)
            if person1.sex != person2.sex:
                father, mother = (person1, person2) if person1.sex == 'M' else (person2, person1)
                children = HumanDAO.child_by_parents(father.id, mother.id)
                weight = 3 if children else 1
                pairs.append((father, mother))
                weights.append(weight)

    if pairs:
        father, mother = random.choices(pairs, weights=weights, k=1)[0]
        if not mother.pregnancy:
            updates = [
                {'human_id': mother.id, 'updated_data': {'pregnancy': 9}},
                {'human_id': father.id, 'updated_data': {'last_partner': mother.id}},
                {'human_id': mother.id, 'updated_data': {'last_partner': father.id}}
            ]
            with ThreadPoolExecutor() as executor:
                list(executor.map(lambda x: HumanDAO.update(**x), updates))
                return None
        else:
            return None
    return None


def process_person(people):
    death_prob = 1 - math.exp(-(people.age / (350 * 12)) ** 3)
    if random.random() < death_prob:
        HumanDAO.update(human_id=people.id, updated_data={'death_or_alive': False})
        return

    if people.pregnancy:
        if people.pregnancy == 1:
            birth(people)
        else:
            HumanDAO.update(
                human_id=people.id,
                updated_data={'age': people.age + 1, 'pregnancy': people.pregnancy - 1}
            )
    else:
        HumanDAO.update(human_id=people.id, updated_data={'age': people.age + 1})


def oldering_on_month():
    peoples = HumanDAO.get_alive()
    child()

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_person, peoples)


def birth(mother):
    sex = random.choice(['M', 'F'])
    name = random.choice(male_names if sex == 'M' else female_names)

    updates = [
        {'human_id': mother.id, 'updated_data': {'pregnancy': None}},
        {'data': {
            'name': name,
            'age': 0,
            'mother_id': mother.id,
            'father_id': mother.last_partner,
            'sex': sex,
            'death_or_alive': True
        }}
    ]


    with ThreadPoolExecutor() as executor:
        executor.submit(HumanDAO.update, **updates[0])
        executor.submit(HumanDAO.create, **updates[1])


def run_simulation(months=1):



    for _ in range(months):
        oldering_on_month()


def export_humans_to_csv(filename):
    humans = HumanDAO.get_all()

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'ID', 'Имя', 'Возраст', 'Пол', 'Статус',
            'Мать ID', 'Отец ID', 'Последний партнер ID', 'Беременность'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with ThreadPoolExecutor() as executor:
            rows = executor.map(lambda h: {
                'ID': h.id,
                'Имя': h.name,
                'Возраст': h.age,
                'Пол': h.sex,
                'Статус': 'Жив' if h.death_or_alive else 'Мертв',
                'Мать ID': h.mother_id or '',
                'Отец ID': h.father_id or '',
                'Последний партнер ID': h.last_partner or '',
                'Беременность': h.pregnancy if h.pregnancy is not None else ''
            }, humans)

            for row in rows:
                writer.writerow(row)


def show_people(chat_id, page=0, page_size=10,edit:bool=False,message_id:int=None):
    people = HumanDAO.get_all()  # Получаем всех людей
    total_pages = (len(people) + page_size - 1) // page_size

    message = "Список людей:\n"
    for person in people[page * page_size: (page + 1) * page_size]:
        message += f"{person.name}-{int(person.age/12)} лет {'Жив' if person.death_or_alive else 'Мертв'}\n"

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "⬅️ Назад", "callback_data": f"people_page_{page - 1}"},
                {"text": f"{page + 1}/{total_pages}", "callback_data": "current_page"},
                {"text": "Вперёд ➡️", "callback_data": f"people_page_{page + 1}"}
            ]
        ]
    }
    if edit:
        Bot.edit_message(
            chat_id=chat_id,
            text=message,
            keyboard=keyboard,
            message_id=message_id
        )
    else:
        Bot.send_message(
            chat_id=chat_id,
            text=message,
            keyboard=keyboard
        )

test_characters = [
    {
        'name': 'Alice',
        'age': 30*12,
        'mother_id': None,
        'pregnancy': None,
        'father_id': None,
        'sex': 'F',
        'death_or_alive': True
    },
    {
        'name': 'Bob',
        'age': 35*12,
        'mother_id': None,
        'pregnancy': None,
        'father_id': None,
        'sex': 'M',
        'death_or_alive': True
    },
    {
        'name': 'Charlie',
        'age': 5,
        'mother_id': None,
        'pregnancy': None,
        'father_id': None,
        'sex': 'M',
        'death_or_alive': True
    },
    {
        'name': 'Diana',
        'age': 28*12,
        'mother_id': None,
        'pregnancy': None,
        'father_id': None,
        'sex': 'F',
        'death_or_alive': True
    },
    {
        'name': 'Ethan',
        'age': 10*12,
        'mother_id': None,
        'pregnancy': None,
        'father_id': None,
        'sex': 'M',
        'death_or_alive': True
    },
    {
            'name': 'Bill',
            'age': 23*12,
            'mother_id': None,
            'pregnancy': None,
            'father_id': None,
            'sex': 'M',
            'death_or_alive': True
    },
    {
        'name': 'Marry',
        'age': 20*12,
        'mother_id': None,
        'pregnancy': None,
        'father_id': None,
        'sex': 'F',
        'death_or_alive': True
    }
]

