from aiogram.fsm.state import State, StatesGroup

class UserProfile(StatesGroup):
    name = State()
    gender = State()
    weight = State()
    height = State()
    age = State()
    city = State()
    activity = State()
    calorie_goal = State()
    water_goal = State()

class LogFood(StatesGroup):
    food_name = State() 
    food_weight = State()



class LogWater(StatesGroup):
    water_amount = State() 

class LogWorkout(StatesGroup):
    workout_type = State()
    workout_duration = State()

class CustomGoals(StatesGroup):
    custom_calorie = State() 
    custom_water = State() 
