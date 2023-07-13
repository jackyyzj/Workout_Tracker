import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import os

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
EXERCISE_ENDPOINT = os.environ.get("EXERCISE_ENDPOINT")
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")

basic = HTTPBasicAuth(USERNAME, PASSWORD)

GENDER = "male"
WEIGHT_KG = 70
HEIGHT_CM = 173
AGE = 24

SHEET_ENDPOINT = "https://api.sheety.co/ecdc46efe484493f90577b62530e3bcf/myWorkouts/workouts"

headers = {
	"x-app-id": APP_ID,
	"x-app-key": API_KEY,
	"x-remote-user_id": "0",
}

exercise_text = input("Tell me which exercises you did: ")

params = {
	"query": exercise_text,
	"gender": GENDER,
	"weight_kg": WEIGHT_KG,
	"height_cm": HEIGHT_CM,
	"age": AGE
}

response = requests.post(url = EXERCISE_ENDPOINT, json = params, headers= headers, auth=basic)
result = response.json()
print(result)

now_date = datetime.now().strftime('%d/%m/%Y')
now_time = datetime.now().strftime('%X')

for exercise in result["exercises"]:
	exercises = exercise["name"].title()
	duration = exercise["duration_min"]
	calories = exercise["nf_calories"]

	workout_params= {
		"workout":{
		"date": now_date,
			"time": now_time,
			"exercise": exercises,
			"duration": duration,
			"calories": calories,
		}
	}

put_request = requests.post(url = SHEET_ENDPOINT, json = workout_params, auth=basic)
sheet_response  = put_request.json()

get_request = requests.get(url = SHEET_ENDPOINT, auth=basic)
updated_sheet = get_request.json()
