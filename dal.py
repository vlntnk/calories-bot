from sqlalchemy.orm import Session
from sqlalchemy import update, select
from pg_config import Users


class DAL():

    def __init__(self, session: Session):
        self.session = session

    def write_user(self, username: str, chat_id: str):
        user = Users(username=username, chat_id=chat_id)
        try:
            self.session.add(user)
            self.session.flush()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f'{e}')
        
    def write_calories(self, username: str, calories: int):
        query = update(Users).where(username=username).values(calories=calories)
        try:
            self.session.execute(query)
            self.session.flush()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f'{e}')

    def check_user_exists(self, username: str):
        query = select(Users).where(Users.username==username)
        try:
            result = self.session.execute(query)
            self.session.commit()
            return bool(result.fetchone())
        except Exception as e:
            self.session.rollback()
            print(f'{e}')