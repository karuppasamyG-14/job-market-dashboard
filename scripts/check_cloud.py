import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

query = """
SELECT COUNT(*) AS total_jobs,
       SUM(CASE WHEN description ILIKE '%sql%' THEN 1 ELSE 0 END) AS sql_jobs
FROM jobs
"""

print(pd.read_sql(text(query), engine))