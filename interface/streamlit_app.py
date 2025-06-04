# interface/streamlit_app.py

import streamlit as st
import pandas as pd
import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print(f"Project root added to sys.path: {PROJECT_ROOT}")

from cleaner.data_profiler import profile_dataset
from ai_layer.code_input_builder import build_cleaning_prompt_context
from ai_layer.code_generator import generate_cleaning_code
from ai_layer.code_executor import save_ai_output

st.set_page_config(page_title="AI Data Cleaning Assistant", layout="wide")
st.title("🧼 AI Data Cleaning Assistant")
st.caption("Upload your dataset and generate custom Python cleaning code using AI.")

# Upload Section
uploaded_file = st.file_uploader("📤 Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file, encoding = "utf-8", header = 0)
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file, encoding = "ISO-8859-1", header = 0)
    
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (list, tuple, dict))).any():
            df[col] = df[col].astype(str)
    
    st.subheader("📊 Sample of Uploaded Data")
    st.dataframe(df.head(), use_container_width = True)

    # Generate cleaning context
    _, action_plan, summary_df = profile_dataset(df)
    context_str = build_cleaning_prompt_context(df, action_plan)

    # Show action plan
    st.subheader("🧠 Action Plan")
    for action in action_plan:
        st.markdown(f"- {action} columns: {action_plan[action]}")

    # Show summary
    st.subheader("📊 Data Profiling Summary")
    st.dataframe(summary_df, use_container_width = True)
    

    if st.button("🧠 Generate Cleaning Code with AI"):
        with st.spinner("Calling the AI model..."):
            ai_response = generate_cleaning_code(context_str)
            code_str = save_ai_output(ai_response)

        st.success("✅ Cleaning script generated!")
        
        # Show summary
        st.subheader("🧾 Summary of Cleaning Logic")
        with open("ai_generated/cleaning_summary.md") as f:
            summary = f.read()
            st.markdown(summary)

        # Show Python code
        st.subheader("📜 Python Code to Clean Your Data")
        st.code(code_str, language = "python")

        st.info("You can copy and paste this code into your notebook or script.")
