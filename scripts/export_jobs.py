import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

df = pd.read_sql("SELECT job_id, title, company, created, description, link FROM jobs", engine)

df.to_csv("jobs_export.csv", index=False, encoding="utf-8-sig")

print("Saved", len(df), "rows")