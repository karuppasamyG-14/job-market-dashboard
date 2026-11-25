import os
import time
import sqlite3
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

params = {
    "app_id": os.getenv("ADZUNA_APP_ID"),
    "app_key": os.getenv("ADZUNA_APP_KEY"),
    "what": "data analyst",
    "where": "chennai",
    "results_per_page": 50,
}

rows = []
for page in range(1, 4):
    url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"
    data = requests.get(url, params=params).json()

    for job in data["results"]:
        rows.append({
            "job_id": job.get("id", ""),
            "title": job.get("title", "Unknown"),
            "company": job.get("company", {}).get("display_name", "Unknown"),
            "created": job.get("created", "Unknown"),
            "description": job.get("description", ""),
            "link": job.get("redirect_url", ""),
        })

    time.sleep(1)

df = pd.DataFrame(rows)

conn = sqlite3.connect("jobs.db")

try:
    existing = pd.read_sql("SELECT job_id FROM jobs", conn)
    existing_ids = set(existing["job_id"])
except Exception:
    existing_ids = set()

new_jobs = df[~df["job_id"].isin(existing_ids)]
new_jobs = new_jobs.drop_duplicates(subset="job_id")
new_jobs.to_sql("jobs", conn, if_exists="append", index=False)

print("Fetched:", len(df), "| New:", len(new_jobs))
print(pd.read_sql("SELECT COUNT(*) AS total FROM jobs", conn))

conn.close()