import seaborn as sns
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize
from numpy.ma.core import equal

# Load all datasets and unpack them in a proper sorted order to avoid mismatches
from src.csv_eda.load_csv import load_all_data
df_appointments, df_churn_label, df_diagnosis, df_diseases, df_doctors, df_emergency_cases, df_hospitals, df_insurances, df_patients = load_all_data()

# Import all EDA logic functions used in plotting
from src.csv_eda.eda import (
    get_common_disease,
    get_age_group_affected_by_critical_illness,
    get_disease_frequency_by_gender,
    get_patient_distribution_by_state,
    get_patients_registration_trends_over_time,
    get_emergency_cases_type,
    get_risk_level_vs_age,
    get_diagnosis_count_per_docter,
    get_hospital_capacity_vs_appointments,
    get_appointments_needing_follow_up_by_disease
)

# Directory path to save all generated visualization images
output_path = r"D:\Data Analytics Project\helthcare_analytics_project\outputs\visuals\csv"

def plot_common_disease(df_patients, top_n):
    """Plot top diseases across India."""
    df_top_disease = get_common_disease(df_patients, top_n=top_n)

    plt.figure(figsize=(10, 6))
    plt.barh(df_top_disease['disease'], df_top_disease['count'], color='skyblue')
    plt.xlabel('Count')
    plt.ylabel('Top Diseases')
    plt.title("Top diseases across India")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f"{output_path}/common_diseases_across_india.png", bbox_inches="tight")
    plt.show()

def plot_common_age_group_by_critical_illness(df_diagnosis, df_patients, top_n):
    """Plot age groups most affected by critical illness."""
    df_common_age_group = get_age_group_affected_by_critical_illness(df_diagnosis, df_patients, top_n=top_n)

    plt.figure(figsize=(10, 6))
    plt.barh(df_common_age_group['age_group'], df_common_age_group['count'], color='orange')
    plt.xlabel('Count')
    plt.ylabel('Age Group')
    plt.title("Top Age Group By Critical Illness")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f"{output_path}/age_group_by_critical_illness.png", bbox_inches="tight")
    plt.show()

def plot_disease_frequency_by_gender(df_patients, top_n):
    """Plot disease frequency distribution by gender."""
    pivoted = get_disease_frequency_by_gender(df_patients, top_n=top_n)

    pivoted.plot(kind='bar', figsize=(12, 6))
    plt.xlabel('Disease')
    plt.ylabel('Count')
    plt.title("Disease Frequency By Gender")
    plt.tight_layout()
    plt.savefig(f"{output_path}/disease_frequency_by_gender.png", bbox_inches="tight")
    plt.show()

def plot_patients_by_state(df_patients, top_n):
    """Plot patient distribution across top states."""
    patients_by_state = get_patient_distribution_by_state(df_patients, top_n=top_n)

    plt.figure(figsize=(10, 6))
    patients_by_state.plot(kind='bar')
    plt.xlabel("State")
    plt.ylabel("Patient Count")
    plt.title("Patients Distribution by State")
    plt.tight_layout()
    plt.savefig(f"{output_path}/patients_distribution_by_state.png", bbox_inches="tight")
    plt.show()

def plot_registration_trends_over_time(df_patients):
    """Plot registration trend of patients over time."""
    registration_trends = get_patients_registration_trends_over_time(df_patients)

    registration_trends.plot(kind='line', marker='o', color='darkorange', figsize=(12, 6))
    plt.xlabel("Registration Month")
    plt.ylabel("Patients Count")
    plt.title("Registration Trends Over Time")
    plt.tight_layout()
    plt.savefig(f"{output_path}/registration_trends_over_time.png", bbox_inches="tight")
    plt.show()

def plot_emergency_cases_type(df_emergency_cases):
    """Plot emergency cases by severity type."""
    emergency_cases_by_type = get_emergency_cases_type(df_emergency_cases)

    plt.pie(emergency_cases_by_type, labels=emergency_cases_by_type.index, autopct='%1.1f%%', startangle=140)
    plt.title("Emergency Cases By Severity Type")
    plt.tight_layout()
    plt.savefig(f"{output_path}/emergency_cases_by_type.png", bbox_inches="tight")
    plt.show()

def plot_risk_level_vs_age(df_patients, df_diagnosis):
    """Plot age distribution across risk levels."""
    merged_df = get_risk_level_vs_age(df_patients, df_diagnosis)

    plt.figure(figsize=(10, 6))
    sns.violinplot(data=merged_df, x='risk_level', y='age', palette='Set2', hue='gender')
    plt.title("Risk Level vs. Age")
    plt.xlabel("Risk Level")
    plt.ylabel("Age")
    plt.tight_layout()
    plt.savefig(f"{output_path}/risk_level_vs_age.png", bbox_inches="tight")
    plt.show()

def plot_diagnosis_count_per_doctor(df_doctors, df_appointments, df_diagnosis, top_n):
    """Plot diagnosis count for each doctor."""
    diagnosis_per_doctor = get_diagnosis_count_per_docter(df_doctors, df_appointments, df_diagnosis, top_n=top_n)

    diagnosis_per_doctor.plot(kind='bar', figsize=(10, 6))
    plt.xlabel("Doctor Name")
    plt.ylabel("Diagnosis Count")
    plt.title("Diagnosis Count Per Doctor")
    plt.tight_layout()
    plt.savefig(f"{output_path}/diagnosis_per_doctor.png", bbox_inches="tight")
    plt.show()

def plot_hospital_capacity_vs_appointments(df_hospitals, df_appointments):
    """Scatter plot of hospital capacity vs. appointment count."""
    capacity_vs_appointments = get_hospital_capacity_vs_appointments(df_hospitals, df_appointments)

    plt.figure(figsize=(10, 6))
    # Scatter plot helps visualize the correlation between capacity and appointment load
    plt.scatter(data=capacity_vs_appointments, x='capacity', y='count', alpha=0.7, color='teal')
    plt.title("Hospital Capacity Vs Appointments")
    plt.xlabel("Hospital Capacity")
    plt.ylabel("Appointment Count")
    plt.tight_layout()
    plt.savefig(f"{output_path}/hospital_capacity_vs_appontments.png", bbox_inches="tight")
    plt.show()

def plot_appointments_needing_follow_up_by_disease(df_appointments, df_patients, top_n):
    """Plot diseases needing follow-up appointments."""
    follow_up_counts = get_appointments_needing_follow_up_by_disease(df_appointments, df_patients, top_n=top_n)

    plt.figure(figsize=(10, 6))
    plt.barh(follow_up_counts['disease'], follow_up_counts['follow_up_counts'], color='orange')
    plt.xlabel("Disease")
    plt.ylabel("Follow Up Count")
    plt.title("Appointment Needing Follow Up by Disease")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f"{output_path}/appointment_needing_follow_up_by_disease.png", bbox_inches="tight")
    plt.show()
