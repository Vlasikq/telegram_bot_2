import requests
from config_reader import config


import requests
from config_reader import config

import requests
from config_reader import config

def fetch_weather(city):
    """Получает текущую температуру в городе через OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.weather_api_key}&units=metric"

    response = requests.get(url)
    print(f"🌍 API-ответ: {response.status_code}, {response.text}")  # ✅ Лог API

    if response.status_code != 200:
        print(f"❌ Ошибка API: {response.status_code}, {response.text}")  
        return None
    
    try:
        data = response.json()
        

        if "main" in data and "temp" in data["main"]:
            temp = data["main"]["temp"]
            return round(temp, 1)

        print("❌ Ошибка: Температура отсутствует в JSON-ответе!", data)
        return None

    except Exception as e:
        print(f"❌ Ошибка при разборе JSON: {e}")  
        return None


def fetch_food_calories(product_name):
    """Получает калорийность продукта из Nutritionix API."""
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": config.nutritionix_app_id,
        "x-app-key": config.nutritionix_api_key,
        "Content-Type": "application/json"
    }
    data = {"query": product_name}
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if "foods" in data and len(data["foods"]) > 0:
            return data["foods"][0].get("nf_calories", "Нет данных")
    return "Продукт не найден"
