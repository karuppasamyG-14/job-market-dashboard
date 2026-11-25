import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

create_view = r"""
CREATE OR REPLACE VIEW skill_demand AS
SELECT 'SQL' AS skill, COUNT(*) AS jobs FROM clean_jobs WHERE description ILIKE '%sql%'
UNION ALL
SELECT 'Python', COUNT(*) FROM clean_jobs WHERE description ILIKE '%python%'
UNION ALL
SELECT 'Excel', COUNT(*) FROM clean_jobs WHERE description ~* '\mexcel\M'
UNION ALL
SELECT 'Power BI', COUNT(*) FROM clean_jobs WHERE description ILIKE '%power bi%'
UNION ALL
SELECT 'Tableau', COUNT(*) FROM clean_jobs WHERE description ILIKE '%tableau%'
"""

with engine.begin() as conn:
    conn.execute(text(create_view))

print(pd.read_sql(text("SELECT * FROM skill_demand ORDER BY jobs DESC"), engine))