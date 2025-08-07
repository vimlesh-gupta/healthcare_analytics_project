from db_connection import get_ingine
import pandas as pd
from sqlalchemy import text
engine=get_ingine()

def run_query(query):
    try:
        return pd.read_sql_query(text(query),engine)
    except Exception as e:
        print("❌ Error during SQL query:")
        print(f"{e}")
        return pd.DataFrame()
