import pandas as pd
from great_expectations.data_context import get_context

def get_validator_from_df(df: pd.DataFrame, datasource_name = "in_memory_pandas"):
    """
    Get a Great Expectations Validator from a pandas DataFrame using an in-memory datasource.
    """

    context = get_context()

    if datasource_name not in context.list_datasources():
        context.sources.add_pandas(name = datasource_name)

    validator = context.sources.pandas_default_in_memory_data_asset(
        name = 'in_memory_dataset',
        batch_data = df
    )

    return validator

def run_expectations(validator, action_plan:dict):
    """
    Apply expectations dynamically based on profiler-generated action plan.
    """
    batch_size = len(validator.active_batch_data)

    #Missing values
    for col in action_plan.get("missing", []):
        validator.expect_column_values_to_not_be_null(column = col)
    
    #Type mismatches
    for col in action_plan.get("type_mismatches", []):
        validator.expect_column_values_to_be_in_type_list(col, type_ = "FLOAT")
    
    #Constant Column
    for col in action_plan.get("constant_columns", []):
        validator.expect_column_unique_value_count_to_be_between(col, min_value = 2)
    
    #High Cardinality
    for col in action_plan.get("high_cardinality", []):
        max_val = int(0.9 * batch_size)
        validator.expect_column_unique_value_count_to_be_between(col, max_value = max_val)
    
    #Format Issues
    for col in action_plan.get("format_issues", []):
        validator.expect_column_values_to_match_regex(col, r"^[a-z0-9\s]+$")
    
    #Date parsing errors
    for col in action_plan.get("date_parse_errors", []):
        try:
            validator.expect_column_values_to_match_strftime_format(
                col, "%Y-%m-%d", mostly=0.8
            )
        except Exception:
            validator.expect_column_values_to_be_dateutil_parseable(col)
    
    #mixed types
    for col in action_plan.get("mixed_types", []):
        validator.expect_column_values_to_match_regex(col, r".*")
    
    if action_plan.get("duplicates", False):
        print("⚠️ WARNING: Duplicate rows detected — Great Expectations cannot validate row-level duplication.")
    
    if action_plan.get("potential_outliers", []):
        print("⚠️ WARNING: Outliers detected — Great Expectations does not support statistical outlier validation.")
    
    return validator.validate()