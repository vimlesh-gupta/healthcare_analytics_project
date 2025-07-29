from src.csv_eda.load_csv import load_all_data
import pandas as pd

# Unpack all DataFrames returned from load_all_data():  — must be in correct order to avoid mismatches
df_appointments, df_churn_label, df_diagnosis, df_diseases, df_doctors, df_emergency_cases, df_hospitals, df_insurances, df_patients = load_all_data()


# 1. Most common diseases across India
def get_common_disease(df_patients, top_n):
    """Returns most common diseases.

    Returns:
        - DataFrame: disease and count.
    """
    # Count occurrences of each disease and return top N
    df_common_diseases = df_patients['disease'].value_counts().sort_values(ascending=False).reset_index().head(top_n)
    df_common_diseases.columns = ['disease', 'count']  # Rename columns for clarity
    return df_common_diseases


# 2. Age group most affected by critical illnesses
def get_age_group_affected_by_critical_illness(df_diagnosis, df_patients, top_n):
    """Returns most affected age groups by high-risk illness.

    Returns:
        - DataFrame: age_group and count.
    """
    # Merge patient and diagnosis data on patient_id
    merged_df = pd.merge(df_diagnosis, df_patients, on='patient_id')

    # Define age bins and labels
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']

    # Create age group column
    merged_df['age_group'] = pd.cut(merged_df['age'], bins=bins, labels=labels, right=False)

    # Filter only high-risk cases
    high_risk_df = merged_df[merged_df['risk_level'] == 'High']

    # Count frequency of each age group among high-risk cases
    df_common_age_group = high_risk_df['age_group'].value_counts().sort_values(ascending=False).reset_index().head(
        top_n)
    df_common_age_group.columns = ['age_group', 'count']
    return df_common_age_group


# 3. Disease frequency by gender
def get_disease_frequency_by_gender(df_patients, top_n):
    """Returns disease frequency by gender.

    Returns:
        - DataFrame: pivoted disease vs gender with count.
    """
    # Count disease occurrences grouped by gender
    df_disease_frequency = df_patients.groupby(['gender', 'disease']).size().reset_index(name='count')

    # Select top N diseases overall
    top_n_diseases = df_disease_frequency.groupby('disease')['count'].sum().nlargest(top_n).index

    # Filter only top diseases
    df_filtered = df_disease_frequency[df_disease_frequency['disease'].isin(top_n_diseases)]

    # Pivot to show disease as index and gender-wise count as columns
    pivoted = df_filtered.pivot(index='disease', columns='gender', values='count').fillna(0)
    return pivoted


# 4. Patient distribution by state
def get_patient_distribution_by_state(df_patients, top_n):
    """Returns patient count by state.

    Returns:
        - Series: state and patient count.
    """
    # Count number of patients per state
    patients_by_state = df_patients['state'].value_counts().sort_values(ascending=False).head(top_n)
    return patients_by_state


# 5. Patient registration trends over time
def get_patients_registration_trends_over_time(df_patients):
    """Returns patient registration trend over months.

    Returns:
        - Series: month and registration count.
    """
    # Convert registration_date to datetime
    df_patients['registration_date'] = pd.to_datetime(df_patients['registration_date'])

    # Group by month and count registrations
    registration_trends = df_patients.groupby(df_patients['registration_date'].dt.to_period('M')).size()

    # Convert index back to timestamp for plotting
    registration_trends.index = registration_trends.index.to_timestamp()
    return registration_trends


# 6. Emergency cases by type
def get_emergency_cases_type(df_emergency_cases):
    """Returns emergency cases by severity type.

    Returns:
        - Series: severity type and count.
    """
    # Count cases by severity type
    emergency_cases_by_type = df_emergency_cases['severity_type'].value_counts()
    return emergency_cases_by_type


# 7. Risk level vs. age scatter plot
def get_risk_level_vs_age(df_patients, df_diagnosis):
    """Returns age vs risk level data.

    Returns:
        - DataFrame: age and risk_level.
    """
    # Merge patient age with diagnosis risk level
    merged_df = pd.merge(df_patients, df_diagnosis[['patient_id', 'risk_level']], on='patient_id')
    return merged_df


# 8. Diagnosis count per doctor
def get_diagnosis_count_per_docter(df_doctors, df_appointments, df_diagnosis, top_n):
    """Returns diagnosis count per doctor.

    Returns:
        - Series: doctor_name and diagnosis count.
    """
    # Merge appointments with doctor data
    merged_df = pd.merge(df_appointments, df_doctors, on='doctor_id')

    # Merge with diagnosis to link diagnosis to doctors
    merged_df = pd.merge(merged_df, df_diagnosis, on='patient_id')

    # Count number of diagnoses per doctor
    diagnosis_per_doctor = merged_df.groupby('doctor_name')['diagnosis_id'].count().sort_values(ascending=False).head(
        top_n)
    return diagnosis_per_doctor


# 9. Hospital capacity vs. no. of appointments
def get_hospital_capacity_vs_appointments(df_hospitals, df_appointments):
    """Returns appointment count vs hospital capacity.

    Returns:
        - DataFrame: hospital_name, capacity, and appointment count.
    """
    # Merge appointments with hospital data
    merged_df = pd.merge(df_hospitals, df_appointments, on='hospital_id')

    # Group by hospital and capacity, then count appointments
    capacity_vs_appointments = merged_df.groupby(['hospital_name', 'capacity'])['appointment_id'].count().sort_values(
        ascending=False).reset_index().head()

    # Rename columns for clarity
    capacity_vs_appointments.columns = ('hospital_name', 'capacity', 'count')
    return capacity_vs_appointments


# 10. Appointments needing follow-up by disease
def get_appointments_needing_follow_up_by_disease(df_appointments, df_patients, top_n):
    """Returns top diseases needing follow-up.

    Returns:
        - DataFrame: disease and follow_up count.
    """
    # Merge appointments with disease info from patients
    merged_df = pd.merge(df_appointments, df_patients[['patient_id', 'disease']], on='patient_id', how='left')

    # Filter appointments marked as needing follow-up
    df_follow_up = merged_df[merged_df['follow_up_needed'] == 'Yes']

    # Count follow-ups by disease
    follow_up_counts = df_follow_up['disease'].value_counts().reset_index(name='follow_up_counts').head(top_n)
    return follow_up_counts
