import math
import random

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
        for person2 in adults[i+1:]:
            if person1.sex != person2.sex:
                if person1.sex == 'M': father_id, mother_id = person1.id, person2.id
                else: father_id, mother_id = person2.id, person1.id
                children = HumanDAO.child_by_parents(father_id, mother_id)
                weight = 1
                if children:
                    weight = 3
                pairs.append((person1, person2))
                weights.append(weight)

    if pairs:
        chosen_pair = random.choices(pairs, weights=weights, k=1)[0]
        person1, person2 = chosen_pair
        if person1.sex =='M':
            HumanDAO.update(human_id=person2.id,updated_data={'pregnancy':9})
    else:
        print("Нет подходящих пар для рождения ребенка.")

def oldering_on_month():
    peoples = HumanDAO.get_alive()
    for people in peoples:
        if (a:=random.randint(7,1000)) < (b:=(people.age /(350*12))*100):HumanDAO.update(human_id=people.id,updated_data={'death_or_alive':False});print('123',a,b)
        if people.pregnancy:
            if people.pregnancy==1:
                pass
            else:
                HumanDAO.update(human_id=people.id,updated_data={'age':people.age+1})
        else:
            HumanDAO.update(human_id=people.id,updated_data={'age':people.age+1})

test_characters = [
    {
        'id': 1,
        'name': 'Alice',
        'age': 30*12,
        'mother_id': None,
        'pregnancy': None,
        'father_id': None,
        'sex': 'F',
        'death_or_alive': True
    },
    {
        'id': 2,
        'name': 'Bob',
        'age': 35*12,
        'mother_id': None,
        'pregnancy': None,
        'father_id': None,
        'sex': 'M',
        'death_or_alive': True
    },
    {
        'id': 3,
        'name': 'Charlie',
        'age': 5,
        'mother_id': None,
        'pregnancy': None,
        'father_id': None,
        'sex': 'M',
        'death_or_alive': True
    },
    {
        'id': 4,
        'name': 'Diana',
        'age': 28*12,
        'mother_id': None,
        'pregnancy': None,
        'father_id': None,
        'sex': 'F',
        'death_or_alive': True
    },
    {
        'id': 5,
        'name': 'Ethan',
        'age': 10*12,
        'mother_id': None,
        'pregnancy': None,
        'father_id': None,
        'sex': 'M',
        'death_or_alive': True
    }
]

for i in range(8*12):
    oldering_on_month()