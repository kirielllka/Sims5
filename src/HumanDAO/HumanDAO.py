from src.Models.HumanModel import Human
from src.database import session_maker


class HumanDAO:

    @classmethod
    def create(cls, data):
        with session_maker() as session:
            human = Human(**data)
            session.add(human)
            session.commit()
            return data

    @classmethod
    def get_by_id(cls, human_id):
        with session_maker() as session:
            return session.query(Human).filter(Human.id == human_id).first()

    @classmethod
    def get_all(cls):
        with session_maker() as session:
            return session.query(Human).all()

    @classmethod
    def update(cls, human_id, updated_data):
        with session_maker() as session:
            human = session.query(Human).get(human_id)
            if not human:
                return None
            for key, value in updated_data.items():
                setattr(human, key, value)
            session.commit()
            return human

    @classmethod
    def delete(cls, human_id: int):
        with session_maker() as session:
            human = cls.get_by_id(human_id)
        if human:
            session.delete(human)
            session.commit()

    @classmethod
    def get_adults(cls):
        with session_maker() as session:
            adults = (
                session.query(Human)
                .filter(Human.death_or_alive == True, Human.age >= 18 * 12)
                .all()
            )
            return adults

    @classmethod
    def get_alive(cls):
        with session_maker() as session:
            people = (
                session.query(Human)
                .filter(
                    Human.death_or_alive == True,
                )
                .all()
            )
            return people

    @classmethod
    def child_by_parents(cls, mother_id, father_id):
        with session_maker() as session:
            child = (
                session.query(Human)
                .filter(
                    Human.mother_id == mother_id,
                    Human.father_id == father_id,
                    Human.death_or_alive == True,
                )
                .all()
            )
            return child

    @classmethod
    def child_by_father(cls,id):
        with session_maker() as session:
            child = (
                session.query(Human)
                .filter(
                    Human.father_id == id,
                    Human.death_or_alive == True,
                )
                .all()
            )
            if len(child) == 0:
                return None
            else:
                return child[0]

    @classmethod
    def child_by_mother(cls,id):
        with session_maker() as session:
            child = (
                session.query(Human)
                .filter(
                    Human.mother_id == id,
                    Human.death_or_alive == True,
                )
                .all()
            )
            if len(child) == 0:
                return None
            else:
                return child[0]
