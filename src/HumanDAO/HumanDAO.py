from src.Models.HumanModel import Human
from src.database import session_maker

from sqlalchemy.orm import Session

class HumanDAO:

    def create(self, data):
        self.session.add(data)
        self.session.commit()
        return data

    def get_by_id(self, human_id):
        return self.session.query(Human).filter(Human.id == human_id).first()

    def get_all(self):
        return self.session.query(Human).all()

    def update(self, human_id, updated_data):
        human = self.get_by_id(human_id)
        if not human:
            return None
        for key, value in updated_data.items():
            setattr(human, key, value)
        self.session.commit()
        self.session.refresh(human)
        return human

    def delete(self, human_id):
        human = self.get_by_id(human_id)
        if not human:
            return False
        self.session.delete(human)
        self.session.commit()
        return True

