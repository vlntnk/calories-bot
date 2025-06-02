from sqlalchemy.orm import Session
from sqlalchemy import update, select, delete, text
from databases.pg_config import Users, Dishes


from configs.validate_models import Dish, CPFC

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
        
    def write_calories(self, username: str, calories: int, proteins: int, fats: int, carbohydrates: int):
        query = update(Users).where(Users.username==username).values(calories=calories, proteins=proteins, fats=fats, carbohydrates=carbohydrates)
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

    def delete_user(self, username: str):
        query = delete(Users).where(Users.username==username)
        try: 
            result = self.session.execute(query)
            print(result)
            self.session.flush()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f'{e}')

    def write_dish(self, dish: Dish):
        new_dish = Dishes(name=dish.name, dish=dish.dish, 
                          calories=dish.calories, proteins=dish.proteins,
                          fats=dish.fats, carbohydrates=dish.carbohydrates, author=dish.author)
        try:
            self.session.add(new_dish)
            self.session.flush()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f'{e}, dal')

    def read_users_menu(self, username: str):
        query = text('SELECT name FROM public."Dishes" WHERE author=:username')
        try:
            raw_result = self.session.execute(query, {'username': username})
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f'{e}, dal')
        else:
            result = raw_result.fetchall()
            return result if result else None
        
    def read_meal_details(self, name: str, username: str):
        query = text('SELECT dish, calories, proteins, fats, carbohydrates FROM public."Dishes" WHERE name=:name AND author=:username')
        try: 
            raw_result = self.session.execute(query, {'name': name, 'username': username})
        except Exception as e:
            self.session.rollback()
            print(f'{e}, dal')
        else:
            result = raw_result.fetchall()
            print("RESULT", result)
            return result
        
    def delet_users_dishes(self, username: str):
        query = delete(Dishes).where(Dishes.author==username)
        try: 
            result = self.session.execute(query)
            print(result)
            self.session.flush()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f'{e}')

    def get_limits(self, username: str):
        query = select(Users).where(Users.username==username)
        try:
            result = self.session.execute(query).scalars().one_or_none()
            return CPFC(
                calories=result.calories,
                proteins=result.proteins,
                fats=result.fats,
                carbohydrates=result.carbohydrates,
            )
        except Exception as e:
            self.session.rollback()
            print(f'{e}')
