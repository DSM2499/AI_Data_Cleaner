import os

OUTPUT_DIR = "/Users/dinakarmurthy/Desktop/Job Work/Projects/AI_Data_Cleaner/ai_generated"
SCRIPT_FILE = os.path.join(OUTPUT_DIR, "cleaning_script.py")
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "cleaning_summary.md")

def save_ai_output(ai_response: str):
    """
    Splits AI response into code and summary, and saves both for UI display.
    Returns code_str.
    """
    os.makedirs(OUTPUT_DIR, exist_ok = True)

    #Extract code
    code_str = ""
    if "```python" in ai_response:
        start = ai_response.index("```python") + len("```python")
        end = ai_response.index("```", start)
        code_str = ai_response[start:end].strip()
    else:
        #fallback
        lines = ai_response.splitlines()
        code_start_idx = next((i for i, line in enumerate(lines) if "def clean_dataframe" in line), 0)
        code_str = "\n".join(lines[code_start_idx:])
    
    summary = ""
    if "# Summary" in ai_response:
        summary = ai_response[ai_response.index("# Summary"):].strip()
    else:
        summary_start = ai_response.lower().find("summary")
        if summary_start != -1:
            summary = ai_response[summary_start:].strip()
    
    with open(SCRIPT_FILE, "w") as f:
        f.write(code_str)
    
    with open(SUMMARY_FILE, "w") as f:
        f.write(summary)
    
    return code_str