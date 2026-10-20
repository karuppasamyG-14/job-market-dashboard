import sqlite3
import pandas as pd

conn = sqlite3.connect("jobs.db")

query = """
SELECT COUNT(*) AS jobs_mentioning_sql
FROM jobs
WHERE description LIKE '%sql%'
"""

print(pd.read_sql(query, conn))

conn.close()