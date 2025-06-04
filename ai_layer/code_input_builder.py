import pandas as pd

def build_cleaning_prompt_context(df: pd.DataFrame, action_plan: dict, sample_rows = 5) -> str:
    """
    Build a prompt context for cleaning a dataset based on the action plan.
    """

    lines = []

    #Add Schema
    lines.append("Dataset Schema:")
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = df[col].isnull().sum()
        lines.append(f"- {col}: {dtype}, {nulls} nulls")

    #Add anomalies
    lines.append("\nAnomalies:")
    for k, cols in action_plan.items():
        if isinstance(cols, list) and cols:
            lines.append(f"- {k}: {', '.join(cols)}")
        elif isinstance(cols, bool) and cols:
            lines.append(f"- {k}: True")
    
    #Add sample rows
    lines.append("\nSample Rows:")
    samples = df.sample(min(sample_rows, len(df)), random_state = 24)
    lines.append(samples.to_string(index = False))

    return "\n".join(lines)