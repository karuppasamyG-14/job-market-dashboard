import sqlite3
import pandas as pd

conn = sqlite3.connect("jobs.db")

query = """
SELECT company, COUNT(*) AS python_jobs
FROM jobs
WHERE description LIKE '%python%'
GROUP BY company
ORDER BY python_jobs DESC
LIMIT 10
"""

print(pd.read_sql(query, conn))

conn.close()