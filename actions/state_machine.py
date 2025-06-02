from aiogram.fsm.state import StatesGroup, State

class CalculatePlan(StatesGroup):
    lets_go = State()
    gender = State()
    age = State()
    aim = State()
    height = State()
    weight = State()
    calculate = State()
    activity = State()

class SetPlan(StatesGroup):
    calories = State()

class MainPlot(StatesGroup):
    adding = State()

class Adding(StatesGroup):
    name = State()
    dish = State()
    calories = State()
    proteins = State()
    fats = State()
    carbohydrates = State()

class HaveEaten(StatesGroup):
    choose = State()
    grams = State()