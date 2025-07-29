import glob
import os
import pandas as pd

# Path to all processed CSV files
data_path = r"D:\Data Analytics Project\helthcare_analytics_project\data\processed\*.csv"

def load_all_csv():
    """
    Loads all CSV files from the specified data path into a dictionary.
    Keys are the file names (without .csv extension), values are DataFrames.
    """
    dataframes = {}  # Empty dictionary to store DataFrames with keys as file names
    csv_files = glob.glob(data_path)  # List of all CSV file paths

    for file in csv_files:
        df = pd.read_csv(file)  # Read each CSV into a DataFrame
        file_name = os.path.basename(file).replace(".csv", "")  # Extract file name (without extension)
        dataframes[file_name] = df  # Store DataFrame with file name as key

    return dataframes  # Return dictionary of DataFrames


def load_all_data():
    """
    Loads all expected DataFrames using file names as keys from the dictionary.
    Returns a tuple of DataFrames in a fixed order for unpacking in other scripts.
    """
    dfs = load_all_csv()  # Load all CSVs into a dictionary

    # Return the required DataFrames in specific order using .get(key)
    return (
        dfs.get("appointments"),
        dfs.get("churn_label"),
        dfs.get("diagnosis"),
        dfs.get("diseases"),
        dfs.get("doctors"),
        dfs.get("emergency_cases"),
        dfs.get("hospitals"),
        dfs.get("insurances"),
        dfs.get("patients"),
    )
