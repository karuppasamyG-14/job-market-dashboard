import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def fetch_jobs():
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
        response = requests.get(url, params=params)
        data = response.json()

        if "results" not in data:
            print("API error on page", page)
            print("HTTP status:", response.status_code)
            print("Message:", data.get("error", "no message"))
            raise SystemExit(1)

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

    return pd.DataFrame(rows)


def store_jobs(df):
    engine = create_engine(os.getenv("DATABASE_URL"))

    try:
        existing = pd.read_sql("SELECT job_id FROM jobs", engine)
        existing_ids = set(existing["job_id"])
    except Exception:
        existing_ids = set()

    new_jobs = df[~df["job_id"].isin(existing_ids)]
    new_jobs = new_jobs.drop_duplicates(subset="job_id")
    new_jobs.to_sql("jobs", engine, if_exists="append", index=False)

    return len(new_jobs)


def main():
    df = fetch_jobs()
    new_count = store_jobs(df)
    print("Fetched:", len(df), "| New:", new_count)


if __name__ == "__main__":
    main()