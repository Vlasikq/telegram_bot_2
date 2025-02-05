from aiogram import types, Dispatcher
from aiogram.filters import Command
from client import fetch_food_calories

users = {}

async def log_food(message: types.Message):
    user_id = message.from_user.id
    food_name = message.text.replace("/log_food ", "").strip()

    if not food_name:
        await message.answer("⚠ Используйте формат: /log_food <название продукта>")
        return

    if user_id not in users:
        users[user_id] = {"calories": 0, "water": 0, "burned_calories": 0}

    calories = await fetch_food_calories(food_name)

    if calories is not None:
        users[user_id]["calories"] += calories
        await message.answer(f"🍏 {food_name} содержит {calories} ккал. Записано в дневник!"
                             f"Проверить прогресс: /check_progress")
    else:
        await message.answer("⚠ Не удалось найти информацию о продукте. Проверьте название.")

async def log_water(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split()

    if len(args) != 2 or not args[1].isdigit():
        await message.answer("⚠ Используйте формат: /log_water <количество мл>")
        return

    if user_id not in users:
        users[user_id] = {"calories": 0, "water": 0, "burned_calories": 0}

    users[user_id]["water"] += int(args[1])
    await message.answer(f"💧 Вы выпили {args[1]} мл воды."
                         f"Проверить прогресс: /check_progress")

async def log_workout(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split()

    if len(args) < 3:
        await message.answer("⚠ Используйте формат: /log_workout <тип тренировки> <время в минутах>")
        return

    workout_type = args[1]
    try:
        duration = int(args[2])

        if user_id not in users:
            users[user_id] = {"calories": 0, "water": 0, "burned_calories": 0}

        burned_calories = duration * 5
        users[user_id]["burned_calories"] += burned_calories

        await message.answer(f"🔥 Вы записали тренировку: {workout_type} ({duration} мин). "
                             f"Сожжено {burned_calories} ккал."
                             f"Проверить прогресс: /check_progress")
    except ValueError:
        await message.answer("⚠ Введите корректное число минут.")

async def check_progress(message: types.Message):
    user_id = message.from_user.id


    if user_id not in users:
        users[user_id] = {"calories": 0, "water": 0, "burned_calories": 0}

    water = users[user_id].get("water", 0)
    calories = users[user_id].get("calories", 0)
    burned_calories = users[user_id].get("burned_calories", 0)
    balance_calories = calories - burned_calories

    progress_text = (
        f"📊 Ваш прогресс:"
        f"💧 Вода выпито: {water} мл"
        f"🍏 Потребленные калории: {calories} ккал"
        f"🔥 Сожженные калории: {burned_calories} ккал"
        f"⚖ Баланс: {balance_calories} ккал"
    )
    await message.answer(progress_text)

def register_tracking_handlers(dp: Dispatcher):
    dp.message.register(log_food, Command(commands=["log_food"]))
    dp.message.register(log_water, Command(commands=["log_water"]))
    dp.message.register(log_workout, Command(commands=["log_workout"]))
    dp.message.register(check_progress, Command(commands=["check_progress"]))
