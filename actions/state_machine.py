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
