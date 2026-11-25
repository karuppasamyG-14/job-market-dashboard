import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

create_view = r"""
CREATE OR REPLACE VIEW entry_level_recent AS
SELECT title, company, created, link
FROM clean_jobs
WHERE CAST(created AS timestamp) >= NOW() - INTERVAL '30 days'
  AND title ~* '\m(intern|interns|internship|trainee|fresher|junior|entry)\M'
ORDER BY created DESC
"""

with engine.begin() as conn:
    conn.execute(text(create_view))

print(pd.read_sql(text("SELECT title, company, created FROM entry_level_recent"), engine))