import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

CLEANING_PROMPT_TEMPLATE = """
You are a data cleaning expert. Your knowledge of pandas, data cleaning techniques, best practices, and data science principles is extensive.

Below is the schema and data profile of a pandas DataFrame, including data types, missing values, anomalies, and a sample of real values.

Your task:
1. Generate a Python function called `clean_dataframe(df)` that applies all appropriate data cleaning steps using pandas.
2. Return a short summary (5–10 bullet points) describing what this function does.

The function should:
- Not use any libraries beyond pandas
- Use best practices (e.g., fillna, astype, strip, drop, etc.)
- Avoid modifying df in place if possible
- Handle columns named in the anomalies section

<<CONTEXT>>
{context}
"""

def generate_cleaning_code(context: str, model = "gpt-3.5-turbo"):
    prompt = CLEANING_PROMPT_TEMPLATE.format(context = context)

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model = model,
        messages = [
            {"role": "system", "content": "You are a helpful AI that writes high-quality, production-ready data cleaning code."},
            {"role": "user", "content": prompt} 
        ],
        temperature = 0.5,
    )

    result = response.choices[0].message.content.strip()
    return result