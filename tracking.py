from aiogram import types, Dispatcher
from aiogram.filters import Command
from client import fetch_food_calories
from logger import logger

users = {}

def get_user_data(user_id):
    """Гарантирует, что у пользователя есть данные в `users`."""
    if user_id not in users:
        users[user_id] = {"calories": 0, "water": 0, "burned_calories": 0}
    return users[user_id]

async def log_food(message: types.Message):
    user_id = message.from_user.id
    query = message.text.replace("/log_food", "").strip()

    if not query:
        await message.answer("⚠ Используйте формат: `/log_food <название продукта>` или `/log_food <количество> <единица> <название>`")
        return

    user_data = get_user_data(user_id)
    calories = await fetch_food_calories(query)

    if isinstance(calories, (int, float)):
        user_data["calories"] += calories
        logger.info(f"🍏 User {user_id} добавил {query}: {calories} ккал")
        await message.answer(f"🍏 {query} содержит {calories} ккал. Записано в дневник!\n"
                             f"Проверить прогресс: /check_progress")
    else:
        logger.warning(f"⚠ User {user_id}: продукт '{query}' не найден")
        await message.answer("⚠ Продукт не найден или произошла ошибка API.")

async def log_water(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split()

    if len(args) != 2 or not args[1].isdigit():
        await message.answer("⚠ Используйте формат: `/log_water <количество мл>`")
        return

    user_data = get_user_data(user_id)
    water_amount = int(args[1])
    user_data["water"] += water_amount

    logger.info(f"💧 User {user_id} выпил {water_amount} мл воды")
    await message.answer(f"💧 Вы выпили {water_amount} мл воды.\n"
                         f"Проверить прогресс: /check_progress")

async def log_workout(message: types.Message):
    user_id = message.from_user.id
    args = message.text.split(maxsplit=2)

    if len(args) < 3 or not args[2].isdigit():
        await message.answer("⚠ Используйте формат: `/log_workout <тип тренировки> <время в минутах>`")
        return

    workout_type, duration = args[1], int(args[2])
    user_data = get_user_data(user_id)
    burned_calories = duration * 5
    user_data["burned_calories"] += burned_calories

    logger.info(f"🔥 User {user_id} записал тренировку: {workout_type} ({duration} мин) - {burned_calories} ккал")
    await message.answer(f"🔥 Вы записали тренировку: *{workout_type}* ({duration} мин).\n"
                         f"Сожжено {burned_calories} ккал.\n"
                         f"Проверить прогресс: /check_progress")

async def check_progress(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    progress_text = (
        "📊 *Ваш прогресс:*\n"
        f"💧 Вода выпито: *{user_data['water']} мл*\n"
        f"🍏 Потребленные калории: *{user_data['calories']} ккал*\n"
        f"🔥 Сожженные калории: *{user_data['burned_calories']} ккал*\n"
        f"⚖ Баланс: *{user_data['calories'] - user_data['burned_calories']} ккал*"
    )

    logger.info(f"📊 User {user_id} запросил прогресс: {user_data}")
    await message.answer(progress_text, parse_mode="Markdown")

def register_tracking_handlers(dp: Dispatcher):
    dp.message.register(log_food, Command("log_food"))
    dp.message.register(log_water, Command("log_water"))
    dp.message.register(log_workout, Command("log_workout"))
    dp.message.register(check_progress, Command("check_progress"))
