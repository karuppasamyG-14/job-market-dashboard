import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

create_view = """
CREATE OR REPLACE VIEW clean_jobs AS
SELECT DISTINCT ON (company, title, created)
       job_id, title, company, created, description, link
FROM jobs
WHERE CAST(created AS timestamp) >= NOW() - INTERVAL '60 days'
ORDER BY company, title, created, job_id
"""

with engine.begin() as conn:
    conn.execute(text(create_view))

print(pd.read_sql(text("SELECT COUNT(*) AS total FROM clean_jobs"), engine))