import sqlite3
import pandas as pd


conn = sqlite3.connect('aceap.db')
df = pd.read_sql_query("SELECT * FROM signals WHERE action = 'record'", conn)
conn.close()

print(df)