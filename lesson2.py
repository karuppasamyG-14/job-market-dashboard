import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://api.adzuna.com/v1/api/jobs/in/search/1"
params = {
    "app_id": os.getenv("ADZUNA_APP_ID"),
    "app_key": os.getenv("ADZUNA_APP_KEY"),
    "what": "data analyst",
    "where": "chennai",
    "results_per_page": 2,
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)

data = response.json()
print("Total jobs found:", data["count"])

safe_url = response.url.replace(os.getenv("ADZUNA_APP_KEY"), "HIDDEN")
print(safe_url)