import pandas as pd
from tabulate import tabulate
import numpy as np
import re
import warnings

def try_parse_dates(series: pd.Series):
    # Attempt common formats first
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d-%m-%Y"]
    for fmt in formats:
        try:
            return pd.to_datetime(series, format=fmt, errors='raise')
        except Exception:
            continue
    # Fallback to dateutil with warnings suppressed
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        return pd.to_datetime(series, errors='coerce')

def profile_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:

    #print("\n📊 Dataset Preview:")
    #print(tabulate(df.head(), headers = 'keys', tablefmt = 'psql'))

    #print("\n📊 Dataset Preview:")

    summary = []
    action_plan = {
        "missing": [],
        "duplicates": False,
        "type_mismatches": [],
        "potential_outliers": [],
        "constant_columns": [],
        "high_cardinality": [],
        "format_issues": [],
        "date_parse_errors": [],
        "mixed_types": [],
    }

    for col in df.columns:
        col_data = df[col]
        dtype = col_data.dtype
        nulls = col_data.isnull().sum()
        unique_vals = col_data.nunique()
        sample = col_data.dropna().astype(str).sample(
            min(3, len(col_data.dropna())), random_state = 24).tolist()
        
        # Missing values
        if nulls > 0:
            action_plan["missing"].append(col)
        
        #Type Mismatch
        if dtype == 'object':
            try:
                pd.to_numeric(col_data, errors = 'coerce')
                action_plan["type_mismatches"].append(col)
            except:
                pass
        
        #Constant Column
        if unique_vals == 1:
            action_plan["constant_columns"].append(col)
        
        #High Cardinality
        if dtype == 'object' and unique_vals > 0.9 * len(df):
            action_plan["high_cardinality"].append(col)
        
        #Mixed Types
        if col_data.apply(type).nunique() > 1:
            action_plan["mixed_types"].append(col)
        
        #Format issues
        if dtype == 'object':
            has_whitespaces = col_data.dropna().str.contains(r"^\s|\s$").any()
            has_case_mismatch = col_data.dropna().str.contains(
                r"[A-Z]").any() and col_data.str.lower().nunique() < unique_vals
            if has_whitespaces or has_case_mismatch:
                action_plan["format_issues"].append(col)
        
        #Date Parsing
        if 'date' in col.lower() or dtype == 'object':
            try:
                parsed = try_parse_dates(col_data)
                if parsed.isnull().sum() > 0 and parsed.notnull().sum() > 0:
                    action_plan["date_parse_errors"].append(col)
            except:
                pass
        
        #Outliers using IQR
        if dtype in ['int64', 'float64']:
            q1 = col_data.quantile(0.25)
            q3 = col_data.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            if len(outliers) > 0:
                action_plan["potential_outliers"].append(col)
        
        summary.append([col, nulls, dtype, unique_vals, ", ".join(map(str, sample))])
    
    #print(tabulate(summary, headers = 
    #               ['Column', 'Nulls', 'Type', 'Unique', 'Sample'], tablefmt = 'grid'))
    summary_df = pd.DataFrame(summary, columns = ['Column', 'Nulls', 'Type', 'Unique', 'Sample'])
    
    dupes = df.duplicated().sum()
    if dupes > 0:
        action_plan["duplicates"] = True
    
    print(f"\n📊 Found {dupes} duplicate rows in the dataset.")
    
    return df, action_plan, summary_df