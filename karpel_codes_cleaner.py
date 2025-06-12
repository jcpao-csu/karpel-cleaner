import pandas as pd
from pathlib import Path

disp_codes = Path("helper_files/karpel_codes/raw/Disposition Codes.csv")
ntfld_codes = Path("helper_files/karpel_codes/raw/Not Filed Codes.csv")

karpel_disp_codes = Path("helper_files/karpel_codes/raw/2025_05_16/Disp Event Codes.csv")
karpel_ntfld_codes = Path("helper_files/karpel_codes/raw/2025_05_16/Not Filed Codes.csv")

nisha_karpel_codes = Path("helper_files/karpel_codes/raw/2024_04_22_Nisha Karpel Codes.csv")

# Import DFs

karpel_codes = pd.read_csv(nisha_karpel_codes, encoding="utf-8")
disp_codes = pd.read_csv(disp_codes, encoding="utf-8")
ntfld_codes = pd.read_csv(ntfld_codes, encoding="utf-8")

karpel_disp_codes = pd.read_csv(karpel_disp_codes, encoding="utf-8")
karpel_disp_codes.columns = ["disp_code", "disp_desc", "disp_event_text", "nolle_flag", "case_stage"]
karpel_ntfld_codes = pd.read_csv(karpel_ntfld_codes, encoding="utf-8")
karpel_ntfld_codes.columns = ["disp_code", "disp_desc", "disp_cat"]

# Join DFs 
disp_codes = pd.merge(disp_codes, karpel_codes, on="disp_code", how="left")
ntfld_codes = pd.merge(ntfld_codes, karpel_codes, on="disp_code", how="left")

# Export DFs 
disp_codes.to_csv("helper_files/karpel_codes/cleaned/2025_05_16/Disposition Codes.csv", encoding="utf-8", index=False)
ntfld_codes.to_csv("helper_files/karpel_codes/cleaned/2025_05_16/Not Filed Codes.csv", encoding="utf-8", index=False)

# Import DFs 
disp_codes = Path("helper_files/karpel_codes/cleaned/2025_05_16/Disposition Codes.csv")
ntfld_codes = Path("helper_files/karpel_codes/cleaned/2025_05_16/Not Filed Codes.csv")

disp_codes = pd.read_csv(disp_codes, encoding="utf-8")
ntfld_codes = pd.read_csv(ntfld_codes, encoding="utf-8")
disp_codes['disp_category'].value_counts()
