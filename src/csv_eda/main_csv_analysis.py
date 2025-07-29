"""Main script to run visualizations on CSV-based healthcare data."""

# Load all datasets and unpack them in a proper sorted order to avoid mismatches
from src.csv_eda.load_csv import load_all_data
df_appointments, df_churn_label, df_diagnosis, df_diseases, df_doctors, df_emergency_cases, df_hospitals, df_insurances, df_patients = load_all_data()

# Import all visualization functions
from src.csv_eda.visualization import (
    plot_common_disease,
    plot_common_age_group_by_critical_illness,
    plot_disease_frequency_by_gender,
    plot_patients_by_state,
    plot_registration_trends_over_time,
    plot_emergency_cases_type,
    plot_risk_level_vs_age,
    plot_diagnosis_count_per_doctor,
    plot_hospital_capacity_vs_appointments,
    plot_appointments_needing_follow_up_by_disease
)

# NOTE: All output image files will be saved automatically to the path defined in visualization.py:
#       D:\Data Analytics Project\helthcare_analytics_project\outputs\visuals\csv

# Plot top common diseases across India
plot_common_disease(df_patients, top_n=10)

# Plot most affected age groups by critical illness
plot_common_age_group_by_critical_illness(df_diagnosis, df_patients, top_n=10)

# Plot disease frequency segmented by gender
plot_disease_frequency_by_gender(df_patients, top_n=10)

# Plot patient count distribution by state
plot_patients_by_state(df_patients, top_n=10)

# Plot registration trends of patients over time
plot_registration_trends_over_time(df_patients)

# Plot emergency case distribution by severity type
plot_emergency_cases_type(df_emergency_cases)

# Plot correlation between risk level and age
plot_risk_level_vs_age(df_patients, df_diagnosis)

# Plot number of diagnoses made by each doctor
plot_diagnosis_count_per_doctor(df_doctors, df_appointments, df_diagnosis, top_n=10)

# Plot relation between hospital capacity and appointment count
plot_hospital_capacity_vs_appointments(df_hospitals, df_appointments)

# Plot diseases that most frequently need follow-up appointments
plot_appointments_needing_follow_up_by_disease(df_appointments, df_patients, top_n=10)
