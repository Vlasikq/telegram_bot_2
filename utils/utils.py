import requests
from config_reader import config


def calculate_water_goal(weight, activity, temperature):
    base_water = weight * 30 
    activity_water = (activity // 30) * 500 
    temp_water = 500 if temperature > 25 else 0 
    return base_water + activity_water + temp_water

def calculate_calorie_goal(weight, height, age, activity):
    base_calories = 10 * weight + 6.25 * height - 5 * age + 400 
    activity_calories = (activity // 30) * 200
    return base_calories + activity_calories

def calculate_food_calories(calories_per_100g, weight):
    return (calories_per_100g * weight) / 100

def calculate_calories_mets(mets, weight, duration):
    return (mets * 3.5 * weight / 200) * duration


def get_temperature(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.weather_api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        return data["main"]["temp"]
    return None

def get_food_calories(product_name):
    """
    Получает калорийность продукта из OpenFoodFacts по названию продукта.
    """
    url = f"{config.food_api_url}{product_name}.json"
    response = requests.get(url)
    data = response.json()

    if "product" in data and "nutriments" in data["product"]:
        return data["product"]["nutriments"].get("energy-kcal_100g", "Нет данных")
    return "Продукт не найден"
