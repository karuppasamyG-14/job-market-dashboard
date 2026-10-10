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
    "results_per_page": 5,
}

data = requests.get(url, params=params).json()

for job in data["results"]:
    title = job.get("title", "Unknown")
    company = job.get("company", {}).get("display_name", "Unknown")
    created = job.get("created", "Unknown")
    print(title, "|", company, "|", created)