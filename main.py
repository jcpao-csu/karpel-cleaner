"""Main Python script runner"""

import pandas as pd
from pathlib import Path

from helper_functions import locate_data, create_dir
from import_rcvd import import_rcvd
from import_ntfld import import_ntfld
from import_fld import import_fld
from import_disp import import_disp

# Identify most recent data dump
df_path = locate_data("data")

# Create sub-folder for cleaned data
export_path = create_dir(df_path) # df_path

# Import CSV files, clean / create tables, and export to "cleaned" sub-folder
for item in Path(df_path).iterdir():
    if item.is_file():
        if "Received" in str(item):
            rcvd, rcvd_cases, rcvd_charges, rcvd_file_court, rcvd_file_report = import_rcvd(item, export_path)
        elif "Not Filed" in str(item):
            ntfld, ntfld_cases, ntfld_charges, ntfld_file_report = import_ntfld(item, export_path)
        elif "Filed" in str(item):
            fld, fld_cases, fld_charges, fld_file_court, fld_file_report = import_fld(item, export_path)
        elif "Disposed" in str(item):
            disp, disp_cases, disp_charges, disp_file_court, disp_file_report = import_disp(item, export_path)