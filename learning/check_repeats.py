import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

pd.set_option("display.width", 250)
pd.set_option("display.max_colwidth", 100)

query = """
SELECT COUNT(*) AS unique_recent_postings
FROM (
    SELECT DISTINCT company, title, created
    FROM jobs
    WHERE CAST(created AS timestamp) >= NOW() - INTERVAL ' 60 days'
) t
"""
print(pd.read_sql(text(query), engine))