from db_connection import get_ingine
from src.csv_eda.load_csv import load_all_data
from tqdm import tqdm
import pandas as pd

# Unpack all DataFrames returned from load_all_data():  — must be in correct order to avoid mismatches
df_appointments, df_churn_label, df_diagnosis, df_diseases, df_doctors, df_emergency_cases, df_hospitals, df_insurances, df_patients = load_all_data()

# Connect to DB
engine = get_ingine()

tables={
    "appointments":df_appointments,
    "churn_label":df_churn_label,
    "diagnosis":df_diagnosis,
    "diseases":df_diseases,
    "doctors":df_doctors,
    "emergency_cases":df_emergency_cases,
    "hospitals":df_hospitals,
    "insurances":df_insurances,
    "patients":df_patients
}

try:
    if engine is None:
        raise ConnectionError("❌ Could not establish connection to PostgreSQL.")

    for table_name,df in tqdm(tables.items(), desc="📦 Importing CSVs to PostgreSQL",unit='tables'):
        if df.empty:
            print(f"⚠️ Skipped: 'CSV {table_name}' is empty.")
            continue
        df.to_sql(table_name, con=engine, if_exists="replace",index=False)
        print(f"\n✅ Imported: '{table_name}'")
    print("🎉 All tables imported successfully!")
except Exception as e:
    print(f"❌ Error during import: {e}")