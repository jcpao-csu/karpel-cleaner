"""Import 'Received Cases.csv' from Karpel"""

# Summary: the initial import and cleaning of the .csv data files from Python perform the following:
    # Rename column names
    # Declare data types for columns (mostly str, except 'count'=int, and datetime cols)
    # Remove unnecessary columns (e.g., 'rcvd_date', 'enter_date', 'user_id')
    # Eliminate test cases (using 'def_name')
    # Cleans string columns such that all string values are stripped of whitespace and uppercase, except 'ref_charge_description'
    # .csv file is then separated into unique tables: cases, charges, file#-court#, file#-report#
    # cleaned dfs are then exported for upload to Supabase

import warnings
import pandas as pd
from pathlib import Path

from helper_functions import row_cleaner, filter_columns, get_date_cols, str_cleaner, expand_id_pairs, export_df


# Ignore Parser Warning 
warnings.filterwarnings("ignore", category=pd.errors.ParserWarning)


# --- Define import_rcvd function --- 
def import_rcvd(rcvd_df_path: str, export_path: str):

    # Initialize Path object
    import_path = Path(rcvd_df_path)

    # Initialize 'Corrected Columns Headers' list from helper_files
    col_df = pd.read_excel(Path("helper_files/Corrected Columns Headers.xlsx"), sheet_name="Rcvd")
    col_names = (col_df.iloc[:, 1]).tolist()

    # No need for "rcvd_date", "enter_date", "user_id"
    keep_names = filter_columns(col_names)

    # Create dtype dict 
    col_dtypes = {key: ('str' if key != 'count' else 'int') for key in keep_names}

    # Date columns 
    rcvd_date_cols = get_date_cols(keep_names)

    # Create converters dict
    # Create a dictionary of converters for specific columns
    str_columns = {k: str_cleaner(uppercase=False) if k == 'ref_charge_description' else str_cleaner() 
                    for k, v in col_dtypes.items() if v == 'str' or k == 'ref_charge_description'}

    # Read CSV file
    df = pd.read_csv(
        import_path,
        header=0,
        names=col_names,
        usecols=keep_names,
        dtype=col_dtypes,
        converters=str_columns,
        encoding="utf-8"
    ) 

    # Remove test cases
    df = row_cleaner(df)

    # Parse dates for date cols 
    for col_name in rcvd_date_cols:
        df[col_name] = pd.to_datetime(df[col_name], format="%m/%d/%Y %I:%M:%S %p", errors="coerce") # date_format="%m/%d/%Y %I:%M:%S %p"
        df[col_name] = df[col_name].dt.date

    # Separate df into tables
        # Unique case (pbk_num- primary key)
        # Associated court_num (pbk_num, court_num) -- should indicate whether case has been FILED 
        # Associated report_num (pbk_num, report_num) -- associated police report number 
        # Unique charges (pbk_num, count- primary key)
        # Addresses 
        # Defendant 

    # Cases 
    cases = df[[
        'pbk_num', 
        # 'court_num', 
        # 'report_num', 
        'agency', # assume case-unique
        'ref_date', # assume case-unique
        'apa', # assume case-unique
        # 'def_name', -- no longer need, since we cleared test cases 
        'def_race', # assume case-unique
        'def_sex', # assume case-unique
        'def_dob', # assume case-unique
        # 'def_ssn', -- PPI 
        # 'def_street_address', -- ignore def address for now
        # 'def_street_address2',
        'def_city', # -- assume def-unique (connected to def profile), and a unique case can only have one unique def
        'def_state', 
        'def_zipcode', 
        # 'offense_street_address', -- ignore incident address for now
        # 'offense_street_address2', 
        # 'offense_city', 
        # 'offense_state', 
        # 'offense_zipcode',
        # 'count', -- charge-specific
        # 'ref_charge_code',
        # 'ref_charge_description', 
        # 'ref_severity', 
        # 'ref_class'
    ]].copy()
    cases.drop_duplicates(keep='first', inplace=True, ignore_index=True)

    # Charges 
    charges = df[[
        'pbk_num',
        'count', 
        'ref_charge_code',
        'ref_charge_description', 
        'ref_severity', 
        'ref_class',
        'offense_city', 
        'offense_state', 
        'offense_zipcode',
    ]].copy()
    charges.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    
    # File # - Court # (one-to-zero/one)
    file_court_num = df[[ # should tell us which referred cases have been filed 
        'pbk_num',
        'court_num'
    ]].copy()
    file_court_num.drop_duplicates(keep='first', inplace=True, ignore_index=True)

    # File # - Report # (many-to-many)
    file_report_num = df[[
        'pbk_num',
        'report_num'
    ]].copy()

    file_report_num.drop_duplicates(keep='first', inplace=True, ignore_index=True)
    file_report_num = expand_id_pairs(file_report_num, col1='pbk_num', col2='report_num') # this appears to have generally worked, however see: 095469895, 095469890 

    # Export as CSV 
    export_df(df, "rcvd_df", export_path)
    export_df(cases, "rcvd_cases", export_path)
    export_df(charges, "rcvd_charges", export_path)
    export_df(file_court_num, "rcvd_file_court_num", export_path)
    export_df(file_report_num, "rcvd_file_report_num", export_path)

    # Return data objects 
    return df, cases, charges, file_court_num, file_report_num