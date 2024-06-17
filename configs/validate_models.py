from pydantic import BaseModel

class Dish(BaseModel):
    name: str
    dish: str
    calories: int
    author: str