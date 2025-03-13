from dotenv import load_dotenv
import os
import requests
from datetime import datetime


load_dotenv()

N_ID = os.getenv("NUTRITIONIX_ID")
N_API = os.getenv("NUTRITIONIX_API")
N_URL = os.getenv("NUTRITIONIX_URL")
S_URL = os.getenv("SHEETY_POST_URL")
WEIGHT = os.getenv("WEIGHT")
HEIGHT = os.getenv("HEIGHT")
AGE = os.getenv("AGE")
TOKEN = os.getenv("TOKEN")

# Enter today's workout
query = input("Enter today's exercise: ")

# Get workout summary from nutritionix API
headers = {
    "Content-Type": "application/json",
    "x-app-id": N_ID,
    "x-app-key": N_API,
}
nutritionix_config = {
    "query": query,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,
}
response = requests.post(url=N_URL, headers=headers, json=nutritionix_config)
response.raise_for_status()
print(response.text)

# Add the summary to Google spreed sheet
now = datetime.today()
today = now.strftime("%d/%m/%Y")
current_time = now.strftime("%X")
sheety_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

for target in response.json().get("exercises"):
    print(target)

    exercise = target.get("name").title()
    duration = target.get("duration_min")
    calories = target.get("nf_calories")

    print(duration)

    sheety_config = {
        "workout": {
            "date": today,
            "time": current_time,
            "exercise": exercise,
            "duration": duration,
            "calories": calories,
        }
    }
    response = requests.post(url=S_URL, headers=sheety_headers, json=sheety_config)
    response.raise_for_status()
