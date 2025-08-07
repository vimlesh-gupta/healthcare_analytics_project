from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus

load_dotenv()

def get_ingine():
    try:
        user=os.getenv("DB_USER")
        password=quote_plus(os.getenv("DB_PASS"))
        host=os.getenv("DB_HOST")
        port=os.getenv("DB_PORT")
        database=os.getenv("DB_NAME")

        if not all([user,password,host,port,database]):
            raise ValueError("❌ One or more required environment variables (user,password,host,port,database) are missing.")
        engine=create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

        with engine.connect() as conn:
            print("✅ Successfully connected to the database.")
        return engine
    except Exception as e:
        print("❌ Failed to connect to the database.")
        print(f"Error: {e}")
        return None
