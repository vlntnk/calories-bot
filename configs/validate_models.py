from pydantic import BaseModel

class Dish(BaseModel):
    name: str
    dish: str
    calories: int
    proteins: int
    fats: int
    carbohydrates: int
    author: str

class CPFC(BaseModel):
    calories: int
    proteins: int
    fats: int
    carbohydrates: int