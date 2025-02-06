import logging
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from states import UserProfile
from client import fetch_weather
from utils.utils import calculate_water_goal, calculate_calorie_goal

logging.basicConfig(level=logging.INFO)

router = Router()
users = {}

def get_user_profile(user_id):
    """Создаёт профиль пользователя, если его нет."""
    if user_id not in users:
        users[user_id] = {}
    return users[user_id]

@router.message(Command("set_profile"))
async def set_profile(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_data = get_user_profile(user_id)

    if user_data:
        await message.answer("У вас уже есть профиль. Хотите обновить? (да/нет)")
        await state.set_state(UserProfile.name)
        return

    await message.answer("Введите ваше имя:")
    await state.set_state(UserProfile.name)

@router.message(UserProfile.name)
async def process_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    get_user_profile(user_id)["name"] = message.text

    await message.answer("Введите ваш пол (м/ж):")
    await state.set_state(UserProfile.gender)

@router.message(UserProfile.gender)
async def process_gender(message: Message, state: FSMContext):
    user_id = message.from_user.id
    gender = message.text.lower()

    if gender not in ["м", "ж"]:
        await message.answer("⚠ Введите 'м' (мужской) или 'ж' (женский).")
        return

    get_user_profile(user_id)["gender"] = gender
    await message.answer("Введите ваш вес (в кг):")
    await state.set_state(UserProfile.weight)

@router.message(UserProfile.weight)
async def process_weight(message: Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        weight = float(message.text.replace(",", "."))
        get_user_profile(user_id)["weight"] = weight
        await message.answer("Введите ваш рост (в см):")
        await state.set_state(UserProfile.height)
    except ValueError:
        await message.answer("⚠ Введите вес числом (например, 72.5).")

@router.message(UserProfile.height)
async def process_height(message: Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        height = int(message.text)
        get_user_profile(user_id)["height"] = height
        await message.answer("Введите ваш возраст:")
        await state.set_state(UserProfile.age)
    except ValueError:
        await message.answer("⚠ Введите рост числом.")

@router.message(UserProfile.age)
async def process_age(message: Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        age = int(message.text)
        get_user_profile(user_id)["age"] = age
        await message.answer("Сколько минут активности у вас в день?")
        await state.set_state(UserProfile.activity)
    except ValueError:
        await message.answer("⚠ Введите возраст числом.")

@router.message(UserProfile.activity)
async def process_activity(message: Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        activity = int(message.text)
        get_user_profile(user_id)["activity"] = activity
        await message.answer("В каком городе вы находитесь?")
        await state.set_state(UserProfile.city)
    except ValueError:
        await message.answer("⚠ Введите количество минут числом.")

@router.message(UserProfile.city)
async def process_city(message: Message, state: FSMContext):
    user_id = message.from_user.id
    city = message.text.strip()

    temperature = await fetch_weather(city)
    
    if temperature is None:
        await message.answer("⚠ Ошибка: не удалось получить температуру. Попробуйте другой город.")
        return

    user_data = get_user_profile(user_id)
    user_data["city"] = city
    user_data["temperature"] = temperature
    user_data["water_goal"] = calculate_water_goal(user_data["weight"], user_data["activity"], temperature)
    user_data["calorie_goal"] = calculate_calorie_goal(user_data["weight"], user_data["height"], user_data["age"], user_data["activity"])

    await state.clear()
    await message.answer(
        f"✅ *Профиль сохранён!*\n\n"
        f"👤 *Имя:* {user_data['name']}\n"
        f"⚤ *Пол:* {user_data['gender']}\n"
        f"⚖️ *Вес:* {user_data['weight']} кг\n"
        f"📏 *Рост:* {user_data['height']} см\n"
        f"🎂 *Возраст:* {user_data['age']} лет\n"
        f"🏙 *Город:* {city}\n"
        f"🌡 *Температура:* {temperature}°C\n" 
        f"💧 *Ваша дневная норма воды:* {user_data['water_goal']} мл\n"
        f"🔥 *Калории:* {user_data['calorie_goal']} ккал",
        parse_mode="Markdown"
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
