import pandas as pd
import numpy as np
import random
from faker import Faker
from tqdm import tqdm

# --------------------------------------
# Initialize Faker & Seed for reproducibility
# --------------------------------------
fake = Faker("en_IN")
Faker.seed(42)
np.random.seed(42)

# --------------------------------------
# Define Data Paths
# --------------------------------------
DATA_RAW = r"D:\Data Analytics Project\helthcare_analytics_project\data\raw"
DATA_PROCESSED = r"D:\Data Analytics Project\helthcare_analytics_project\data\processed"

# --------------------------------------
# 1. Hospital Data Generation
# --------------------------------------
df_hospitals = pd.read_csv(f"{DATA_RAW}/HospitalsInIndia.csv")
df_hospitals['hospital_id'] = ['HOSP{:05d}'.format(i) for i in range(len(df_hospitals))]
df_hospitals['capacity'] = np.random.randint(20, 500, size=len(df_hospitals))
df_hospitals['emergency_facility'] = np.random.choice(['True', 'False'], size=len(df_hospitals))
# Move 'hospital_id' to first column
hospital_id = df_hospitals.pop('hospital_id')
df_hospitals.insert(0, 'hospital_id', hospital_id)
df_hospitals.to_csv(f"{DATA_PROCESSED}/hospitals.csv", index=False)

# --------------------------------------
# 2. Doctor Data Generation
# --------------------------------------
def generate_doctors(n):
    """Generate doctor records with random experience and associated hospital."""
    data = []
    for i in tqdm(range(n), desc="Generating doctor data"):
        data.append({
            'doctor_id': f'DOCT{i:05d}',
            'doctor_name': fake.name(),
            'experience': np.random.randint(1, 40),
            'hospital_id': np.random.choice(df_hospitals['hospital_id'].values)
        })
    return pd.DataFrame(data)

df_doctors = generate_doctors(65000)
df_doctors.to_csv(f"{DATA_PROCESSED}/doctors.csv", index=False)

# --------------------------------------
# 3. Patient Data Generation
# --------------------------------------
df_diseases = pd.read_csv(f"{DATA_PROCESSED}/diseases.csv")
city_state_list = df_hospitals[['city', 'state']].dropna().values.tolist()

def generate_patients(n):
    """Generate fake patients with diseases, location, and registration date."""
    data = []
    for i in tqdm(range(n), desc="Generating patients"):
        city, state = random.choice(city_state_list)
        data.append({
            'patient_id': f'PATE{i:05d}',
            'patient_name': fake.name(),
            'age': np.random.randint(0, 100),
            'gender': np.random.choice(['Male', 'Female']),
            'disease': np.random.choice(df_diseases['disease']),
            'city': city,
            'state': state,
            'mob_no': '+91 ' + str(random.randint(6000000000, 9999999999)),
            'registration_date': fake.date_between(start_date='-2y', end_date='today')
        })
    return pd.DataFrame(data)

df_patients = generate_patients(100000)
df_patients.to_csv(f"{DATA_PROCESSED}/patients.csv", index=False)

# --------------------------------------
# 4. Appointment Data
# --------------------------------------
# Cache columns for speed
patient_ids = df_patients['patient_id'].values
registration_dates = df_patients['registration_date'].values
doctor_ids = df_doctors['doctor_id'].values
hospital_ids = df_doctors['hospital_id'].values

def generate_appointments(n):
    """Link patients with doctors and hospitals via appointments."""
    data = []
    for i in tqdm(range(n), desc="Generating appointments"):
        idx_p = np.random.randint(0, len(patient_ids))
        idx_d = np.random.randint(0, len(doctor_ids))
        data.append({
            'appointment_id': f'APP{i:06d}',
            'patient_id': patient_ids[idx_p],
            'hospital_id': hospital_ids[idx_d],
            'doctor_id': doctor_ids[idx_d],
            'appointment_date': fake.date_between(start_date=registration_dates[idx_p], end_date='today'),
            'follow_up_needed': np.random.choice(['Yes', 'No'])
        })
    return pd.DataFrame(data)

df_appointments = generate_appointments(300000)
df_appointments.to_csv(f"{DATA_PROCESSED}/appointments.csv", index=False)

# --------------------------------------
# 5. Diagnosis Data
# --------------------------------------
def generate_diagnosis(n):
    """Generate diagnosis for patients with disease and risk level."""
    disease_map = dict(zip(df_patients['patient_id'], df_patients['disease']))
    reg_dates = pd.to_datetime(df_patients['registration_date']).values
    data = []
    for i in tqdm(range(n), desc="Generating diagnosis"):
        idx = np.random.randint(0, len(patient_ids))
        pid = patient_ids[idx]
        disease = disease_map.get(pid, "Unknown")
        reg_date = pd.to_datetime(reg_dates[idx]).date()
        data.append({
            'diagnosis_id': f'DIAGNO{i:05d}',
            'patient_id': pid,
            'disease': disease,
            'risk_level': np.random.choice(['High', 'Medium', 'Low']),
            'diagnosis_date': fake.date_between(start_date=reg_date, end_date='today')
        })
    return pd.DataFrame(data)

df_diagnosis = generate_diagnosis(50000)
df_diagnosis.to_csv(f"{DATA_PROCESSED}/diagnosis.csv", index=False)

# --------------------------------------
# 6. Emergency Cases
# --------------------------------------
def generate_emergency_cases(n):
    """Generate emergency records for patients."""
    data = []
    for i in tqdm(range(n), desc="Generating Emergency cases"):
        idx_p = np.random.randint(0, len(patient_ids))
        data.append({
            'case_id': f'CASE{i:04d}',
            'patient_id': patient_ids[idx_p],
            'emergency_type': np.random.choice(['Accident', 'Cardic Arrest']),
            'severity_type': np.random.choice(['High', 'Medium', 'Low']),
            'case_date': fake.date_between(start_date=registration_dates[idx_p], end_date='today')
        })
    return pd.DataFrame(data)

df_emergency_cases = generate_emergency_cases(25000)
df_emergency_cases.to_csv(f"{DATA_PROCESSED}/emergency_cases.csv", index=False)

# --------------------------------------
# 7. Insurance Data
# --------------------------------------
insurance_company = [
    "LIC of India", "Star Health and Allied Insurance", "ICICI Lombard General Insurance",
    "HDFC ERGO Health Insurance", "New India Assurance", "Bajaj Allianz General Insurance",
    "Religare Health Insurance (now Care Health)", "Tata AIG General Insurance",
    "United India Insurance", "National Insurance Company", "Oriental Insurance Company",
    "SBI General Insurance", "Future Generali India Insurance", "ManipalCigna Health Insurance",
    "Aditya Birla Health Insurance", "Reliance General Insurance", "IFFCO Tokio General Insurance",
    "Niva Bupa Health Insurance", "Kotak Mahindra General Insurance", "Edelweiss General Insurance"
]

def generate_insurances(n):
    """Generate insurance company data."""
    data = []
    for i in tqdm(range(n), desc="Generating insurance data"):
        data.append({
            'insurance_id': f'INSURE{i:04d}',
            'company_name': np.random.choice(insurance_company),
            'coverage_amount': round(np.random.uniform(1_000_000, 10_000_000), 2),
            'premium_per_year': round(np.random.uniform(2000, 25000), 2),
            'valid_till': fake.date_between(start_date='-2y', end_date='+25y')
        })
    return pd.DataFrame(data)

df_insurances = generate_insurances(50000)
df_insurances.to_csv(f"{DATA_PROCESSED}/insurances.csv", index=False)

# --------------------------------------
# 8. Assign Insurance to Patients
# --------------------------------------
def assign_insurance_to_some(df_patients, df_insurances, coverage=0.7):
    """Assign insurance to a portion of patients."""
    n_patients = len(df_patients)
    n_insured = int(n_patients * coverage)

    selected_ids = random.sample(list(df_insurances['insurance_id']), min(n_insured, len(df_insurances)))
    insurance_list = selected_ids + [None] * (n_patients - len(selected_ids))
    np.random.shuffle(insurance_list)

    df_patients['insurance_id'] = insurance_list
    df_patients['is_insured'] = df_patients['insurance_id'].notnull()
    return df_patients

df_patients = assign_insurance_to_some(df_patients, df_insurances)
df_patients.to_csv(f"{DATA_PROCESSED}/patients.csv", index=False)

# --------------------------------------
# 9. Generate Churn Labels
# --------------------------------------
df_last_visit = df_appointments.groupby('patient_id')['appointment_date'].max().reset_index()
df_last_visit.rename(columns={'appointment_date': 'last_visit_date'}, inplace=True)

today = pd.to_datetime('today')
df_last_visit['last_visit_date'] = pd.to_datetime(df_last_visit['last_visit_date'])
df_last_visit['days_since_last_visit'] = (today - df_last_visit['last_visit_date']).dt.days
df_last_visit['churn'] = df_last_visit['days_since_last_visit'].apply(lambda x: 1 if x > 90 else 0)

df_churn_label = df_last_visit[['patient_id', 'last_visit_date', 'days_since_last_visit','churn']]
df_churn_label.to_csv(f"{DATA_PROCESSED}/churn_label.csv", index=False)

# --------------------------------------
print("✅ All files generated successfully!")
