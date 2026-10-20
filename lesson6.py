import sqlite3
import pandas as pd

conn = sqlite3.connect("jobs.db")

query = """
SELECT company, COUNT(*) AS open_jobs
FROM jobs
GROUP BY company
ORDER BY open_jobs DESC
LIMIT 10
"""

print(pd.read_sql(query, conn))

conn.close()