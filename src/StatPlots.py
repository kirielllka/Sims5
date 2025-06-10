import csv
from concurrent.futures import ThreadPoolExecutor

from matplotlib import pyplot as plt

from src.HumanDAO.HumanDAO import HumanDAO


class StatPlot:
    data = HumanDAO.get_all()

    @classmethod
    def get_sex_pie(cls):
        fig, ax = plt.subplots()
        label = ["Мужчины", "Женщины"]
        vals = [
            len([p for p in cls.data if p.sex == "M"]),
            len([p for p in cls.data if p.sex == "F"]),
        ]

        ax.pie(vals, labels=label, autopct="%1.1f%%")
        ax.set_title("Соотношение женщин и мужчин")

        url = "pie_sex_plot.png"
        fig.savefig(url)
        plt.close(fig)
        return url

    @classmethod
    def get_scatter_old(cls):
        fig, ax = plt.subplots()
        age = [people.age // 12 for people in cls.data]
        status = [
            "Жив" if people.death_or_alive is True else "Мертв"
            for people in cls.data
        ]
        ax.scatter(x=age, y=status)
        ax.set_title("График продолжительности жизни")
        url = "scatter_old.png"
        fig.savefig(url)
        plt.close(fig)
        return url

    @classmethod
    def get_pregn_pie(cls):
        fig, ax = plt.subplots()
        vals = [
            len([people for people in cls.data if people.pregnancy]),
            len(
                [
                    people
                    for people in cls.data
                    if not people.pregnancy and people.sex == "F"
                ]
            ),
        ]
        label = ["Беременные", "Не беременные"]
        ax.pie(vals, labels=label, autopct="%1.1f%%")
        ax.set_title("Соотношение беременных женщин к небеременным")
        url = "pregn_pie.png"
        fig.savefig(url)
        plt.close(fig)
        return url

    @classmethod
    def get_demogr_pie(cls):
        fig, ax = plt.subplots()
        vals = [
            a := len(
                [people for people in cls.data if people.death_or_alive is False]
            ),
            len(cls.data) - a,
        ]
        label = ["Умерло", "Родилось"]
        ax.pie(vals, labels=label, autopct="%1.1f%%")
        url = "demog_pie.png"
        fig.savefig(url)
        plt.close(fig)
        return url

    @classmethod
    def export_humans_to_csv(cls):
        humans = HumanDAO.get_all()

        with open("human.csv", "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "ID",
                "Имя",
                "Возраст",
                "Пол",
                "Статус",
                "Мать ID",
                "Отец ID",
                "Последний партнер ID",
                "Беременность",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            with ThreadPoolExecutor() as executor:
                rows = executor.map(
                    lambda h: {
                        "ID": h.id,
                        "Имя": h.name,
                        "Возраст": h.age,
                        "Пол": h.sex,
                        "Статус": "Жив" if h.death_or_alive else "Мертв",
                        "Мать ID": h.mother_id or "",
                        "Отец ID": h.father_id or "",
                        "Последний партнер ID": h.last_partner or "",
                        "Беременность": (
                            h.pregnancy if h.pregnancy is not None else ""
                        ),
                    },
                    humans,
                )

                for row in rows:
                    writer.writerow(row)
        return "human.csv"

    @classmethod
    def get_all(cls):
        return [
            StatPlot.get_sex_pie(),
            StatPlot.get_scatter_old(),
            StatPlot.get_pregn_pie(),
            StatPlot.get_demogr_pie(),
            StatPlot.export_humans_to_csv(),
        ]
