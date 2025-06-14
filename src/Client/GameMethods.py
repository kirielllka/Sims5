import math
from functools import partial


from src.Client.BotMethods import Bot
from src.HumanDAO.HumanDAO import HumanDAO
from concurrent.futures import ThreadPoolExecutor, as_completed

import random

from src.StatPlots import StatPlot

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


class Human:
    def __init__(self,id,name,age,sex,death_or_alive,
                 pregnancy,mother_id,father_id,last_partner):
        self.id = id
        self.name = name
        self.age = age
        self.sex = sex
        self.death_or_alive = death_or_alive
        self.pregnancy = pregnancy
        self.mother_id = mother_id
        self.father_id = father_id
        self.last_partner = last_partner

    def birth(self):
        sex = random.choice(["M", "F"])
        name = random.choice(male_names if sex == "M" else female_names)
        self.pregnancy = None
        child = Human(
                    id=None,
                    name=name,
                    age=0,
                    mother_id=self.id,
                    father_id=self.last_partner,
                    sex=sex,
                    death_or_alive=True,
                    last_partner=None,
                    pregnancy=None)
        c_dict = child.__dict__
        c_dict.pop('id')
        with ThreadPoolExecutor() as executor:
            executor.submit(HumanDAO.update, **{'human_id':self.id,
                                                'updated_data':
                                                    {'pregnancy':self.pregnancy}})
            executor.submit(HumanDAO.create, **{'data': c_dict})



    @classmethod
    def oldering_on_year(cls):
        peoples = [Human(id=p.id,name=p.name,age=p.age,
                         sex=p.sex,death_or_alive=p.death_or_alive,
                         pregnancy=p.pregnancy,mother_id=p.mother_id,
                         father_id=p.father_id,
                         last_partner=p.last_partner) for p in HumanDAO.get_alive()]
        choose_pair()

        with ThreadPoolExecutor() as executor:
            executor.map(process_person, peoples)

def choose_pair(n=0):
    peoples = list(HumanDAO.get_all())
    p1 = random.choice(peoples)
    peoples.remove(p1)
    wights = len(peoples) * [1]
    try:
        if p1.sex == 'F':second_p = HumanDAO.get_by_id(HumanDAO.child_by_mother(p1.id).father_id)
        else:second_p = HumanDAO.get_by_id(HumanDAO.child_by_father(p1.id).mother_id)
        wights[wights.index(second_p)] = 3
    except Exception:
        pass
    p2 = random.choices(peoples, weights=wights, k=1)[0]
    if (p1.sex != p2.sex and p1.age>=18 and p2.age>=18 and
            p1.pregnancy is None and p2.pregnancy is None):
        if p1.sex == 'F':mother,father = p1,p2
        else: mother,father = p2,p1
        updates = [
            {"human_id": mother.id, "updated_data": {"pregnancy": 1}},
            {"human_id": father.id, "updated_data": {"last_partner": mother.id}},
            {"human_id": mother.id, "updated_data": {"last_partner": father.id}},
        ]
        with ThreadPoolExecutor() as executor:
            list(executor.map(lambda x: HumanDAO.update(**x), updates))
    if n != 2:
        choose_pair(n + 1)
    else:
        return None


def process_person(people:Human):
    death_prob = (people.age/120)**8
    a = random.random()
    if a < death_prob:
        print(a,death_prob)
        HumanDAO.update(human_id=people.id, updated_data={"death_or_alive": False})
        return
    if people.pregnancy and people.death_or_alive :
        if people.pregnancy == 0.5:
            people.birth()
            HumanDAO.update(
                human_id=people.id,
                updated_data={
                    "age": people.age + 0.25,
                    "pregnancy": None,
                },
            )
        else:
            HumanDAO.update(
                human_id=people.id,
                updated_data={
                    "age": people.age + 0.5,
                    "pregnancy": people.pregnancy-0.5,
                },
            )
    elif people.death_or_alive:
        HumanDAO.update(human_id=people.id, updated_data={"age": people.age + 0.5})


def run_simulation(years=1):
    for i in range(years*2):
        if i%2 == 0:
            Human.oldering_on_year()
            print(i//2)


async def show_people(
    chat_id, page=0, page_size=10, edit: bool = False, message_id: int = None
):
    people = HumanDAO.get_all()
    total_pages = (len(people) + page_size - 1) // page_size

    message = "Список людей:\n"
    for person in people[page * page_size : (page + 1) * page_size]:
        message += (
            f"{person.name}-{int(person.age)} лет "
            f"{'Жив' if person.death_or_alive else 'Мертв'}\n"
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
        await Bot.edit_message(
            chat_id=chat_id, text=message, keyboard=keyboard, message_id=message_id
        )
    else:
        await Bot.send_message(chat_id=chat_id, text=message, keyboard=keyboard)


def reset():
    for p in HumanDAO.get_all():
        HumanDAO.delete(p.id)
    for p in start_characters:
        HumanDAO.create(p)


start_characters = [
    {
        "name": "Алиса",
        "age": 30,
        "mother_id": None,
        "pregnancy": None,
        "father_id": None,
        "sex": "F",
        "death_or_alive": True,
    },
    {
        "name": "Миша",
        "age": 35,
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
        "age": 28,
        "mother_id": None,
        "pregnancy": None,
        "father_id": None,
        "sex": "F",
        "death_or_alive": True,
    },
    {
        "name": "Рома",
        "age": 10,
        "mother_id": None,
        "pregnancy": None,
        "father_id": None,
        "sex": "M",
        "death_or_alive": True,
    },
    {
        "name": "Николай",
        "age": 23,
        "mother_id": None,
        "pregnancy": None,
        "father_id": None,
        "sex": "M",
        "death_or_alive": True,
    },
    {
        "name": "Алина",
        "age": 20,
        "mother_id": None,
        "pregnancy": None,
        "father_id": None,
        "sex": "F",
        "death_or_alive": True,
    },
]
