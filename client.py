import requests
from googletrans import Translator
from config_reader import config
from logger import logger

async def fetch_weather(city):
    """Получает температуру из OpenWeather API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.weather_api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temp = data.get("main", {}).get("temp")

        if temp is not None:
            logger.info(f"🌤 Погода в {city}: {temp}°C")
            return round(temp, 1)
        logger.error(f"⚠ Ошибка: Температура не найдена в JSON для {city}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка API OpenWeather: {e}")

    return None

async def fetch_food_calories(query):
    """Переводит продукт и запрашивает калории из Nutritionix API."""
    translator = Translator()

    try:
        translated_product = await translator.translate(query, src='ru', dest='en')
        translated_product = translated_product.text
        logger.info(f"📡 Перевод: {query} → {translated_product}")
    except Exception as e:
        logger.error(f"Ошибка перевода: {e}")
        return "Ошибка перевода"

    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": config.nutritionix_app_id,
        "x-app-key": config.nutritionix_api_key,
        "Content-Type": "application/json"
    }
    data = {"query": translated_product}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        data = response.json()

        if "foods" in data and len(data["foods"]) > 0:
            calories = data["foods"][0].get("nf_calories", 0)
            logger.info(f"🍏 {translated_product}: {calories} ккал")
            return round(calories, 2)
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка API Nutritionix: {e}")

    return "Продукт не найден"
