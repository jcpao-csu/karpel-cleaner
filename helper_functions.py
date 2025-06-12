"""Helper functions to run the Karpel data_preparer and data_uploader"""

import re
import pandas as pd
from pathlib import Path

# --- Define locate_data function --- 
def locate_data(data_path: str) -> str:
    """Identifies and locates the folder with the most recent Karpel data pull"""

    # Initialize Path object 
    main_path = Path(data_path)

    # Initialize list
    all_dates = []

    # Loop through designated folder
    for item in main_path.iterdir():
        if item.is_dir():
            all_dates.append(f"{item}")
    
    # Remove duplicates (there shouldn't be)
    all_dates = list(set(all_dates))

    # Sort list 
    all_dates.sort()

    # Identify folder name (path) with most recent date
    return str(all_dates[-1])

# --- Define create_dir function --- 
def create_dir(data_path: str) -> str:
    """Creates sub-folder in 'Cleaned' directory based off date of recent data dump, then exports all cleaned dfs as CSVs"""
    
    # Extracts dir name, which is the date of the latest data dump
    dir_name = Path(data_path).name

    # Creates dir with dir_name in 'Cleaned' folder
    dir_path = f"cleaned/{dir_name}"
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    return dir_path

# --- Define create_mshp_dir function --- 
def create_mshp_dir(data_path: str) -> str: 
    dir_name = Path(data_path).name
    dir_path = f"helper_files/mshp_codes/cleaned/{dir_name}"
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    return dir_path

# --- Define export_df function --- 
def export_df(df: pd.DataFrame, df_name: str, export_path: str):
    export_to = Path(export_path) / f"{df_name}.csv"
    df.to_csv(export_to, encoding="utf-8", index=False)

# --- Define export_mshp function --- 
def export_mshp(df: pd.DataFrame, df_name: str, subfolder_path: str, export_path: str = "helper_files/mshp_codes/cleaned"):
    export_to = Path(export_path) / Path(subfolder_path).name / f"{df_name}_{subfolder_path}.csv"
    df.to_csv(export_to, encoding="utf-8", index=False)

# --- Exploratory data analysis --- 
    # print(len(df['col_name'].unique()))
    # print(df['col_name'].value_counts())
    # df.drop_duplicates(subset=['col1','col2'], keep='first', inplace=True, ignore_index=True) # Confirm combined primary key (col1, col2) is unique


# --- (import_df) Helper functions --- 

# Initialize test_names list
test_names = [
    'BOGUS', 
    'BADGUY', 
    'SAVEKC', 
    'KARPEL', 
    'MOUSE, MORTIMER'
]

# Define 'row_cleaner' function: remove test cases (based on 'def_name' column)
def row_cleaner(
    df: pd.DataFrame, 
    col_name: str = 'def_name', 
    test_values: [] = test_names # Values indicating test, or fake case
) -> pd.DataFrame:
    """Remove rows containing test (fake cases) values from df"""
    return df[~df[col_name].str.contains("|".join(test_values), regex=True, case=False, na=False)] 

# Define 'filter_columns' function: filter usecols
def filter_columns(column_list: [], remove_columns: [] = ['rcvd_date','enter_date','user_id']) -> []:
    return [item for item in column_list if item not in remove_columns]

# Define 'get_date_cols' function: return list of datetime cols to parse
def get_date_cols(keep_names: []) -> []:
    date_columns = ['ref_date','file_date','disp_date','def_dob'] # All possible datetime cols from Karpel reports 
    return [item for item in keep_names if item in date_columns]

# Define 'str_cleaner' function: tidy values in str cols
def str_cleaner(uppercase=True):
    def cleaner(value):
        if not isinstance(value, str): # If not string, just return value 
            return value
        result = value 
        if uppercase: # If uppercase set to True, apply .strip().upper()
            result = result.strip().upper()
        else: # If uppercase set to False, just apply strip()
            result = result.strip()
        return result
    return cleaner

# Define 'expand_id_pairs' function: create unique Karpel file # and Police report # combinations
def expand_id_pairs(df, col1, col2): # col1='pbk_num', col2='report_num'
    # Create a list to store the pairs
    pairs = []
    
    # Iterate through each row of the DataFrame
    for _, row in df.iterrows():
        id1 = row[col1]
        # Split id2 by multiple separators
        id2_values = re.split(r'[,;&+]+', row[col2])  #\s - any whitespace
        
        # Create a pair for each id2 value
        for id2 in id2_values:
            # Skip empty values that might result from splitting
            if id2.strip():
                pairs.append({col1: id1, col2: id2.strip()})
    
    # Create a new DataFrame from the pairs
    result_df = pd.DataFrame(pairs)
    
    # Remove duplicates
    result_df = result_df.drop_duplicates()
    
    return result_df