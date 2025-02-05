from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import UserProfile
from client import fetch_weather
from utils.utils import calculate_water_goal, calculate_calorie_goal
from aiogram.filters import Command


router = Router()
users = {} 

@router.message(Command("set_profile"))
async def set_profile(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if user_id in users:
        await message.answer("У вас уже есть профиль. Хотите обновить? (да/нет)")
        await state.set_state(UserProfile.name)
        return

    users[user_id] = {} 
    await message.answer("Введите ваше имя:")
    await state.set_state(UserProfile.name)

@router.message(UserProfile.name)
async def process_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    users[user_id]["name"] = message.text

    await message.answer("Введите ваш пол (м/ж):")
    await state.set_state(UserProfile.gender)

@router.message(UserProfile.gender)
async def process_gender(message: Message, state: FSMContext):
    user_id = message.from_user.id
    gender = message.text.lower()

    if gender not in ["м", "ж"]:
        await message.answer("⚠ Введите 'м' (мужской) или 'ж' (женский).")
        return

    users[user_id]["gender"] = gender
    await message.answer("Введите ваш вес (в кг):")
    await state.set_state(UserProfile.weight)

@router.message(UserProfile.weight)
async def process_weight(message: Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        weight = int(message.text)
        users[user_id]["weight"] = weight
        await message.answer("Введите ваш рост (в см):")
        await state.set_state(UserProfile.height)
    except ValueError:
        await message.answer("⚠ Введите вес числом.")

@router.message(UserProfile.height)
async def process_height(message: Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        height = int(message.text)
        users[user_id]["height"] = height
        await message.answer("Введите ваш возраст:")
        await state.set_state(UserProfile.age)
    except ValueError:
        await message.answer("⚠ Введите рост числом.")

@router.message(UserProfile.age)
async def process_age(message: Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        age = int(message.text)
        users[user_id]["age"] = age
        await message.answer("Сколько минут активности у вас в день?")
        await state.set_state(UserProfile.activity)
    except ValueError:
        await message.answer("⚠ Введите возраст числом.")

@router.message(UserProfile.activity)
async def process_activity(message: Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        activity = int(message.text)
        users[user_id]["activity"] = activity
        await message.answer("В каком городе вы находитесь?")
        await state.set_state(UserProfile.city)
    except ValueError:
        await message.answer("⚠ Введите количество минут числом.")

@router.message(UserProfile.city)
async def process_city(message: Message, state: FSMContext):
    user_id = message.from_user.id
    city = message.text.strip()

    temperature = fetch_weather(city) 
    
    print(f"🔍 DEBUG: Температура в {city} = {temperature}")

    if temperature is None:
        await message.answer("⚠ Ошибка: не удалось получить температуру. Попробуйте другой город.")
        return

    users[user_id]["city"] = city
    users[user_id]["temperature"] = temperature  # 
    users[user_id]["water_goal"] = calculate_water_goal(users[user_id]["weight"], users[user_id]["activity"], temperature)
    users[user_id]["calorie_goal"] = calculate_calorie_goal(users[user_id]["weight"], users[user_id]["height"], users[user_id]["age"], users[user_id]["activity"])

    await state.clear()
    await message.answer(
        f"✅ *Профиль сохранён!*\n\n"
        f"👤 *Имя:* {users[user_id]['name']}\n"
        f"⚤ *Пол:* {users[user_id]['gender']}\n"
        f"⚖️ *Вес:* {users[user_id]['weight']} кг\n"
        f"📏 *Рост:* {users[user_id]['height']} см\n"
        f"🎂 *Возраст:* {users[user_id]['age']} лет\n"
        f"🏙 *Город:* {city}\n"
        f"🌡 *Температура:* {temperature}°C\n" 
        f"💧 *Ваша дневная норма воды:* {users[user_id]['water_goal']} мл\n"
        f"🔥 *Калории:* {users[user_id]['calorie_goal']} ккал"
    )


def register_profile_handlers(router: Router):
    router.message.register(set_profile, Command("set_profile"))
    router.message.register(process_name, UserProfile.name)
    router.message.register(process_gender, UserProfile.gender)
    router.message.register(process_weight, UserProfile.weight)
    router.message.register(process_height, UserProfile.height)
    router.message.register(process_age, UserProfile.age)
    router.message.register(process_activity, UserProfile.activity)
    router.message.register(process_city, UserProfile.city)
