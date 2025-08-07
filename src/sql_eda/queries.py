"""
queries.py - SQL query definitions for healthcare analytics project.

This module defines SQL queries used for exploratory data analysis (EDA)
and insights generation from synthetic healthcare data.

Author: Vimlesh Gupta
Project: Healthcare Analytics
"""

import pandas as pd
from db_connection import get_ingine

# Establish connection to the database
engine = get_ingine()

# 1. 🔍 Top 5 cities with the highest number of patients
q_top_5_cities_with_highest_disease = """
SELECT city, COUNT(patient_id) AS no_of_patients
FROM patients
GROUP BY city
ORDER BY no_of_patients DESC
LIMIT 5;
"""

# 2. 🎯 Average age of patients diagnosed with high-risk diseases
q_avg_patients_age_with_high_risk_diseases = """
SELECT AVG(p.age) AS avg_age, d.risk_level
FROM patients p 
JOIN diagnosis d ON d.patient_id = p.patient_id
WHERE d.risk_level = 'High'
GROUP BY d.risk_level;
"""

# 3. 👨‍⚕️ Doctor with the most follow-up appointments
q_doctors_with_most_follow_up_appointments = """
SELECT d.doctor_name, COUNT(a.follow_up_needed) AS total_follow_up_appointments
FROM appointments a
JOIN doctors d ON a.doctor_id = d.doctor_id
GROUP BY d.doctor_name
ORDER BY total_follow_up_appointments DESC
LIMIT 10;
"""

# 4. 🔁 Patients who visited more than 3 times in a year
q_patients_who_visited_more_than_3_times_in_a_year = """
SELECT patient_id, COUNT(DATE_TRUNC('year', appointment_date::timestamp)) AS no_of_appointments
FROM appointments
GROUP BY patient_id
HAVING COUNT(DATE_TRUNC('year', appointment_date::timestamp)) > 3
ORDER BY no_of_appointments DESC
LIMIT 10;
"""

# 5. 🚨 States with the highest number of emergency cases
q_state_with_highest_emergency_cases = """
SELECT p.state, COUNT(e.severity_type) AS total_emergency_cases
FROM patients p
JOIN emergency_cases e ON e.patient_id = p.patient_id
GROUP BY p.state
ORDER BY total_emergency_cases DESC
LIMIT 10;
"""

# 6. 🏥 Hospitals with capacity < 100 and high patient load
q_hospitals_with_capacity_less_than_100_and_high_patient_load = """
SELECT h.hospital_name, h.capacity, COUNT(a.patient_id) AS total_patients
FROM appointments a
JOIN hospitals h ON a.hospital_id = h.hospital_id
WHERE h.capacity < 100
GROUP BY h.hospital_name, h.capacity
HAVING COUNT(a.patient_id) > h.capacity
ORDER BY capacity DESC
LIMIT 10;
"""

# 7. ⏳ Average time between patient registration and first diagnosis
q_avg_time_patient_registration_and_first_diagnosis = """
SELECT 
    AVG(d.first_diagnosis_date - p.registration_date::timestamp) AS avg_time_between_registration_and_diagnosis
FROM patients p
JOIN (
    SELECT 
        patient_id, 
        MIN(diagnosis_date::timestamp) AS first_diagnosis_date
    FROM diagnosis
    GROUP BY patient_id
) d ON d.patient_id = p.patient_id;
"""

# 8. 📊 Most common emergency type by city
q_most_common_emergency_type_by_city = """
SELECT city, emergency_type, count
FROM (
    SELECT
        p.city,
        e.emergency_type,
        COUNT(*) AS count,
        ROW_NUMBER() OVER (PARTITION BY p.city ORDER BY COUNT(*) DESC) AS rn
    FROM emergency_cases e
    JOIN patients p ON e.patient_id = p.patient_id
    GROUP BY p.city, e.emergency_type
) AS ranked
WHERE rn = 1
LIMIT 10;
"""

# 9. 📉 Monthly churn rate (%)
q_monthly_churn_rate = """
SELECT
    TO_CHAR(last_visit_date::date, 'MM') AS month_number,
    TO_CHAR(last_visit_date::date, 'Month YYYY') AS churn_month,
    TO_CHAR(last_visit_date::date, 'YYYY') AS churn_year,
    COUNT(*) FILTER (WHERE churn = 1) AS churned_patients,
    COUNT(*) AS total_patients,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE churn = 1) / COUNT(*),
        2
    ) AS churn_rate_percent
FROM churn_label
GROUP BY churn_year, churn_month, month_number
ORDER BY churn_year, month_number;
"""

# 10. 📌 Correlation between insurance coverage and churn
# Used for calculating correlation coefficient in Python
q_correlation_between_insurance_covered_and_churn = """
SELECT 
    c.churn::int,
    CASE WHEN p.is_insured THEN 1 ELSE 0 END AS insurance
FROM patients p
JOIN churn_label c ON p.patient_id = c.patient_id;
"""

# Sample usage in Python:
# df = pd.read_sql_query(q_top_5_cities_with_highest_disease, engine)
# print(df)
# correlation = df['churn'].corr(df['insurance'])
# print(f'Correlation between insurance and churn: {correlation:.2f}')
